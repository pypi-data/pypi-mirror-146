"""TwinCAT widgets are Qt elements that are easily linked to an ADS symbol.

E.g. a label that shows an output value or an input box which changes a
parameter.

The `@pyqtSlot()` is Qt decorator. In many cases it is not essential, but
it's good practice to add it anyway.
"""

from typing import Optional, Any, Tuple, Union, Callable, List
from abc import ABC, ABCMeta, abstractmethod
import os
import time
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QAbstractButton,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QSlider,
)
from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QIcon
from .custom_widgets import GraphWidget

from ..twincat.symbols import Symbol


PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__) + "/../..")


class QABCMeta(ABCMeta, type(QWidget)):
    """Create a meta class that combines ABC and the Qt meta class."""


class Color:  # pylint: disable=too-few-public-methods
    """Collection of useful colours."""

    DEFAULT = "#FFFFFF"  # White
    EDITING = "#FFFFAA"  # Yellow-ish


class TcWidget(ABC, metaclass=QABCMeta):
    """Abstract class, to be multi-inherited together with a Qt item.

    There are different event types, which determine how and when new remote
    values are retrieved:

        * `EVENT_NOTIFICATION`: An ADS notification is created, resulting in a
          callback on a remote value change. Suitable for rarely changing values or
          when a very quick response is needed.
          ADS notifications have some overhead. No more than 200 symbol
          notifications should exist at the same time.
        * `EVENT_TIMER`: New values are read at a fixed interval. Useful when
          remote values change often but no instant response is needed. This
          method has very little overhead.
        * `EVENT_NONE`: No attempts are made to update according to remote values.

    You can override the defaults for your entire project by changing the
    ``TcWidget.DEFAULT_EVENT_TYPE`` and ``TcWidget.DEFAULT_UPDATE_FREQ``
    class properties. Make sure to update these before any widgets are
    created and they will have new standard values.

    :cvar DEFAULT_EVENT_TYPE: (default: EVENT_NOTIFICATION)
    :cvar DEFAULT_UPDATE_FREQ: (default: 10.0 Hz)
    """

    EVENT_NOTIFICATION = "notification"
    EVENT_TIMER = "timer"
    EVENT_NONE = "none"

    DEFAULT_EVENT_TYPE = EVENT_NOTIFICATION
    DEFAULT_UPDATE_FREQ = 10.0  # Hz

    def __init__(self, *args, **kwargs):
        """

        It is important to call this init() as late as possible from a
        subclass! The order should be:

           1. Subclass specific stuff (e.g. number formatting)
           2. Call to super().__init__(...) - Now the QWidget stuff has been
              made ready
           3. QWidget related stuff

        Note: these methods do not affect when or how a value is _written_ to the ADS
        pool.

        :param args:
        :param kwargs: See list below - kwargs are passed along to
            `connect_symbol` too

        :kwargs:
            * `symbol`: ``Symbol`` to link to
                        (i.e. to read from and/or write to)
            * `format`: Formatter symbol, e.g. '%.1f' or '%d' or callable
                        ('%.3f' by default, ignored when not relevant)
                        Callable must have a single argument
            * `event_type`:     Possible values are EVENT_* constants
                                (default: ``DEFAULT_EVENT_TYPE``)
            * `update_freq`:    Frequency (Hz) for timed update
                                (for EVENT_TIMER only, default: ``DEFAULT_UPDATE_FREQ``)
            * `greyed`:         When true, the widget is visibly disabled
                                When false, the widget is shown normally even when
                                disconnected (default: `true`)

        """

        self._symbol: Optional[Symbol] = kwargs.pop("symbol", None)
        # Included None fallback

        self.value_format: Union[str, Callable[[Any], str]] = kwargs.pop(
            "format", "%.3f"
        )

        self.event_type = kwargs.pop("event_type", self.DEFAULT_EVENT_TYPE)

        self.update_freq = kwargs.pop("update_freq", self.DEFAULT_UPDATE_FREQ)

        self.greyed = kwargs.pop("greyed", True)

        self._handles: Optional[Tuple[int, int]] = None
        # Handles to the notification specific for this widget

        self._skip_event: bool = False  # If true, QWidget events should not result in
        # a change of the ADS symbol

        self._last_update: Optional[float] = None  # Timestamp of the last successful
        # twincat_send(), used to prevent an event loop

        self._timer: Optional[QTimer] = None  # For timed event loop
        self._last_value: Optional[Any] = None  # For timed event loop

        # Disable widget
        if self.greyed:
            self.setDisabled(True)

        if self._symbol:
            self.connect_symbol(self._symbol, **kwargs)
            # Connect already if passed

    def connect_symbol(self, new_symbol: Optional[Symbol] = None, **kwargs):
        """Connect a symbol (copy is left as property).

        By default a device callback is created with an on-change event
        from TwinCAT.
        Old callbacks are deleted first. Pass None to only clear callbacks.
        The notification handles are stored locally.
        Extend (= override but call the parent first) this method to
        configure more of the widget, useful if e.g. widget callbacks depend
        on the symbol.

        :param new_symbol: Symbol to link to (set None to only clear the
            previous)
        :param kwargs: See list below - Keyword arguments are passed along as
            device notification settings too

        :kwargs:
            * `event_type`:     See :class:`TcWidget`
            * `update_freq`:    See :class:`TcWidget`
        """

        if self._handles is not None and self._symbol is not None:
            self._symbol.del_device_notification(self._handles)
            # In case previous callback existed, clear it
            self._handles = None

        self._timer = None  # Destroy old timer

        self._symbol = new_symbol

        if "event_type" in kwargs:
            self.event_type = kwargs.pop("event_type")
        if "update_freq" in kwargs:
            self.update_freq = kwargs.pop("update_freq")

        if new_symbol is None:
            if self.greyed:
                self.setDisabled(True)
        else:
            connected = True  # New connected state
            if self.event_type == self.EVENT_NOTIFICATION:
                self._handles = self._symbol.add_device_notification(
                    self.twincat_receive_wrapper, **kwargs
                )
                # It seems a notification is always fired on creation, so we don't
                # need to call it now
                if self._handles is None:  # In case the callback quietly failed
                    connected = False
            elif self.event_type == self.EVENT_TIMER:
                self._timer = QTimer()
                self._timer.timeout.connect(self.on_timeout)
                m_sec = int(1000 / self.update_freq)
                self._timer.start(m_sec)
            elif self.event_type == self.EVENT_NONE:
                pass  # Nothing to be done
            else:
                ValueError("Unrecognized event type: " + self.event_type)

            if self.greyed and connected:
                self.setDisabled(False)

    def twincat_receive_wrapper(self, value):
        """Intermediate twincat_receive callback to prevent event loops."""

        # If incoming value equals old buffered value
        if value == self._symbol.value and self._last_update is not None:

            elapsed_ms = (time.time() - self._last_update) * 1000
            if elapsed_ms < 50:
                # If within 50 ms of the last update, discard this notification
                # This is typically a callback after a twincat_send()
                return

        self.twincat_receive(value)

    @pyqtSlot()
    def on_timeout(self):
        """Callback for the event timer."""
        # We cannot use the buffered _symbol.value, since it could have been updated
        # outside this widget instance.
        new_val = self._symbol.read()
        if new_val != self._last_value:
            # Trigger incoming-value callback
            self.twincat_receive(new_val)
            self._last_value = new_val

    @abstractmethod
    def twincat_receive(self, value):
        """Callback attached to the TwinCAT symbol.

        Note: changing a state of a widget (e.g. checkbox being checked through
        `setChecked(True)`) will typically fire the on-change events again. So be
        careful to prevent an event loop when updating a widget based on a remote
        change: a change could result in a state change, which could result in a
        remote change, etc.

        :param value: New remote value
        """

    def twincat_send(self, value: Any):
        """Set value in symbol (and send to TwinCAT).

        Method is safe: if symbol is not connected, nothing will happen.
        """
        self._last_update = time.time()  # Current floating point timestamp

        if self._symbol is not None:  # Safe for unconnected symbols
            self._symbol.set(value)

    def format(self, value: Any) -> str:
        """ "Use the stored formatting to created a formatted text.

        In case the format specifier is a string and the new value is a list,
        element-wise string formatting will be concatenated automatically.
        """
        if isinstance(self.value_format, str):
            if isinstance(value, list):
                elements = [self.value_format % item for item in value]
                return ", ".join(elements)

            return self.value_format % value

        if callable(self.value_format):
            return self.value_format(value)

        raise NotImplementedError(
            "The format `{}` could not be processed".format(self.value_format)
        )

    def __del__(self):
        """Destructor."""

        if self._symbol is not None:
            # Element is about to become extinct, so clear callbacks
            self._symbol.clear_device_notifications()


class TcLabel(QLabel, TcWidget):
    """Label that shows a value."""

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: See :class:`TcWidget`
        """

        super().__init__(*args, **kwargs)  # Both constructors will be called

        # Prevent it being empty from the start
        if self._symbol is None and not self.text():
            self.setText("NaN")  # Default value

        # Give the label a frame to visually indicate it is not static
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)

    def twincat_receive(self, value):
        self.setText(self.format(value))


class TcLineEdit(QLineEdit, TcWidget):
    """Readable and writable input box."""

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs: See :class:`TcWidget`
        """

        super().__init__(*args, **kwargs)  # Both constructors will be called

        self.textEdited.connect(self.on_text_edited)
        self.editingFinished.connect(self.on_editing_finished)

        self.setStyleSheet("background-color:" + Color.DEFAULT)

    def twincat_receive(self, value) -> Any:
        self.setText(self.format(value))
        # `setText` does not fire the `editingFinished` signal

    @pyqtSlot()
    def on_editing_finished(self):
        """Called when [Enter] is pressed or box loses focus."""

        self.setStyleSheet("background-color:" + Color.DEFAULT)

        value = self.text()
        self.twincat_send(value)

    @pyqtSlot(str)
    def on_text_edited(self, *_value):
        """Callback when text was modified (i.e. on key press)."""
        self.setStyleSheet("background-color:" + Color.EDITING)


class TcPushButton(QPushButton, TcWidget):
    """Button that sends value when button is held pressed."""

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:

        :kwargs:
            * `value_pressed`: Value on press (default: 1), None for no action
            * `value_released`: Value on release (default: 0), None for no action
            * See :class:`TcWidget`
        """

        self.value_pressed = kwargs.pop("value_pressed", 1)
        self.value_released = kwargs.pop("value_released", 0)

        super().__init__(*args, **kwargs)

        if self.value_pressed is not None:
            self.pressed.connect(self.on_pressed)
        if self.value_released is not None:
            self.released.connect(self.on_released)

    @pyqtSlot()
    def on_pressed(self):
        """Callback on pressing button."""
        self.twincat_send(self.value_pressed)

    @pyqtSlot()
    def on_released(self):
        """Callback on releasing button."""
        self.twincat_send(self.value_released)

    def twincat_receive(self, value):
        """Do nothing, method requires definition anyway."""


class TcRadioButton(QRadioButton, TcWidget):
    """Radiobutton that updates the symbol when it is selected.

    The radiobutton will _not_ update the symbol when another selection is made.
    Instead a write could be performed if that other radio is also a TcWidget.

    Use :class:`TcRadioButtonGroupBox` instead to create a set of radio buttons together
    that all update the same ADS symbol.

    When connecting to a boolean symbol, use 0 and 1 as values for the best result
    instead of `True` and `False`.

    Radios need to be in a QButtonGroup together to link together.
    """

    def __init__(self, *args, **kwargs):
        """

        :param label: Label of this radio button
        :type label: str
        :param args:
        :param kwargs:

        :kwargs:
            * `value_checked`: Value when radio becomes checked (default: 1)
            * See :class:`TcWidget`
        """

        self.value_checked = kwargs.pop("value_checked", 1)

        super().__init__(*args, **kwargs)

        self.toggled.connect(self.on_toggled)

    @pyqtSlot()
    def on_toggled(self):
        """Callback when radio state is togged (either checked or unchecked)."""

        if self.isChecked():
            self.twincat_send(self.value_checked)
        # Do nothing when the radio became unchecked

    def twincat_receive(self, value):
        """Set checked state if the new value is equal to the is-checked value."""

        self.blockSignals(True)  # Prevent calling `on_toggled` based on a remote
        # change

        # Become checked or unchecked
        self.setChecked(value == self.value_checked)
        # Note: this could result in no radio being checked at all

        self.blockSignals(False)


class TcRadioButtonGroupBox(QGroupBox, TcWidget):
    """An instance on this class forms a group of radio buttons.

    The group of radio buttons together control a single ADS variable.

    Instances of `QRadioButton` will be automatically created through this
    class. Using literal instances of `TcRadioButton` is not efficient because of
    duplicate callbacks.

    When the remote value changes to a value that is not listed as an option in the
    radio_toggle, the displayed value simply won't change at all.
    """

    def __init__(self, *args, **kwargs):
        """

        The `options` argument is required.

        :param title: Title of this QGroupBox
        :type title: str
        :param args:
        :param kwargs:

        :kwargs:
            * `options`: List of tuples that form the label-value pairs of the radio,
                         e.g. `[('Low Velocity', 0.5), ('High Velocity', 3.0)]`
            * `layout_class`: Class of the layout used inside the QGroupBox (default:
                              `QVBoxLayout`)
            * See :class:`TcWidget`
        """

        options = kwargs.pop("options")

        self.button_group = QButtonGroup()  # Use Button group to connect radio_toggle

        layout_class = kwargs.pop("layout_class", QVBoxLayout)
        self.button_layout = layout_class()  # Use button_layout to add buttons

        self.radio_buttons: List[QRadioButton] = []
        self.values: List = []

        for i, option in enumerate(options):
            radio = QRadioButton(option[0])
            self.button_layout.addWidget(radio)
            self.button_group.addButton(radio)
            # Give radios an increment id so we can identify them later
            self.button_group.setId(radio, i)
            self.radio_buttons.append(radio)
            self.values.append(option[1])

        super().__init__(*args, **kwargs)

        self.button_group.buttonClicked.connect(self.on_click)

        self.setLayout(self.button_layout)  # Must be done _after_ the parent
        # constructor was called

    @pyqtSlot(QAbstractButton)
    def on_click(self, button: QAbstractButton):
        """Callback when a button of the group was pressed."""
        i = self.button_group.id(button)
        value = self.values[i]
        self.twincat_send(value)

    def twincat_receive(self, value):
        """Callback for a remote value change."""

        for i, radio_value in enumerate(self.values):
            # Update checked status (allow for multiple checks in case of duplicate
            # options)
            self.radio_buttons[i].setChecked(radio_value == value)
            # `radio_button.setChecked` won't fire a relevant event


class TcCheckBox(QCheckBox, TcWidget):
    """Checkbox to control a symbol."""

    def __init__(self, *args, **kwargs):
        """
        Set either value to `None` to send nothing on that state.
        For the best results, use 1 and 0 for a boolean variable instead of `True`
        and `False`.

        :param label: Label of this radio button
        :type label: str
        :param args:
        :param kwargs:

        :kwargs:
            * `value_checked`: Value when checkbox becomes checked (default: 1)
            * `value_unchecked`: Value when checkbox becomes unchecked (default: 0)
            * See :class:`TcWidget`
        """

        self.value_checked = kwargs.pop("value_checked", 1)
        self.value_unchecked = kwargs.pop("value_checked", 0)

        super().__init__(*args, **kwargs)

        self.toggled.connect(self.on_toggled)

    @pyqtSlot()
    def on_toggled(self):
        """Callback when box state is togged (either checked or unchecked)."""

        if self.isChecked():
            if self.value_checked is not None:
                self.twincat_send(self.value_checked)
        else:
            if self.value_unchecked is not None:
                self.twincat_send(self.value_unchecked)

    def twincat_receive(self, value):
        """Set checked state if the new value is equal to the is-checked value."""

        self.blockSignals(True)  # Prevent calling `on_toggled` based on a remote
        # change

        # Become checked or unchecked
        self.setChecked(value == self.value_checked)
        # Note: this could result in no radio being checked at

        self.blockSignals(False)


class TcSlider(QWidget, TcWidget):
    """Interactive slider.

    Also has built-in slider numbers (unlike the basic QSlider).
    This class extends a plain widget so a layout can be added for any labels.

    The basic QSlider only supports integer values. To support floating point
    numbers too, the slider values are multiplied by a scale (e.g. 100) when writing,
    and divided again when reading from the slider.
    Use this with the `float` and `float_scale` options. This is done automatically if
    `interval` is not an integer.

    :ivar slider: QSlider instance
    """

    def __init__(self, *args, **kwargs):
        """

        :param orientation: Either `QtCore.Qt.Horizontal` (default) or `Vertical`
        :param args:
        :param kwargs:

        :kwargs:
            * `min`: Slider minimum value (default: 0)
            * `max`: Slider maximum value (default: 100)
            * `interval`: Slider interval step size (default: 1)
            * `show_labels`: When true (default), show the min and max values with
                             labels
            * `show_value`: When true (default), show the current slider value with a
                            label
            * `float`: When true, QSlider values are scaled to suit floats (default:
                       False)
            * `float_scale`: Factor between QSlider values and real values (default:
                             100)
            * See :class:`TcWidget`
        """

        orientation = kwargs.pop("orientation", Qt.Horizontal)
        range_min = kwargs.pop("min", 0)
        range_max = kwargs.pop("max", 100)
        interval = kwargs.pop("interval", 1)
        show_labels = kwargs.pop("show_labels", True)
        show_value = kwargs.pop("show_value", True)
        self.float: bool = kwargs.pop("float", isinstance(interval, float))
        self.float_scale: float = kwargs.pop("float_scale", 1.0 / interval)

        if range_min > range_max:
            raise ValueError("Slider minimum cannot be bigger than the maximum")

        if interval > abs(range_max - range_min):
            raise ValueError("Interval is bigger than the space between min and max")

        self.slider = QSlider(orientation=orientation)  # Create the real slider
        self.slider.setRange(
            self.value_to_slider(range_min), self.value_to_slider(range_max)
        )
        ticks = self.value_to_slider(interval)
        self.slider.setTickInterval(ticks)
        self.slider.setSingleStep(ticks)
        self.slider.setPageStep(ticks * 5)

        if range_min > range_max:
            self.slider.setInvertedAppearance(True)

        super().__init__(*args, **kwargs)  # Both constructors will be called

        self.label_min = QLabel(str(range_min))
        self.label_max = QLabel(str(range_max))
        self.label_value = QLabel("NaN")

        if orientation == Qt.Horizontal:
            self.layout_slider = QVBoxLayout(self)  # Create a layout for this widget
            self.layout_labels = QHBoxLayout()

            alignment_min = Qt.AlignLeft
            alignment_max = Qt.AlignRight
        else:
            self.layout_slider = QHBoxLayout(self)  # Create a layout for this widget
            self.layout_labels = QVBoxLayout()

            alignment_min = Qt.AlignBottom
            alignment_max = Qt.AlignTop  # Vertical slider has max at the top

        self.label_min.setAlignment(alignment_min)
        self.label_max.setAlignment(alignment_max)
        self.label_value.setAlignment(Qt.AlignCenter)

        self.layout_slider.setContentsMargins(0, 0, 0, 0)
        self.layout_labels.setContentsMargins(0, 0, 0, 0)
        self.layout_labels.setSpacing(0)

        if orientation == Qt.Horizontal:
            self.layout_labels.addWidget(self.label_min, alignment_min)
            self.layout_slider.addStretch()
            self.layout_labels.addWidget(self.label_value, Qt.AlignCenter)
            self.layout_slider.addStretch()
            self.layout_labels.addWidget(self.label_max, alignment_max)
        else:
            # For a vertical QSlider the top value is the max
            self.layout_labels.addWidget(self.label_max, alignment_max)
            self.layout_slider.addStretch()
            self.layout_labels.addWidget(self.label_value, Qt.AlignCenter)
            self.layout_slider.addStretch()
            self.layout_labels.addWidget(self.label_min, alignment_min)

        self.layout_slider.addWidget(self.slider)
        self.layout_slider.addLayout(self.layout_labels)

        if not show_labels:
            self.label_min.hide()
            self.label_max.hide()

        if not show_value:
            self.label_value.hide()

        # Events
        self.slider.valueChanged.connect(self.on_value_changed)
        # Note: the event will be triggered while the user is dragging

    def slider_to_value(self, value: int) -> Union[float, int]:
        if not self.float:
            return value
        return value / self.float_scale

    def value_to_slider(self, value: float) -> Union[int, float]:
        if not self.float:
            return round(value)
        return round(value * self.float_scale)

    @pyqtSlot(int)
    def on_value_changed(self, new_value):
        """Callback when the slider was changed by the user."""

        real_value = self.slider_to_value(new_value)
        self.twincat_send(real_value)

    def twincat_receive(self, value) -> Any:
        """On remote value change.

        This will be triggered by `on_value_changed` too. A small timeout is added to
        prevent a loop between the two callbacks, received changes right after a user
        change are ignored.
        """

        label_txt = "%.3f" % value if self.float else str(value)
        self.label_value.setText(label_txt)

        slider_value = self.value_to_slider(value)

        self.slider.blockSignals(True)  # Prevent calling `on_value_changed`
        # based on a remote change

        self.slider.setValue(slider_value)

        self.slider.blockSignals(False)


class TcGraph(GraphWidget, TcWidget):
    """Draw rolling graph of symbol values.

    TcGraph works only well with `EVENT_TIMER`!

    The graph refresh rate is limited to self.FPS, while data is being requested at
    `update_freq`.
    For research measurements, use a log file or a TwinCAT measurement project
    instead. Even with a high `update_freq` there is no guarantee all data is captured!
    """

    def __init__(self, *args, **kwargs):
        """

        If no symbol for the x-axis is selected, the local time will be used instead.
        Note that due to how PyQt events are handled, the local time can be slightly
        warped with respect the ADS symbol values.

        See :class:`GraphWidget` for more options.

        :param args:
        :param kwargs:

        :kwargs:
            * `symbols`: List of symbols to plot (for the y-axis)
            * `symbol_x`: Symbol to use on the x-axis (optional)
        """

        self._symbol: Optional[List[Symbol]] = None

        # Handle symbols
        if "symbols" in kwargs:
            kwargs["symbol"] = kwargs.pop("symbols")

        self.symbol_x: Optional[Symbol] = kwargs.pop("symbol_x", None)

        # Other properties
        kwargs.setdefault("event_type", self.EVENT_TIMER)
        if "labels" not in kwargs:
            kwargs["labels"] = [symbol.name for symbol in kwargs["symbol"]]

        if kwargs["event_type"] != self.EVENT_TIMER:
            raise ValueError("TcGraph can only work with EVENT_TIMER!")

        super().__init__(*args, **kwargs)

    def connect_symbol(
            self,
            new_symbol: Optional[Union[Symbol, List[Symbol]]] = None,
            **kwargs,
    ):
        """Connect to list of symbols (override)."""

        if "new_symbols" in kwargs:
            new_symbol = kwargs.pop("new_symbols")

        # Force to list
        if new_symbol is not None and not isinstance(new_symbol, list):
            new_symbol = [new_symbol]

        super().connect_symbol(new_symbol, **kwargs)

    @pyqtSlot()
    def on_timeout(self):
        """Callback for the event timer (override)."""

        values = [symbol.read() for symbol in self._symbol]

        value_x = self.symbol_x.read() if self.symbol_x is not None else None

        self.add_data(values, value_x)

    def twincat_receive(self, value):
        """Abstract implementation.

        All useful code is in on_timeout() instead.
        """
        pass

    def __del__(self):
        """Destructor."""

        # Parent destructor will try to remove notifications, which won't work since
        # the _symbol property can be a list
        self._symbol = None  # No further destruction needed with EVENT_TIMER.
        super().__del__()


class TcMainWindow(QMainWindow):
    """Parent class for TwinCAT GUIs.

    Extends QMainWindow. The resulting window is empty, but will have a
    destructor that neatly closes any TcWidgets first.

    To make it easier to navigate the different elements, adhere to:

    * Create objects as late as possible
    * Save objects as property only if that is really necessary
    * Name objects by elements starting with the most general item
      (e.g. 'layout_group_drives')
    * To save space, create a Layout directly with its parent widget:

            `button_layout = QLayout(widget_parent)`

            `# widget_parent.addLayout(button_layout)  # < Not needed now`

    Widgets consist of layouts. Layouts contain widgets.
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.setWindowTitle("TwinCAT GUI")

        icon_path = os.path.join(PACKAGE_DIR, "resources/icon.ico")
        self.setWindowIcon(QIcon(icon_path))

    def find_tc_widgets(self) -> List[TcWidget]:
        """Find all children of the TcWidget type (recursively)."""
        for widget in self.findChildren(TcWidget):
            yield widget

    def closeEvent(self, event):
        """On window close."""

        # An error will occur when a callback is fired to a widget that has
        # already been removed, so on the closing of the window we make sure
        # to clear callbacks to TcWidgets
        for widget in self.find_tc_widgets():
            widget.connect_symbol(None)

        super().closeEvent(event)  # Continue to parent event handler
