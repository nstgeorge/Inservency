import json, pickle, os

MAPS_PATH = "./data/maps.json"
MAP_LIST_DIR = "./data/stored/map_lists"

class MapManagerException(Exception):
    '''Exception associated with loading maps and scenarios.'''

    def __init__(self, message=None, *args, **kwargs):
        self.message = message
        super(MapManagerException, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return repr(self.message)

    def __str__(self):
        return repr(self.message)

class MapManager:
    '''Manages maps, scenarios, and map lists.'''

    scenarios = {}
    map_lists = {}

    def __init__(self):
        with open(MAPS_PATH, 'r') as f:
            self.scenarios = json.load(f)

    def get_all_scenarios(self):
        '''Get the dictionary of scenarios associated with maps.'''
        return self.scenarios

    def get_all_maps(self):
        '''Get all map names.'''
        return self.scenarios.keys()

    def get_scenario_name(self, map_name, scenario_name):
        '''Get the proper scenario name associated with the given map.'''

        if map_name not in self.scenarios.keys():
            raise MapManagerException("Map \"{}\" does not exist.".format(map_name))

        if scenario_name not in self.scenarios[map_name]["gametypes"]: 
            raise MapManagerException("Map {} does not have a scenario called \"{}\".".format(map_name, scenario_name))
            
        return self.scenarios[map_name]["prefix"] + scenario_name

    def get_map_scenarios(self, map_name):
        '''Get the valid game types for the map.'''
        return self.scenarios[map_name]["gametypes"]

    def get_friendly_map_scenarios(self, map_name):
        '''Get game types for this map that look nice for the user.'''
        return [scenario.replace("_", " ") for scenario in self.scenarios[map_name]["gametypes"]]

    def save_map_lists(self):
        '''Save the map lists to the system.'''
        try:
            os.makedirs(MAP_LIST_DIR)
        except FileExistsError:
            pass
        with open(os.path.join(MAP_LIST_DIR, "map_lists.p"), 'wb') as map_file:
            pickle.dump(self.map_lists, map_file)

    def load_map_lists(self, append_to_existing=False):
        '''Load the map lists from the system. If `append_to_existing`, the map list loaded will be appended to the map lists in memory.'''
        if not os.path.isfile(os.path.join(MAP_LIST_DIR, "map_lists.p")):
            raise MapManagerException("Unable to load map lists. Make sure you've already saved your map lists.")

        with open(os.path.join(MAP_LIST_DIR, "map_lists.p"), 'rb') as map_file:
            pickle.load(self.map_lists, map_file)

    def get_map_list(self, list_name):
        '''Get the map list of the given name.'''
        if list_name not in self.map_lists.keys():
            raise MapManagerException("Attempted to access map list \"{}\", which does not exist.".format(list_name))
        return self.map_lists[list_name]

    def has_list_called(self, list_name):
        '''Does the map list directory contain a list by the given name?'''
        return list_name in self.map_lists.keys()

    def create_map_list(self, list_name, *scenarios):
        '''Create a new map list with the given name and associated scenarios. Expects properly formatted scenario names like those provided by `get_scenario_name()`.'''
        self.map_lists[list_name] = []
        self.append_to_map_list(list_name, scenarios)

    def append_to_map_list(self, list_name, *scenarios):
        '''Append the given scenarios to the map list. Expects properly formatted scenario names like those provided by `get_scenario_name()`.'''
        for s in scenarios:
            self.get_map_list(list_name).append(s)

    def remove_from_map_list(self, list_name, *scenarios):
        '''Remove the scenarios from the map list.'''
        for s in scenarios:
            if s in self.get_map_list(list_name):
                self.map_lists[list_name].remove(s)

    
