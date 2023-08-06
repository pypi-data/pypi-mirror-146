"""These widgets are specific implementations of TcWidgets.

They are not intended to be overridden again. They are separate classes mostly
because their specific logic became significant.
"""

from typing import List, Optional
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
    QHBoxLayout,
)
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtMultimedia import QSound

from .tc_widgets import PACKAGE_DIR, TcLabel, TcPushButton
from .custom_widgets import ScrollLabel
from ..twincat.simulink import SimulinkModel


class TcErrorsLabel(TcLabel):
    """Extension of TcLabel for a list of joint errors.

    This is separate class because the amount of logic got a little bit much.

    When clicking on the widget, a new window pops up showing the decoded errors.
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:

        :kwargs:
            * `format`: Callback to format errors
                        (default: show hexadecimal representation of error values)
            * `popup`:  Whether or not to enable a detailed popup window
                        (default: True)
            * `play_sound`:     When True, play a beep sound on a new error
                                (default: False)
            * See :class:`TcLabel`
        """

        # Use local format function (neatly attached to format callback)
        if "format" not in kwargs:
            kwargs["format"] = self.format_errors_list

        self.popup_window: Optional[ErrorPopupWindow] = None
        if kwargs.pop("popup", True):
            self.popup_window = ErrorPopupWindow()

        self.sound: Optional[QSound] = None
        if kwargs.pop("play_sound", False):
            self.sound = QSound(os.path.join(PACKAGE_DIR, "resources", "error.wav"))
        self.has_error = True  # If any error is present (True at the start to
        # prevent a beep when the GUI is started)

        super().__init__(*args, **kwargs)

        self.setTextFormat(Qt.RichText)  # Allow HTML-like tags

    def twincat_receive(self, value):
        """Callback on remote value change."""

        # In case only a single actuator is used, the incoming value might not be an
        # array, so convert it
        if isinstance(value, int):
            value = [value]

        if self.popup_window is not None:
            # Update window content
            self.popup_window.update_content(value)

        # Play an error sound when needed (note: negative when not in use)
        has_error = any(v > 0 for v in value)
        if self.sound is not None:  # If enabled in settings
            if has_error and not self.has_error:  # If there is a new error
                self.sound.play()

        self.has_error = has_error

        # Base method does a great job already:
        super().twincat_receive(value)

    @staticmethod
    def format_errors_list(error_list: List[int]) -> str:
        """Set text for errors label."""

        text = ""

        for error in error_list:
            if text:
                text += "<br>"  # In rich text, use HTML break instead of \n

            code = TcErrorsLabel.to_hex(error)

            if error > 0:
                line = "<font color=red><b>" + code + "</b></font>"
            else:
                line = "<font color=grey>" + code + "</font>"

            text += line

        return text

    @staticmethod
    def to_hex(value: int) -> str:
        """Create human-readable hex from integer."""

        code = hex(abs(value)).upper()[2:].rjust(8, "0")

        code = code[0:4] + " " + code[4:]  # Add a space for readability

        return code

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """On clicking on the label.

        QLabel does not have an on-click signal already.
        """

        win = self.popup_window  # Create shortcut reference
        if win is not None:
            win.show()
            win.activateWindow()
            win.setWindowState(
                int(win.windowState()) & ~Qt.WindowMinimized | Qt.WindowActive
            )

        super().mousePressEvent(event)


class ErrorPopupWindow(QWidget):
    """Popup window for drive error details.

    It's meant to only be instantiated by :class:`TcErrorsLabel`.

    This window does not attach it's own ADS callbacks. Instead it must be called
    by another widget that does.
    """

    ERROR_DESCRIPTIONS = [
        "ActuatorNotInUse",
        "Slave offline",
        "Motor angle guard",
        "JointAngle position guard",
        "Spring deflection guard",
        "Torque guard",
        "Motor encoder frozen",
        "Joint encoder frozen",
        "Spring encoder frozen",
        "Encoder consistency",
        "FromToActuator consistency",
        "Drive went off without error",
        "STO active (with or without Stop button)",
        "Motor overvoltage",
        "Motor undervoltage",
        "Drive over/under-temperature",
        "Motor overtemperature",
        "Overcurrent/Short circuit error (drive limit)",
        "Overcurrent (user limit)",
        "I2t error",
        "Position out of range detected by drive",
        "Velocity out of range detected by drive",
        "Drive communications watchdog error",
        "Too many encoder read errors",
        "Drive external fault",
        "Drive configuration error",
        "Drive electronics problem",
        "Other drive error (see LastError register)",
    ]

    JOINTS = ["LHA", "LHF", "LK", "LA", "RHA", "RHF", "RK", "RA"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setWindowTitle("Drive Errors")

        # Create read-only label and make it the main thing
        self.label = ScrollLabel()

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.label)

    def update_content(self, error_list):
        """Set the window content based on a new errors list."""

        text = ""

        for i, error in enumerate(error_list):
            if text:
                text += "<br>"  # In rich text, use HTML break instead of \n

            text += "<u>" + self.JOINTS[i] + "</u>: &nbsp;"

            code = TcErrorsLabel.to_hex(error)

            if error > 0:
                text += "<font color=red><b>" + code + "</b></font>"
            else:
                text += "<font color=grey>" + code + "</font>"

            text += "<br>"

            for descriptions in self.get_error_descriptions(error):
                text += " - " + descriptions + "<br>"

        self.label.setText(text)

    @classmethod
    def get_error_descriptions(cls, error: int) -> List[str]:
        """Get list of decoded errors from an error code"""

        if error == 0:
            return []  # Save some effort

        descriptions = []

        for bit, description in enumerate(cls.ERROR_DESCRIPTIONS):
            # Perform bitwise check

            mask = 2 ** bit
            if error & mask:
                text = TcErrorsLabel.to_hex(mask) + " | " + description
                descriptions.append(text)

        return descriptions


class DrivesWidget(QGroupBox):
    """Group with buttons for the drives."""

    def __init__(self, actuator: Optional[SimulinkModel] = None):

        super().__init__("Drives")

        self.button_drives_enable = TcPushButton("Enable Drives")
        self.button_drives_disable = TcPushButton("Disable Drives")
        self.label_drives_enabled = TcLabel()
        self.button_calibrate = TcPushButton("Calibrate motor encoders")

        if actuator is not None:
            self.button_drives_enable.connect_symbol(
                actuator.EnableDrives.Value
            )
            self.button_drives_disable.connect_symbol(
                actuator.DisableDrives.Value
            )
            self.button_calibrate.connect_symbol(  # Typo is correct
                actuator.RecalibrateMotorEncoders.Value
            )

            # We use a manual callback for the drives instead of formatter:
            actuator.FromActuators.OperationEnabled_Read.so1.add_device_notification(
                self.on_drives_enabled_change
            )

        layout_group_drives = QVBoxLayout(self)
        layout_group_drives.addWidget(self.button_drives_enable)
        layout_group_drives.addWidget(self.button_drives_disable)
        layout_group_drives.addWidget(self.button_calibrate)
        layout_group_drives.addWidget(self.label_drives_enabled)

    def on_drives_enabled_change(self, enabled_list: List[float]):
        """An additional callback for the drive state change.

        Manual callback instead of TcWidget symbol connection so we can also
        change button state and label color.
        """

        drives_count = len(enabled_list)
        enabled_count = sum(e > 0 for e in enabled_list)

        if enabled_count == 0:
            label_text = "All drives are disabled"
            style = ""
            button_enable_on = True
            button_disable_on = False
        elif enabled_count == drives_count:
            label_text = "All drives are enabled"
            style = "background-color:#14DB4C"
            button_enable_on = False
            button_disable_on = True
        else:
            label_text = "%d out of %d drives enabled" % (enabled_count, drives_count)
            style = "background-color:#74CC8D"
            button_enable_on = True
            button_disable_on = True

        self.label_drives_enabled.setText(label_text)
        self.label_drives_enabled.setStyleSheet(style)
        self.button_drives_enable.setEnabled(button_enable_on)
        self.button_drives_disable.setEnabled(button_disable_on)


class ErrorsWidget(QWidget):
    """Widget for the current and last errors.

    Layout contains two groupboxes, and each can be clicked for a popup with more info.

    You might want to call the `close_windows()` method from inside the
    `closeEvent()` function from the main window, to close the popups when closing
    the GUI.
    """

    def __init__(self, actuator: Optional[SimulinkModel] = None):

        super().__init__()

        self.label_errors_current = TcErrorsLabel(play_sound=True)
        self.label_errors_current.popup_window.setWindowTitle("Current Errors")
        self.label_errors_last = TcErrorsLabel(play_sound=False)
        self.label_errors_last.popup_window.setWindowTitle("Last Errors")

        if actuator is not None:
            self.label_errors_current.connect_symbol(
                actuator.ToActuators.JointError_Read.so1
            )
            self.label_errors_last.connect_symbol(
                actuator.ToActuators.JointErrorLatched_Read.so1
            )

        group_errors_current = QGroupBox("Current Errors")
        group_errors_last = QGroupBox("Last Errors")

        layout_group_errors_current = QVBoxLayout(group_errors_current)
        layout_group_errors_last = QVBoxLayout(group_errors_last)
        layout_group_errors_current.addWidget(self.label_errors_current)
        layout_group_errors_last.addWidget(self.label_errors_last)

        layout_errors = QHBoxLayout(self)
        layout_errors.addWidget(group_errors_current)
        layout_errors.addWidget(group_errors_last)

    def close_windows(self):
        """Close the popup windows in case they were opened."""
        if self.label_errors_current is not None:
            if self.label_errors_current.popup_window is not None:
                self.label_errors_current.popup_window.close()

        if self.label_errors_last is not None:
            if self.label_errors_last.popup_window is not None:
                self.label_errors_last.popup_window.close()


class SystemBackpackWidget(QGroupBox):
    """Widget containing labels for the temperature and voltages.

    This widget is for the old backpack system.
    """

    def __init__(self, actuator: Optional[SimulinkModel] = None):

        super().__init__("System Info")

        self.label_battery_logic = TcLabel()
        self.label_battery_motor = TcLabel()
        self.label_temperature = TcLabel()

        if actuator is not None:
            self.label_battery_logic.connect_symbol(actuator.LogicBatteryVoltage_V.so1)
            self.label_battery_motor.connect_symbol(actuator.MotorBatteryVoltage_V.so1)
            self.label_temperature.connect_symbol(actuator.BackpackTemperature_V.so1)

        layout_group_system = QFormLayout(self)
        layout_group_system.addRow(
            QLabel("Logic Battery (V):"), self.label_battery_logic
        )
        layout_group_system.addRow(
            QLabel("Motor Battery (V):"), self.label_battery_motor
        )
        layout_group_system.addRow(
            QLabel("Backpack Temperature (C):"), self.label_temperature
        )


class SystemWRBSWidget(QGroupBox):
    """Widget containing labels for the temperature and voltages.

    This widget is for the new wearable robotics base station.
    """

    def __init__(self, actuator: Optional[SimulinkModel] = None):

        super().__init__("System Info")

        self.label_v_left = TcLabel()
        self.label_v_right = TcLabel()
        self.label_temp = TcLabel()

        if actuator is not None:
            self.label_v_left.connect_symbol(actuator.WRBS_A.V_Left.so1)
            self.label_v_right.connect_symbol(actuator.WRBS_A.V_Right.so1)
            self.label_temp.connect_symbol(actuator.WRBS_A.Temp.so1)

        layout_group_system = QFormLayout(self)
        layout_group_system.addRow(
            QLabel("Voltage Left (V):"), self.label_v_left
        )
        layout_group_system.addRow(
            QLabel("Voltage Right (V):"), self.label_v_right
        )
        layout_group_system.addRow(
            QLabel("WRBS Temperature (C):"), self.label_temp
        )
