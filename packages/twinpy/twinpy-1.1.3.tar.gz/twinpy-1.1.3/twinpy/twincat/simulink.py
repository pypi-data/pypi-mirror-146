"""Model to wrap around a Simulink model.

An object for a Simulink model is created first before a
TwinCAT connection is made. We cannot get the original
model structure from TwinCAT alone.
"""

from __future__ import annotations  # Allows forward declarations
from typing import Optional, List, Dict, Union

import os
import xml.etree.ElementTree as ElementTree
import re
import warnings

from .connection import TwincatConnection
from .symbols import Symbol, Signal, Parameter

# Constants
FILENAME_TEMPLATE = "{0}_ModuleInfo.xml"

# Store compile regex objects to save some performance
re_characters = re.compile(r"\W+")
re_leading = re.compile(r"^[\d\_]+")


def sanitize_name(name: str) -> str:
    """Reduce a string to characters which are allowed in a Python variable name.

    This is needed because Simulink blocks can contain more characters than
    this. Python variables can only contain a-z, A-Z, 0-9 and '_'.
    Additionally, a variable cannot start with a digit, nor can it start with
    an underscore to prevent conflicts with semi-private properties.
    """

    # Built-in `\W` checks for anything that is *not* a letter, digit
    # or underscore
    name = re_characters.sub("", name)

    # Remove all leading digits and underscores
    name = re_leading.sub("", name)

    return name


class SimulinkBlock:
    """
    A single Simulink Block (anything, e.g. constant, gain, a sub-system)

    A SimulinkBlock can contain children, which are also SimulinkBlock objects.
    Using __getattr__ those subblocks (and their symbols) can be addressed
    directly:

        model = ...
        # Subblocks can be addressed smoothly:
        print(model.MySubsystem.MyConstant.Value)

    Blocks contain parameters (`Value`) in the example above. When only a
    single parameter or signal is present, you can directly call it from the
    block itself:

        print(model.MySubsystem.MyConstant.get())  # Short
        print(model.MySubsystem.MyConstant.Value.get())  # Same but longer

        print(model.MySubsystem.MySineWave.Phase.get())  # Multiple parameters
        print(model.MySubsystem.MySineWave.Amplitude.get())

    """

    def __init__(self, xmltree: ElementTree.Element, model: SimulinkModel):
        """
        Create this block based on an XML tree

        Sub-blocks are created too based on the remaining tree structure. This
        means the creation of blocks works recursively.

        :param xmltree: A branch of a model XML tree (or the entire tree)
        :param model: A reference back to the original model (the root of the
                      structure)
        """

        name_branch = xmltree.find("Name")
        self.name = name_branch.text if name_branch is not None else None

        type_branch = xmltree.find("Type")
        self.type = type_branch.text if type_branch is not None else None

        identifier_branch = xmltree.find("Identifier")
        self.identifier = (
            identifier_branch.text if identifier_branch is not None else None
        )

        if self.name is None and self.identifier is not None:
            # Use part of identifier instead
            self.name = self.identifier.rsplit("/")[-1]

        # Private property, references back the complete model
        self._model = model

        self._subblocks = {}
        self._parameters = {}
        self._signals = {}

        # Dict of sub-blocks (private property)
        self._subblocks = self.make_subblocks(xmltree)
        # Dict of parameters (private property)
        self._parameters = self.make_parameters(xmltree)
        # Dict of signals (private property)
        self._signals = self.make_signals(xmltree)

    def make_subblocks(self, xmltree: ElementTree.Element) -> Dict[str, SimulinkBlock]:
        """Build sub-blocks (this makes the SimulinkBlocks recursive)."""

        subblocks = {}  # List of sub-blocks (private property)

        for subblock_xml in xmltree.findall("Block"):

            if (
                subblock_xml.find("Type").text in ["Inport", "Outport", "Terminator"]
                or subblock_xml.find("Identifier") is None
            ):
                # Skip blocks that don't take or show any information, and skip
                # blocks that somehow lack an identifier
                continue

            subblock = SimulinkBlock(subblock_xml, self._model)
            block_name = sanitize_name(subblock.name)
            subblocks[block_name] = subblock

        return subblocks

    def make_parameters(self, xmltree: ElementTree.Element) -> dict:
        """Find and create Parameters in the current block."""

        parameters = {}

        for parameter_xml in xmltree.findall("Parameter"):
            # Skip first two characters:
            index_offset_hex = parameter_xml.find("AdsIdxOffs").text[2:]
            index_offset = int(index_offset_hex, 16)  # Convert to decimal

            parameter = Parameter(
                block=self,
                name=parameter_xml.get("Name"),
                index_offset=index_offset,
                symbol_type=parameter_xml.find("Type").text,
            )
            parameters[sanitize_name(parameter.name)] = parameter

        return parameters

    def make_signals(self, xmltree: ElementTree.Element) -> dict:
        """Find and create Signals in the current block."""

        signals = {}

        # Signals are part of Ports in Simulink
        for port_xml in xmltree.findall("Port"):

            signal_xml = port_xml.find("Signal")
            if signal_xml is None:
                continue  # No accessible signal for this port

            # Skip first two characters:
            index_offset_hex = signal_xml.find("AdsIdxOffs").text[2:]
            index_offset = int(index_offset_hex, 16)  # Convert to decimal

            name = signal_xml.find("GlobalName").text
            if name.startswith("BlockIO."):
                name = name[8:]

            signal = Signal(
                block=self,
                name=name,
                index_offset=index_offset,
                symbol_type=signal_xml.find("Type").text,
            )

            type_xml = port_xml.find("Type")
            # Port number, 1-based (but this is merely a human-interacted
            # property)
            port_number = type_xml.get("No")
            type_name = type_xml.text.lower()
            if type_name.startswith("out"):
                key = "so"
            elif type_name.startswith("in"):
                key = "si"
            else:
                continue  # Could be a trigger port or something else weird

            key += port_number

            signals[sanitize_name(key)] = signal
            # A signal name might be identical to a parameter, instead we save
            # it like "in_1" or "out_5"

        return signals

    def _get_first_symbol(self) -> Symbol:
        """Get reference to first parameter or signal.

        Throw an error if there are none or more than one (to prevent
        accidental ambiguity).
        """
        if len(self._parameters) > 1:
            raise RuntimeError(
                "Block `{0}` has {1} parameters, you need to "
                "address them by name directly".format(self.name, len(self._parameters))
            )

        if len(self._signals) > 1:
            raise RuntimeError(
                "Block `{0}` has {1} signals, you need to"
                "address them by name directly".format(self.name, len(self._signals))
            )

        if self._parameters:
            key = next(iter(self._parameters))
            return self._parameters[key]

        if self._signals:
            key = next(iter(self._signals))
            return self._signals[key]

        raise RuntimeError("Block `{0}` has no parameters or signals".format(self.name))

    def get(self):
        """Get value of the first symbol."""

        symbol = self._get_first_symbol()
        return symbol.get()

    def set(self, val):
        """Set value of the first symbol."""

        symbol = self._get_first_symbol()
        return symbol.set(val)

    def get_plc(self) -> Optional[TwincatConnection]:
        """Return Connection (owned by model)."""
        return self._model.plc

    def get_index_group(self) -> int:
        """Return the group index (owned by model)."""
        return self._model.object_id

    def get_symbols_recursive(self) -> List[Symbol]:
        """Recursively navigate subblocks and collect all parameters and signals."""
        for *_, parameter in self._parameters.items():
            yield parameter
        for *_, signal in self._signals.items():
            yield signal
        for *_, subblock in self._subblocks.items():
            for sub_symbol in subblock.get_symbols_recursive():
                yield sub_symbol

    def print_structure(self, max_depth: Optional[int] = 3, depth: int = 0):
        """Recursively print the child signals and parameters of this block.

        Use this to test your model from the command line.

        :param max_depth: Max recursion depth (set to None for infinite)
        :param depth: Current depth (do not use this argument, it's used internally)
        """

        # Get indentation
        indent = " " * depth * 8

        # Block / model itself
        print(indent, self.name, "(" + type(self).__name__ + ")")

        # Parameters
        for name, parameter in self._parameters.items():
            print(indent, "   + ", name, "(" + parameter.symbol_type + ")")

        # Signals
        for name, signal in self._signals.items():
            print(
                indent, "   * ", name, "(" + signal.name + ",", signal.symbol_type + ")"
            )

        # Do subblocks if depth allows it
        if max_depth is None or depth < max_depth:
            for *_, subblock in self._subblocks.items():
                print()  # Empty line
                subblock.print_structure(max_depth, depth=depth + 1)

        # Print ellipsis if cut off by max_depth
        elif max_depth is not None and depth >= max_depth:
            if self._subblocks:
                print(" " * (depth + 1) * 8, "...")

    def __getattr__(self, item: str) -> Union[SimulinkBlock, Symbol]:
        """Magic method, executed when an addressed property does not exist.

        When a property does not exist, we think it might be a subblock and it
        will be retrieved from self._subblocks, or a symbol and it will be
        retrieved from self._signals or self._parameters.

        :param item: The requested item
        :return:
        """

        if item in ["_subblocks", "_parameters", "_signals"]:
            raise RuntimeError(
                "Tried to find `{}` with __getattr__, "
                "this should not happen".format(item)
            )

        if hasattr(self, "_subblocks") and item in self._subblocks:
            return self._subblocks[item]
        if hasattr(self, "_parameters") and item in self._parameters:
            return self._parameters[item]
        if hasattr(self, "_signals") and item in self._signals:
            return self._signals[item]
        raise AttributeError(
            "The current block `{0}` has no property, "
            "subblock, parameter or signal named `{1}`".format(self.name, item)
        )

    def __dir__(self):
        """Method to show internals.

        Used to help autocompletion with our hidden subblocks and symbols.
        We override this to show the subblocks and symbols accessed through
        __getattr__.
        """

        return (
            list(super().__dir__())
            + list(self._subblocks.keys())
            + list(self._parameters.keys())
            + list(self._signals.keys())
        )

    def __len__(self):
        """Result of len(object)."""
        return len(self._subblocks) + len(self._parameters) + len(self._signals)

    def __iter__(self):
        """Make hidden properties iterable."""
        return self._subblocks.__iter__()

    def __getitem__(self, key):
        """Allow the [...] notation."""
        return self.__getattr__(key)

    def __repr__(self):
        """Debug print."""
        return "<%s instance at %s>, name: %s (type: %s)" % (
            self.__class__.__name__,
            id(self),
            self.name,
            self.type,
        )


class SimulinkModel(SimulinkBlock):
    """Wrapper for a compiled Simulink model in TwinCAT.

    The model is built using the XML file, created when the model is compiled.
    Therefore the model can be loaded without TwinCAT running.

    This model object is actually an extension of a SimulinkBlock. The complete
    model is basically just the root block.
    """

    def __init__(self, object_id: int, object_name: str, type_name: str = None):
        """

        By default the `TWINCAT3DIR` environment variable is used to locate the TwinCAT
        installation and look for the installed compiled XML files.

        To work around this, you can pass either of the following to `type_name`:

        * A single name (`TWINCAT3DIR` will be used)
        * A path to a directory (default XML file name will be
          searched)
        * A path to the XML file, typically named like `*_ModuleInfo.xml` (no
          searching will be done)

        :param object_id: ID of the TcCOM object in TwinCAt (the symbol group
                          index)
        :param object_name: Object Name (as shown in TwinCAT)
        :param type_name: Type name (as shown in TwinCAT) (defaults
                          to be the same as object_name).
        """

        if type_name is None:
            type_name = object_name
        self.type_name = type_name

        xml_root = self.get_xml_data(self.type_name)

        # The 'DefaultValues' branch contains an un-indexed list of standard
        # properties
        self.build_timestamp = None
        self.module_info = self.get_module_info(
            xml_root.find("ModuleInfo/DefaultValues")
        )

        self.plc: Optional[TwincatConnection] = None
        # Nothing connected by default

        # Actual structure starts here
        block_diagram = xml_root.find("ModuleInfo/BlockDiagram")

        self.object_id = object_id

        # Use super class to build the root block and the children (recursive)
        super().__init__(block_diagram, self)
        # Pass `self` as the model to follow the SimulinkBlock pattern

        self.name = object_name  # The super constructor will write an incorrect
        # name, replace it with the passed name

    @staticmethod
    def get_xml_data(type_name: str) -> ElementTree.Element:
        """Find and parse model XML file.

        The block diagram is returned.
        """

        user_path = os.path.realpath(type_name)

        if os.path.isfile(user_path):
            filepath = user_path
        else:
            if os.path.isdir(user_path):
                module_dir = user_path
            else:
                module_dir = os.path.join(
                    os.getenv("TWINCAT3DIR", "C:/TwinCAT/3.1/"),
                    "CustomConfig/Modules",
                    type_name,
                )

            dir_name = os.path.basename(os.path.normpath(user_path))  # Find the
            # name of the last directory in the path (this will be the name of
            # the XML file)

            filename = FILENAME_TEMPLATE.format(dir_name)
            filepath = os.path.join(module_dir, "deploy", filename)

            if not os.path.isfile(filepath):
                # Older TwinCAT versions have not yet added a `deploy` directory
                filepath = os.path.join(module_dir, filename)

        try:
            xml_root = ElementTree.parse(filepath).getroot()
        except FileNotFoundError as err:
            raise FileNotFoundError(
                "XML file belonging to Simulink model could not be found at "
                "`{}` (also not in the `deploy` subdirectory)! Is the "
                "type_name correct? Was the default module location "
                "used?".format(filepath)
            ) from err

        return xml_root

    @staticmethod
    def get_module_info(xmltree: ElementTree.Element) -> dict:
        """Get dictionary of module info fields.

        The `DefaultValues` section is a list of names and values, this method
        creates a regular dict from it.
        """

        values = {}

        for value_xml in xmltree:
            name_xml = value_xml.find("Name")

            if name_xml is None or not name_xml.text.startswith("ModuleInfo."):
                continue  # Skip this one

            key = name_xml.text[11:]
            values[key] = list(value_xml)[1].text
            # Second element (e.g. Value, GUID, EnumText) is the actual value

        return values

    def connect_to_twincat(self, connection: TwincatConnection):
        """Connect model the one running in TwinCAT.

        This will link all the symbols in the model to actual ADS symbols. And
        the remote model is compared to the local .xml file through
        the model checksum.

        :param connection: Connection object to connect through
        """
        remote_info = connection.get_module_info(module_name=self.name)

        remote_checksum = remote_info["ModelCheckSum"]
        # Checksum in TwinCAT is displayed signed
        for i, val in enumerate(remote_checksum):
            if val < 0:
                remote_checksum[i] += 2 ** 32  # Convert signed to unsigned

        # Checksum in XML is displayed unsigned
        model_checksum = [
            int(self.module_info["ModelCheckSum[%i]" % i]) for i in range(4)
        ]

        if model_checksum != remote_checksum:
            # raise RuntimeError(
            warnings.warn(
                "The model `{0}` checksum does not match with the "
                "online version. Maybe both rebuild and reload "
                "the model?".format(self.name),
                RuntimeWarning,
            )

        # Every symbol needs a references to the connection object
        self.plc = connection

        # Test connection with the first symbol that was found
        for symbol in self.get_symbols_recursive():
            symbol.set_connection(connection)

    def get_plc(self) -> Optional[TwincatConnection]:
        return self.plc

    def get_index_group(self) -> int:
        return self.object_id

    def __repr__(self):
        """Debug print."""
        return "<%s instance at %s>, model name: %s" % (
            self.__class__.__name__,
            id(self),
            self.name,
        )

    def __dir__(self):
        """List of properties (autocomplete helper), based on super method."""

        return ["type_name", "object_id", "module_info"] + super().__dir__()
