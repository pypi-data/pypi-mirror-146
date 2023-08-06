"""Module containing the Base GUI class.

This class should be extended to make your own GUI.
"""


from typing import Optional

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTabWidget

from .tc_widgets import TcMainWindow
from .base_widgets import (
    DrivesWidget,
    ErrorsWidget,
    SystemBackpackWidget,
    SystemWRBSWidget,
)
from .tabs import PythonConsole, ConsoleTab, FirmwareTab
from ..twincat import SimulinkModel

try:
    import ctypes

    APP_NAME = "WR.BaseGui"  # Change application id to make the taskbar icon
    # displayed correctly
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_NAME)
except ImportError:
    ctypes = None  # Very unimportant fix, continue if ctypes was not found
except AttributeError:
    pass  # On Linux systems, windll is not available and will give trouble


class BaseGUI(TcMainWindow):
    """Base TwinCAT GUI, specific for the WE2 actuators and controller model.

    Extends this class if you want to use those models. For other models,
    using :class:`twinpy.ui.TcMainWindow` might be more appropriate.

    The left side of the main window consists of the basic control elements. The right
    contains a tabs widget, to which you can add your own custom tabs.

    An example of an extended GUI could be:

    .. code-block:: python

        class CustomTab(QWidget):
            # Widget containing a set of TcWidgets

        class MyGUI(BaseGUI):

            def __init__():
                super().__init__()

                self.custom_tab = CustomTab()
                # Add new tab to the existing list:
                self.tabs.addTab(custom_tab, "Custom Tab")

                # Make the custom tab the default:
                self.tabs.setCurrentWidget(self.custom_tab)


    Note: if the `pyqtconsole` package is not found, the console won't be created and
    the tabs list could be empty.

    """

    def __init__(
        self,
        actuator: Optional[SimulinkModel] = None,
        controller: Optional[SimulinkModel] = None,
        **kwargs
    ):
        """

        :param actuator: The WE2_actuators model (or a derivative)
        :param controller: The WE2_controller model (or a derivative)
        :param kwargs:
        """

        super().__init__()

        main_widget = QWidget()  # Widget spanning the entire window

        main_layout = QHBoxLayout(main_widget)

        layout_left = QVBoxLayout()  # Main button_layout

        self.tabs = QTabWidget()  # Container for tabs on the right side

        main_layout.addLayout(layout_left)
        main_layout.addWidget(self.tabs)

        self.setCentralWidget(main_widget)  # Make widget the main thingy

        if controller is not None and hasattr(controller, "Controller"):
            controller = controller.Controller  # Shorten one block

        # Drives
        self.widget_drives = DrivesWidget(actuator)
        layout_left.addWidget(self.widget_drives)

        # Errors
        self.widget_errors = ErrorsWidget(actuator)
        layout_left.addWidget(self.widget_errors)

        # Info
        system_widget_class = None
        if actuator is not None and "WRBS_A" in actuator:
            system_widget_class = SystemWRBSWidget
        elif actuator is not None and "LogicBatteryVoltage_V" in actuator:
            system_widget_class = SystemBackpackWidget

        if system_widget_class is not None:
            self.widget_system = system_widget_class(actuator)
            layout_left.addWidget(self.widget_system)

        # Tabs
        if PythonConsole is not None:
            self.tab_console = ConsoleTab(actuator, controller)
            self.tabs.addTab(self.tab_console, "Console")

        if actuator is not None and "WRBS_A" in actuator:
            self.tab_firmware = FirmwareTab(actuator)
            self.tabs.addTab(self.tab_firmware, "Firmware")

        # -------

        self.show()

    def closeEvent(self, event):
        """Callback when window is closed."""

        # Also close error popup windows, just in case
        self.widget_errors.close_windows()

        super().closeEvent(event)
