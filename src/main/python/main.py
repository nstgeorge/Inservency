import os
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from layout import Ui_Inservency
from ui.map_manager_ui import MapManagerUI

BASE_PATH = "./src/main/python"

def handle_server_start_requirements():
    if
    if map_manager.starting_map is not None and map_manager.open_file is not None:
        inserv_ui.startServerButton.setDisabled(False)

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    inserv_ui = Ui_Inservency()
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    appctxt.app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    window = QMainWindow()
    inserv_ui.setupUi(window)

    map_manager = MapManagerUI(inserv_ui, window)

    # Handle server start requirements
    inserv_ui.startServerButton.setDisabled(True)


    window.show()
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)

