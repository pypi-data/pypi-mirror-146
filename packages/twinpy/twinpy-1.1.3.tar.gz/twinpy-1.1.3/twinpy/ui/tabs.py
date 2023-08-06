"""Module containing complete UI tabs."""

from typing import Optional

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
)

from ..twincat import SimulinkModel
from .tc_widgets import TcCheckBox

try:
    from pyqtconsole.console import PythonConsole
except ModuleNotFoundError:
    PythonConsole = None  # Make console optional


if PythonConsole is not None:

    class ConsoleTab(PythonConsole):
        """Tab with the Python console.

        The `clear()` command is available in the console.
        """

        def __init__(
            self,
            actuator: Optional[SimulinkModel] = None,
            controller: Optional[SimulinkModel] = None,
        ):

            super().__init__()

            self.push_local_ns("actuator", actuator)
            self.push_local_ns("controller", controller)

            # Make the `clear()` command available in the console
            self.interpreter.locals["clear"] = self.edit.clear

            self.eval_in_thread()

else:
    ConsoleTab = None


class FirmwareTab(QWidget):
    """Widget for the firmware CtrlWord options (Base Station only)."""

    def __init__(self, actuator: Optional[SimulinkModel] = None):
        super().__init__()

        layout_main = QVBoxLayout(self)

        layout_check = QHBoxLayout()

        group_check = QGroupBox("CtrlWord")
        group_check.setLayout(layout_check)

        self.check_sto = TcCheckBox("Enable STO")
        self.check_power_off = TcCheckBox("Power off")

        layout_check.addWidget(self.check_sto)
        layout_check.addWidget(self.check_power_off)

        layout_main.addWidget(group_check)

        if actuator is not None:
            try:
                fw = actuator.WRBS_A
                self.check_sto.connect_symbol(fw.FirmwareSTO.Value)
                self.check_power_off.connect_symbol(fw.FirmwarePowerOff.Value)
            except AttributeError:
                pass  # Ignore if properties don't exist for old backpack compatibility
