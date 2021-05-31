import pysteamcmd
import os, platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STEAMCMD_LOC = "data/steamcmd"

IS_SERVER_ID = 581330
IS_SERVER_LOC = "data/insurgency_server"

class InsurgencyInstallerException(Exception):
    '''Generic exception class for the Insurgency: Sandstorm server installer.'''

    def __init__(self, message=None, *args, **kwargs):
        self.message = message
        super(InsurgencyInstallerException, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return repr(self.message)

    def __str__(self):
        return repr(self.message)

class InsurgencyServerInstaller:
    '''
    A class that handles installing the Insurgency: Sandstorm server and SteamCMD.
    Automatically downloads SteamCMD if it is not in the expected place.
    Run `install_is_server()` to download the Insurgency: Sandstorm server files.
    '''

    steamcmd = pysteamcmd.Steamcmd(STEAMCMD_LOC)
    os_name = platform.system()

    def __init__(self):
        if not os.path.isdir(STEAMCMD_LOC):
            os.makedirs(STEAMCMD_LOC)
        if not os.path.isdir(IS_SERVER_LOC):
            os.makedirs(IS_SERVER_LOC)
        # Ensure SteamCMD is installed
        if self.os_name == "Windows":
            steamcmd_path = os.path.join(STEAMCMD_LOC, "steamcmd.exe")
        elif self.os_name == "Linux":
            steamcmd_path = os.path.join(STEAMCMD_LOC, "steamcmd.sh")
        else:
            raise InsurgencyInstallerException("Your operating system is not supported. SteamCMD only has Windows and Linux support, {} will not work.".format(self.os_name))

        if not os.path.isfile(steamcmd_path):
            self.steamcmd.install()

    def install_is_server(self):
        '''Install or update the Insurgency: Sandstorm server.'''
        # Move up two levels to account for the data/steamcmd directory in game_install_dir 
        self.steamcmd.install_gamefiles(gameid=IS_SERVER_ID, game_install_dir=os.path.join("../../", IS_SERVER_LOC), validate=True)

    @staticmethod
    def is_installed():
        '''Is the Insurgency server installed?'''
        return os.path.isdir(os.path.join(IS_SERVER_LOC, "Insurgency"))

if __name__ == "__main__":
    print(IS_SERVER_LOC)
    iss = InsurgencyServerInstaller()
    iss.install_is_server()