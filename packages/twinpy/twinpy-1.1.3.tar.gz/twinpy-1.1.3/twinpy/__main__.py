"""Example of a script using a GUI.

You can run the BaseGUI itself (linked to the WE actuator model) by running

    `$ python -m twinpy`

(I.e. by executing the module.) This provides a quick demo of how such a GUI can
work, and a quick check to see everything is working on your system.

This script should not be used in your program! Instead, your application should
have it's own main script and create a GUI instance from there.
"""


from PyQt5.QtWidgets import QApplication
import sys
from pyads import ADSError

from twinpy.ui import BaseGUI
from twinpy.twincat import SimulinkModel
from twinpy.twincat import TwincatConnection


class GUI(BaseGUI):
    """Some extension of the BaseGUI.

    Custom GUIs should extend the base class.
    """


if __name__ == "__main__":

    app = QApplication(sys.argv)

    models = {
        "actuator": SimulinkModel(
            0x01010010, "WE2_actuator_model", "we2_actuator_model"
        ),
        "controller": SimulinkModel(
            0x01010030, "WE2_controller_model", "we2_controller_model"
        ),
    }

    try:
        connection = TwincatConnection()
        for name, model in models.items():
            model.connect_to_twincat(connection)

    except ADSError as err:
        connection = None
        print("Not connected to TwinCAT, continuing -", err)

    gui = GUI(**models)

    app.exec()
