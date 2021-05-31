import json, pickle, os, configparser, platform

SETTINGS_PATH = "./data/insurgency_server/Insurgency/Config"

def load_json(json_path):
        '''Helper: Load a JSON path.'''
        with open(json_path, 'r') as file:
            return json.load(file)

class ServerSettingsException(Exception):
    '''Exception caused by errors in basic server configuration or saving and loading server settings files.'''

    def __init__(self, message=None, *args, **kwargs):
        self.message = message
        super(ServerSettingsException, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return repr(self.message)

    def __str__(self):
        return repr(self.message)

class ServerSettings:
    '''Stores and manages the settings for the server.'''

    settings_dir = SETTINGS_PATH

    game_port = 27102
    query_port = 27131
    hostname = "Inservency Server"
    cheats = False
    password = None
    max_players = 28
    admins = []
    motd = "Welcome to the server!"
    
    def __init__(self):
        platform_specific_folder = ""
        if platform.system() == "Windows":
            platform_specific_folder = "WindowsServer"
        else:
            platform_specific_folder = "LinuxServer"

        self.settings_dir = os.path.join(SETTINGS_PATH, platform_specific_folder)

        if not os.path.isdir(self.settings_dir):
            os.makedirs(self.settings_dir)

        

    def save_settings(self, name="default", force=False):
        '''Save the settings to the system. `name` can be used to create unique setting saves. If a custom name is provided and the name already exists, `force` will overwrite the file.'''
        filename = os.path.join(SETTINGS_PATH, "{}_settings.p".format(name))
        try:
            os.makedirs(SETTINGS_PATH)
        except FileExistsError:
            pass

        if os.path.isfile(filename) and not force and not name == "default":
            raise ServerSettingsException("Server setting file \"{}\" already exists. Use force=True to save to this location.".format(name))

        with open(filename, 'wb') as settings_file:
            pickle.dump(self, settings_file)

    def load_settings(self, name="default"):
        '''Load the settings from the system.'''
        filename = os.path.join(SETTINGS_PATH, "{}_settings.p".format(name))
        if not os.path.isfile(filename):
            raise ServerSettingsException("Settings file name \"{}\" does not exist.".format(name))

        with open(filename, 'rb') as settings_file:
            pickle.load(self, settings_file)

    