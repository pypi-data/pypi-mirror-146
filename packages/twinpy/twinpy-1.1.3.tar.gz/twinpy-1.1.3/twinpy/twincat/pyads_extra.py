"""
This file complements the pyads.ads file.

pyads has methods to read from / write to multiple symbols at once, but those don't
work neatly for the AdsSymbol class. Here a new interface is defined.
Unfortunately this is not very DRY, but it can't be helped.

This was offered as an addition to pyads here:
https://github.com/stlehmann/pyads/pull/268, but it was decided not to merge it.
"""

from pyads import AdsSymbol
from pyads.structs import AmsAddr
from pyads.pyads_ex import adsSumReadBytes, adsSumWriteBytes, \
    get_value_from_ctype_data, type_is_string
from pyads.errorcodes import ERROR_CODES
from ctypes import sizeof
import struct
from typing import Optional, List, Dict, Any, Tuple


def adsSumReadSymbols(
    port: int,
    address: AmsAddr,
    symbols: List[AdsSymbol],
) -> Dict[AdsSymbol, Any]:
    """Perform a sum read to get the value of multiple variables.

    Different form :func:`pyads.adsSumRead` because `adsSumRead` relies on
    `SAdsSymbolEntry` for the symbol info, which we don't have available.

    :param port: Local AMS port as returned by adsPortOpenEx()
    :param address: Local or remote AmsAddr
    :param symbols: List of ADS symbols
    :return: Dict of variable names and values
    """
    result: Dict[AdsSymbol, Optional[Any]] = {s: None for s in symbols}

    num_requests = len(symbols)

    symbol_infos = [
        (
            symbol.index_group,
            symbol.index_offset,
            sizeof(symbol.plc_type),
        )
        for symbol in symbols
    ]
    # When a read is split, `data_symbols` will be bigger than `data_names`
    # Therefore we avoid looping over `data_symbols`

    sum_response = adsSumReadBytes(port, address, symbol_infos)

    data_start = 4 * num_requests
    offset = data_start

    for i, symbol in enumerate(symbols):
        error = struct.unpack_from("<I", sum_response, offset=i * 4)[0]

        size = sizeof(symbol.plc_type)

        if error:
            result[symbol] = ERROR_CODES[error]
        else:

            # Create ctypes instance, then convert to Python value
            obj = symbol.plc_type.from_buffer(sum_response, offset)
            value = get_value_from_ctype_data(obj, symbol.plc_type)

            result[symbol] = value

        offset += size

    return result


def adsSumWriteSymbols(
    port: int,
    address: AmsAddr,
    symbols_and_values: Dict[AdsSymbol, Any],
) -> Dict[AdsSymbol, str]:
    """Perform a sum write to write the value of multiple ADS variables

    `data_symbols` should contain tuples of information according
    to (idx_group, idx_offset, plc_type). Note that the type is a
    ctypes based type, not an integer like in `SAdsSymbolEntry`.

    The difference with :func:`pyads.adsSumWrite` is this version doesn't
    rely on the `adsSymbolEntry` type.

    :param port: Local AMS port as returned by adsPortOpenEx()
    :param address: Local or remote AmsAddr
    :param symbols_and_values: Dict of variables and values to be written
    :return: Dict of variable names and error codes
    """

    offset = 0
    num_requests = len(symbols_and_values)
    total_request_size = num_requests * 3 * 4  # iGroup, iOffset & size

    for symbol in symbols_and_values.keys():
        total_request_size += sizeof(symbol.plc_type)

    buf = bytearray(total_request_size)

    for symbol in symbols_and_values.keys():

        struct.pack_into("<I", buf, offset, symbol.index_group)
        struct.pack_into("<I", buf, offset + 4, symbol.index_offset)
        struct.pack_into("<I", buf, offset + 8, sizeof(symbol.plc_type))
        offset += 12

    for symbol, value in symbols_and_values.items():

        size = sizeof(symbol.plc_type)

        if type_is_string(symbol.plc_type):
            buf[offset : offset + len(value)] = value.encode("utf-8")
        else:
            # Create ctypes instance from Python value
            if type(symbol.plc_type).__name__ == "PyCArrayType":
                write_data = symbol.plc_type(*value)
            elif type(value) is symbol.plc_type:
                write_data = value
            else:
                write_data = symbol.plc_type(value)
            buf[offset : offset + size] = bytes(write_data)

        offset += size

    error_descriptions = adsSumWriteBytes(
        port,
        address,
        num_requests,
        buf,
    )

    return dict(zip(symbols_and_values.keys(), error_descriptions))
