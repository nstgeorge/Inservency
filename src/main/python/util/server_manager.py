import subprocess
import os
import platform

from ui.map_manager_ui import MapManagerUI
from layout import Ui_Inservency
from util.settings_manager import ServerSettings
from util.install_server import InsurgencyServerInstaller


class ServerManager:
    def __init__(self, inserv_ui: Ui_Inservency, map_manager_instance: MapManagerUI,
                 settings_manager_instance: ServerSettings):
        self.inserv_ui = inserv_ui
        self.map_manager = map_manager_instance
        self.settings_manager = settings_manager_instance

        self.inserv_ui.startServerButton.clicked.connect(self.start)

    def start(self):
        if not InsurgencyServerInstaller.is_installed():
            print("Installing Insurgency server")
            self.inserv_ui.startServerButton.setDisabled(True)
            self.install()

        if platform.system() == "Windows":
            pass
            #subprocess.run([os.path.join("data", "insurgency_server", )])

    def install(self):
        self.inserv_ui.statusbar.showMessage("Installing Insurgency: Sandstorm server binaries...")
        installer = InsurgencyServerInstaller()
        installer.install_is_server()
        self.inserv_ui.statusbar.showMessage("Server binaries downloaded.", timeout=5000)
