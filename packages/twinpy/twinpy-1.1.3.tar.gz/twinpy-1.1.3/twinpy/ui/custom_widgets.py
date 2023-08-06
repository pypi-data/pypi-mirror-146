"""Qt widgets that are not directly children of TcWidget.

Use this for more general custom widgets.
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
)
from pyqtgraph import PlotWidget, PlotDataItem, mkPen, intColor
import numpy as np
import time
from typing import List, Optional


class ScrollLabel(QScrollArea):
    """Scrollable label."""

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.setWidgetResizable(True)

        content = QWidget(self)
        self.setWidget(content)
        layout = QVBoxLayout(content)

        self.label = QLabel("NaN")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setTextFormat(Qt.RichText)  # Allow HTML-ish formatting
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        layout.addWidget(self.label)

    def setText(self, text):  # noqa: N802 # pylint: disable=invalid-name
        self.label.setText(text)


class GraphWidget(QWidget):
    """Class to make an rolling plot of some data.

    When data comes in faster than FS, the plot won't be refreshed. The data will
    still be stored and show up when it's time.

    :cvar FPS: Maximum refresh rate (Hz), faster samples are buffered but not yet
               plotted.
    """

    FPS = 30.0  # Maximum refresh rate

    def __init__(
            self,
            labels: List[str],
            units: Optional[List[str]] = None,
            buffer_size: int = 100,
            values_in_legend: bool = True,
            *args, **kwargs,
    ):
        """

        :param labels: List of strings corresponding to plotted variable names
        :param units: List of display units for each variable (default: None)
        :param buffer_size: Number of points to keep in graph
        :param values_in_legend: When `True` (default), put the last values in the
                                 legend
        """

        super().__init__(*args, **kwargs)

        self.labels = labels
        self.buffer_size = buffer_size
        self.units = units
        self.values_in_legend = values_in_legend

        self.num_signals = len(self.labels)

        if self.units is not None:
            if len(self.units) > self.num_signals:
                raise ValueError("Number of units does not match the number of signals")
            if len(self.units) < self.num_signals:
                self.units.extend([""] * (self.num_signals - len(self.units)))

        # All buffered data (column 0 is x-axis data) (row per sample)
        self.data = np.empty([self.buffer_size, self.num_signals + 1]) * np.nan
        # Create uninitialized matrix and place NaN values

        self.start_time: float = time.time()
        self.last_update: float = 0.0  # Keep track of last screen refresh

        # Make plot stuff:

        self.plot_widget = PlotWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_widget)

        self.plot_item = self.plot_widget.getPlotItem()

        self.legend = self.plot_item.addLegend()
        self.legend.setBrush('k')

        self.curves: List[PlotDataItem] = []

        for i, name in enumerate(self.labels):
            pen = mkPen(color=intColor(i), width=2)
            curve = self.plot_item.plot(name=name, pen=pen)
            self.curves.append(curve)

        for i, label in enumerate(self.labels):
            self.legend.items[i][1].setText(self.labels[i])

    def add_data(self, y_list: List[float], x: Optional[float] = None):
        """Add new datapoint to the rolling graph.

        :param y_list: List of new y-values
        :param x: New x-value (default: use system time instead)
        """

        if len(y_list) != self.num_signals:
            raise ValueError("Size of `y_list` does not match the number of signals!")

        if x is None:
            x = time.time() - self.start_time

        # Roll data matrix
        self.data = np.roll(self.data, -1, axis=0)  # Roll all rows up by one

        self.data[-1, :] = [x] + y_list

        if time.time() - self.last_update > 1.0 / self.FPS:
            self.update_plot()

    def update_plot(self):
        """Refresh the plot based on `self.data`."""

        for i, curve in enumerate(self.curves):
            curve.setData(x=self.data[:, 0], y=self.data[:, 1 + i])

            if self.values_in_legend:
                value = self.data[-1, 1 + i]
                entry = "{}: {:.3f}".format(self.labels[i], value)
                if self.units is not None:
                    entry += " [{}]".format(self.units[i])
                self.legend.items[i][1].setText(entry)

        self.last_update = time.time()
