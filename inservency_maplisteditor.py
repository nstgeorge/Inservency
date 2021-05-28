from util.settings_manager import ServerSettings, ServerSettingsException
from util.install_server import InsurgencyServerInstaller, InsurgencyInstallerException
from util.map_manager import MapManager, MapManagerException

import argparse

def start_server():
    '''Start the server.'''
    # Check installation status
    if not InsurgencyServerInstaller.is_installed():
        print("The Insurgency: Sandstorm server binaries do not appear to be downloaded. Attempting to download.")
        installer = InsurgencyServerInstaller()
        installer.install_is_server()

    # TODO: Finish server config/start routine

def map_list_create(map_manager: MapManager):
    valid = False
    while not valid:
        list_name = input("Time to create a map list! What should the list be called? ")
        
        if map_manager.has_list_called(list_name):
            print("There is already a list by that name, please delete the list first or choose another name.")

        else:
            valid = True
            map_manager.create_map_list(list_name)
            map_list_loop(map_manager, list_name)

def map_list_loop(map_manager: MapManager, list_name):
    '''Loop through adding maps to a list.'''

    map_loop_help = """
COMMANDS:
    "(h)elp": List commands.
    "(m)aps": List map names.
    "(s)cenarios": List scenarios that work with the selected map. *This can only be used if a map is selected.*
    "(d)one": End the current scenario list or map list.

TIPS:
    - You can enter more than one map or scenario at a time -- just separate each one with commas. For instance, this is a valid way to enter these maps all at once: Town, Farmhouse, Mountain
    - If you're not sure which scenarios work with the map you selected, type "scenarios".
    - All commands can be written as their first letter as a form of shorthand. You can pull up this page with just "h".
    """

    print("You will enter a map name, followed by a list of gamemodes on that map. Type \"help\" for some commands that might help you, or \"done\" to end the map entering process.")

    user_input = ""
    while user_input.lower() != "done" or user_input != 'd':
        user_input = input("Enter the name of a map or type \"help\" for commands that could help you: ")

        if user_input.lower() == "help" or user_input == "h":
            print(map_loop_help)

        elif user_input.lower() == "maps" or user_input == "m":
            print("All valid map names:")
            for m in map_manager.get_all_maps():
                print(m)

        elif user_input.lower() == "done" or user_input == "d":
            print("Map entry complete.")
            break

        else:
            for map_name in user_input.split(","):
                map_name = map_name.strip()
                map_list_edit_entry(map_manager, list_name, map_name)


def map_list_edit_entry(map_manager: MapManager, list_name, map_name):

    valid = False
    while not valid:
        if map_name not in map_manager.get_all_maps():
            print("\"{}\" is not a valid map name or command. Type \"maps\" to see the list of valid map names, or \"help\" for commands.".format(map_name))
            continue

        user_input = input("Which scenarios would you like to include for {}? ".format(map_name))

        if user_input.lower() == "scenarios" or user_input == "s":
            print("Valid scenarios for {}:".format(map_name))
            for scenario in map_manager.get_friendly_map_scenarios(map_name):
                print(scenario)

        elif user_input.lower() == "done" or user_input == "d":
            continue

        else:
            for scen_name in user_input.split(","):
                scen_name = scen_name.strip()
                scen_name = scen_name.replace(" ", "_")
                if scen_name not in map_manager.get_map_scenarios(map_name):
                    print("\"{}\" is not a valid scenario name or command. Type \"scenarios\" to see the list of valid scenario names, or \"help\" for commands.".format(scen_name))
                    continue

                map_manager.append_to_map_list(list_name, map_manager.get_scenario_name(map_name, scen_name))
            map_manager.save_map_lists()
            print("Added all scenarios to the map list.")
            valid = True
if __name__ == "__main__":
    map_manager = MapManager()
    try:
        map_manager.load_map_lists()
    except MapManagerException:
        print("Could not load map list. This is only a problem if you expect maps to be saved already.")

    map_list_create(map_manager)
    print(map_manager.get_map_list("FirstMapList"))
