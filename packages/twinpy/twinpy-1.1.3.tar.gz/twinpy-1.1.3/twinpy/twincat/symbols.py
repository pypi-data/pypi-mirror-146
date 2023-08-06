"""Module with classes that wrap around TwinCAT symbols.

With 'symbol' we mean ADS variable.
"""


from __future__ import annotations  # Allows forward declarations
from abc import ABC
from typing import TYPE_CHECKING  # Allows circular dependencies for types
from typing import Tuple, Callable, Any, Optional, Union, Type
import pyads

if TYPE_CHECKING:
    from .simulink import SimulinkBlock


class Symbol(pyads.AdsSymbol, ABC):
    """Base (abstract) class for a TwinCAT symbol.

    Extends :class:`pyads.AdsSymbol` - Introduced in pyads 3.3.1

    A symbol (or a Symbol sub-class) is typically owned by a block in a
    Simulink model.
    Each symbol contains a reference back to the block that owns it, which can
    be used to trace back to the model that owns that block.
    The symbol needs a reference to the connection object directly.

    Symbols can be created from a block or manually (either based on name or
    by providing all information).

    :ivar value: The **buffered** value, *not* necessarily the latest value. The buffer
                 is updated on each read, write and notification callback. It can be
                 useful when the value needs to be applied multiple times, to avoid
                 storing the value in your own variable.
    """

    def __init__(
        self,
        block: Optional[SimulinkBlock] = None,
        plc: pyads.Connection = None,
        name: Optional[str] = None,
        index_group: Optional[int] = None,
        index_offset: Optional[int] = None,
        symbol_type: Optional[Union[str, Type]] = None,
    ) -> None:
        """

        See :class:`pyads.Symbol`. If a block was passed, index_group and plc
        are automatically extracted from it and do not need to passed too.

        Additional arguments:

        :param block: Block that owns this symbol (default: None)
        :raises ValueError:
        """

        self.block = block

        if block is not None:
            if plc is None:
                plc = block.get_plc()
            if index_group is None:
                index_group = block.get_index_group()

        super().__init__(
            plc=plc,
            name=name,
            index_group=index_group,
            index_offset=index_offset,
            symbol_type=symbol_type,
        )

    def set_connection(self, connection: Optional[pyads.Connection]):
        """Update the connection reference."""
        self._plc = connection

    def get(self):
        """Get the symbol value from TwinCAT.

        Simply an alias for :meth:`read`.
        """
        return self.read()

    def set(self, val):
        """Write the symbol in TwinCAT.

        Simply an alias for :meth:`write`.
        """
        return self.write(val)

    def read(self) -> Any:
        """Read the current value of this symbol.

        The new read value is also saved in the buffer.
        Overridden from AdsSymbol, to work without an open Connection.
        """
        if self.plc_type is None:
            raise NotImplementedError(
                "The type `{0}` has not yet been mapped "
                "to a PLCTYPE".format(self.symbol_type)
            )

        if self._plc is None:
            return None

        return super().read()

    def write(self, new_value: Optional[Any] = None) -> None:
        """Write a new value or the buffered value to the symbol.

        When a new value was written, the buffer is updated.
        Overridden from AdsSymbol, to work without an open Connection

        :param new_value    Value to be written to symbol (if None,
                            the buffered value is send instead)
        """
        if self.plc_type is None:
            raise NotImplementedError(
                "The type `{0}` has not yet been mapped "
                "to a PLCTYPE".format(self.symbol_type)
            )

        if self._plc is None:
            return

        if isinstance(new_value, str):  # Convert from string if necessary
            new_value = self.get_value_from_string(new_value)

        super().write(new_value)

    def get_value_from_string(self, text: str) -> Any:
        """Parse a string to the right data type."""

        if self.symbol_type.endswith("REAL"):
            return float(text)

        if self.symbol_type.endswith("INT"):
            return int(text)

        if self.symbol_type == "BOOL":
            if text.lower() in ["on", "true", "t", "yes", "y", "1"]:
                return 1
            if text.lower() in ["off", "false", "f", "no", "n", "0"]:
                return 0
            raise ValueError("Value `{}` does not map to a boolean value".format(str))

        raise NotImplementedError(
            "The value `{0}` could not be mapped to "
            "type `{1}`".format(text, self.symbol_type)
        )

    def add_device_notification(
        self,
        callback: Callable[[Any], None],
        attr: Optional[pyads.NotificationAttrib] = None,
        user_handle: Optional[int] = None,
    ) -> Optional[Tuple[int, int]]:
        """Add on-change callback to symbol.

        Superclass method is used, this version adds a wrapper for the
        callback to set the variable type. The user-defined callback will be
        called with the new symbol value as an argument.
        """
        if self._plc is None or self.plc_type is None:
            return None  # Do nothing

        def callback_wrapper(notification, *_):
            """Callback wrapper to make datatype conversion.

            As a bonus, this wrapper will also update the internal buffer.
            """
            (_handle, _timestamp, new_value) = self._plc.parse_notification(
                notification, self.plc_type
            )
            self.value = new_value  # Update buffer
            return callback(new_value)  # Now call user function

        try:
            return super().add_device_notification(callback=callback_wrapper, attr=attr)
        except pyads.ADSError as err:
            if err.err_code == 1793:
                raise pyads.ADSError(
                    text="Symbol does not seem to support device callbacks - "
                    "Or maybe the group and offset indices are "
                    "incorrect?"
                ) from err
            raise err

    def del_device_notification(self, handles: Tuple[int, int]):
        """Remove a single device notification by handles."""
        if self._plc is not None:
            super().del_device_notification(handles)


class Parameter(Symbol):
    """A TwinCAT parameter.

    A constant setting, e.g. a gain block value, constant block value. For read/write
    access.
    Needs no changes, can use the default.

    See :class:`~Symbol`.
    """


class Signal(Symbol):
    """A TwinCAT signal.

    Typically a port, e.g. a subsystem input or output
    """

    def set(self, val):
        raise RuntimeError(
            "Symbol `{0}` is a Signal and is read-only, it "
            "cannot be set".format(self.name)
        )
