from pyads import AdsSymbol, Connection
from pyads.constants import MAX_ADS_SUB_COMMANDS
from pyads.ads import _list_slice_generator, _dict_slice_generator
import pyads
from typing import Optional, Union, Type, List, Dict, Any, Tuple

from .symbols import Parameter, Signal
from .pyads_extra import adsSumReadSymbols, adsSumWriteSymbols


class TwincatConnection(Connection):
    """Extend default Connection object (typically named `plc`).

    ADS connection with custom features.
    """

    def __init__(
        self,
        ams_net_id: str = "127.0.0.1.1.1",
        ams_net_port: int = 350,
        ip_address: str = None,
    ):
        """

        Note that this version will connect on object creation, throwing an exception
        when it fails. `pyads.Connection` waits for `.open()` and will fail quietly.

        :param ams_net_id: TwinCAT AMS address (default is localhost)
        :param ams_net_port: ADS Port (default is 350)
        :param ip_address: Target IP (automatically deduced from AMS address)
        :raises pyads.ADSError: When connection failed
        """

        super().__init__(ams_net_id, ams_net_port, ip_address)

        self.open()

        if not self.is_open:
            raise pyads.ADSError(
                text="Connection to TwinCAT could not be "
                "established. Is TwinCAT in run mode?"
                "Are the port and address correct?"
            )

    def get_module_info(self, module_name: str) -> dict:
        """Get information about live module."""

        # Read all info as list of bytes (doing it as a list of variable
        # names fails)
        try:
            var_name = module_name + ".ModuleInfo"
            data = self.read_by_name(var_name, pyads.PLCTYPE_ARR_DINT(37))
        except pyads.ADSError as err:
            # Re-raise error
            raise pyads.ADSError(
                text="Could not connect to TwinCAT module. "
                "Does the target module exist in the "
                "running TwinCAT instance?"
            ) from err

        return {
            "ClassId": data[0:4],
            "BuildTimeStamp": data[4],
            "ModelCheckSum": data[5:9],
            "ModelVersion": data[9:13],
            "TwinCatVersion": data[13:17],
            "TcTargetVersion": data[17:21],
            "MatlabVersion": data[21:25],
            "SimulinkVersion": data[25:29],
            "CoderVersion": data[29:33],
            "TcTargetLicenseID": data[33:38],
        }

    def get_signal(
        self,
        name: Optional[str] = None,
        index_group: Optional[int] = None,
        index_offset: Optional[int] = None,
        symbol_type: Optional[Union[str, Type]] = None,
    ) -> Signal:
        """Get Signal instance.

        See :class:`Signal`.
        """
        return Signal(
            plc=self,
            name=name,
            index_group=index_group,
            index_offset=index_offset,
            symbol_type=symbol_type,
        )

    def get_parameter(
        self,
        name: Optional[str] = None,
        index_group: Optional[int] = None,
        index_offset: Optional[int] = None,
        symbol_type: Optional[Union[str, Type]] = None,
    ) -> Parameter:
        """Get Parameter instance.

        See :class:`Parameter`.
        """
        return Parameter(
            plc=self,
            name=name,
            index_group=index_group,
            index_offset=index_offset,
            symbol_type=symbol_type,
        )

    def read_list_of_symbols(
            self,
            symbols: List[AdsSymbol],
            ads_sub_commands: int = MAX_ADS_SUB_COMMANDS,
    ) -> Dict[AdsSymbol, Any]:
        """Read a list of symbols in a single request.

        Same principe as `read_list_by_name`. See :func:`read_list_by_name` for
        more info.

        This version doesn't work for structs.

        The `_value` property for each symbol will be updated. A dictionary will also
        be returned of the symbol names and their new values.
        """

        for symbol in symbols:
            if symbol.is_structure:
                raise ValueError("Method is not available for structured variables")

        # Relying on `adsSumRead()` is tricky, because we do not have the `dataType`
        # (integer) for each symbol, we only have the ctypes-type.

        # Limit request side, split into multiple if needed
        if len(symbols) <= ads_sub_commands:
            symbols_list = [symbols]  # Turn into list of a single element
        else:
            symbols_list = _list_slice_generator(symbols, ads_sub_commands)

        return_data: Dict[AdsSymbol, Any] = {}

        for symbols_slice in symbols_list:
            result = adsSumReadSymbols(
                self._port,
                self._adr,
                symbols_slice,
            )

            return_data.update(result)

        for symbol, value in return_data.items():
            symbol._value = value

        return return_data

    def write_list_of_symbols(
        self,
        symbols_and_values: Dict[AdsSymbol, Any],
        ads_sub_commands: int = MAX_ADS_SUB_COMMANDS,
    ) -> Dict[AdsSymbol, str]:
        """Write new values to a list of symbols.

        Same principe as `write_list_by_name`. See :func:`write_list_by_name` for
        more info.

        For example:

        .. code:: python

            # Using dict
            new_data = {symbol1: 3.14, symbol2: False}
            plc.write_list_of_symbols(new_data)

        :param symbols_and_values: Symbols to write to
        :param ads_sub_commands: Max. number of symbols per call (see
                                 `write_list_by_name`)
        """

        for symbol in symbols_and_values.keys():
            if symbol.is_structure:
                raise ValueError("Method not available for structured variables")

        for symbol, new_value in symbols_and_values.items():
            symbol._value = new_value  # Update cache

        if len(symbols_and_values) <= ads_sub_commands:
            # Turn into array of single element
            symbols_and_values_list = [symbols_and_values]
        else:
            symbols_and_values_list = _dict_slice_generator(
                symbols_and_values, ads_sub_commands
            )

        return_data: Dict[AdsSymbol, str] = {}
        for symbols_and_value_slice in symbols_and_values_list:
            result = adsSumWriteSymbols(
                self._port,
                self._adr,
                symbols_and_value_slice,
            )
            return_data.update(result)

        return return_data
