import json
import os

MAPS_PATH = "data/maps.json"
MAP_LIST_DIR = "data/insurgency_server/Insurgency/Config/Server"

with open(MAPS_PATH, 'r') as f:
    SCENARIOS = json.load(f)


def get_scenario_name(map_name, scenario_name):
    """Get the proper scenario name associated with the given map."""

    if map_name not in SCENARIOS.keys():
        raise MapManagerException("Map \"{}\" does not exist.".format(map_name))

    if scenario_name not in SCENARIOS[map_name]["gametypes"]:
        raise MapManagerException("Map {} does not have a scenario called \"{}\".".format(map_name, scenario_name))

    return SCENARIOS[map_name]["prefix"] + scenario_name


def get_friendly_map_scenarios(map_name):
    """Get game types for this map that look nice for the user."""
    return [scenario.replace("_", " ") for scenario in SCENARIOS[map_name]["gametypes"]]


def get_map_of_scenario(scenario):
    """Returns the name of the map associated with the scenario."""
    for map_name in SCENARIOS.keys():
        if scenario in SCENARIOS[map_name]:
            return map_name

    return None


def get_all_scenarios():
    """Get the dictionary of scenarios associated with maps."""
    return SCENARIOS


def get_all_maps():
    """Get all map names."""
    return SCENARIOS.keys()


def get_map_scenarios(map_name):
    """Get the valid game types for the map."""
    return SCENARIOS[map_name]["gametypes"]


def has_list_called(list_name):
    """Does the map list directory contain a list by the given name?"""
    return list_name in [s.split(".")[0] for s in os.walk(MAP_LIST_DIR)]


class MapManagerException(Exception):
    """Exception associated with loading maps and scenarios."""

    def __init__(self, message=None, *args):
        self.message = message
        super(MapManagerException, self).__init__(*args)

    def __unicode__(self):
        return repr(self.message)

    def __str__(self):
        return repr(self.message)


class MapManager:
    """Manages maps, scenarios, and map lists."""

    SCENARIOS = {}
    map_list = []
    list_dirty = False

    current_list_path = ""

    def __init__(self, *maps):
        if not os.path.exists(MAP_LIST_DIR):
            os.makedirs(MAP_LIST_DIR)

        self.append_to_map_list(maps)

    def clear(self):
        self.map_list = []

    def save_map_list(self, path):
        """Save the map lists to the system."""
        try:
            os.makedirs(MAP_LIST_DIR)
        except FileExistsError:
            pass
        with open(path, 'w') as map_file:
            for s in self.map_list:
                map_file.write(s + "\n")

        self.list_dirty = False

    def load_map_list(self, path):
        """Load the given map list from the system."""
        if not os.path.isfile(path):
            raise MapManagerException("Unable to load map list at {}.".format(path))

        with open(path, 'r') as map_file:
            self.map_list = map_file.read().split()

        self.list_dirty = False

    def get_map_list(self):
        """Get the map list."""
        return self.map_list

    def append_to_map_list(self, *scenarios):
        """Append the given scenarios to the map list. Expects properly formatted scenario names like those provided
        by `get_scenario_name()`. """
        for s in scenarios:
            self.map_list.append(s)

        self.list_dirty = True

    def remove_from_map_list(self, *scenarios):
        """Remove the scenarios from the map list."""
        for s in scenarios:
            if s in self.map_list:
                self.map_list.remove(s)

        self.list_dirty = True
