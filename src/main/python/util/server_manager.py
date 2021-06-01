import subprocess

from map_manager import MapManager
from settings_manager import ServerSettings

class ServerManager:
    def __init__(self, map_manager_instance: MapManager, settings_manager_instance: ServerSettings):
        self.map_manager = map_manager_instance
        self.settings_manager = settings_manager_instance



