from util.map_manager import MapManager, get_all_scenarios, get_map_scenarios, get_scenario_name, MAP_LIST_DIR

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMenu, QAction

from PyQt5.QtCore import Qt, QModelIndex

from layout import Ui_Inservency
from util.item_tree import TreeModel

from functools import partial

import os


class MapManagerUI:
    """Front-end representation of the MapManager class."""

    def __init__(self, inserv_ui: Ui_Inservency, window: QMainWindow):
        self.scenario_model = TreeModel(get_all_scenarios())
        self.map_manager = MapManager()

        self.inserv_ui = inserv_ui
        self.window = window

        self.map_actions = {}
        self.scenario_actions = {}

        self.starting_map = None
        self.open_file = None

        # Map list
        inserv_ui.saveMapListAsButton.clicked.connect(self.save_as_map_list)
        self.setup_map_list_ui()
        inserv_ui.loadMapListButton.clicked.connect(self.load_map_list)

        # Starting map
        inserv_ui.startingMapDropdown.setMenu(self._generate_map_menu())
        inserv_ui.startingMapDropdown.clicked.connect(inserv_ui.startingMapDropdown.showMenu)
        inserv_ui.startingScenarioDropdown.clicked.connect(inserv_ui.startingScenarioDropdown.showMenu)
        self.inserv_ui.startingScenarioDropdown.hide()

    def save_as_map_list(self):
        if not os.path.isdir(MAP_LIST_DIR):
            os.makedirs(MAP_LIST_DIR)

        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)

        dialog.setDirectory(os.path.join(os.getcwd(), MAP_LIST_DIR))
        dialog.setObjectName("Save Map List As")
        dialog.setNameFilter("Text files (*.txt)")
        dialog.setDefaultSuffix("txt")
        filename = dialog.getSaveFileName(self.window, "Choose map list save location", MAP_LIST_DIR, "Text files (*.txt)")[0]

        self.save_changes_to_internal_map_list()
        self.map_manager.save_map_list(filename)
        self.open_file = filename

    def load_map_list(self):
        if not os.path.isdir(MAP_LIST_DIR):
            os.makedirs(MAP_LIST_DIR)

        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptOpen)

        dialog.setDirectory(os.path.join(os.getcwd(), MAP_LIST_DIR))
        dialog.setDefaultSuffix("txt")
        filename = dialog.getOpenFileName(self.window, "Choose map list", MAP_LIST_DIR, "Text files (*.txt)")[0]

        with open(filename, 'r') as f:
            file_text = f.read().split()
            self.map_manager.clear()
            for map_item in self.scenario_model.get_root().children():
                for scenario_item in map_item.children():
                    if get_scenario_name(map_item.data(0), scenario_item.data(0).replace(" ", "_")) in file_text:
                        scenario_item.set_check_state(True)
                    else:
                        scenario_item.set_check_state(False)

    def setup_map_list_ui(self):
        self.inserv_ui.scenarioTreeView.setModel(self.scenario_model)
        self.inserv_ui.scenarioTreeView.setColumnWidth(0, 500)
        self.scenario_model.dataChanged.connect(self.refresh_check_state)

    def refresh_check_state(self):
        # This is awful but it's the only thing that worked
        self.inserv_ui.scenarioTreeView.hide()
        self.inserv_ui.scenarioTreeView.show()

    def save_changes_to_internal_map_list(self):
        self.map_manager.clear()
        for map_item in self.scenario_model.get_root().children():
            for scenario_item in map_item.children():
                if scenario_item.get_check_state() == Qt.Checked:
                    self.map_manager.append_to_map_list(get_scenario_name(map_item.data(0), scenario_item.data(0).replace(" ", "_")))

    def set_starting_map(self, map_name):
        self.inserv_ui.startingScenarioDropdown.setMenu(self._generate_scenario_menu(map_name))
        self.inserv_ui.startingScenarioDropdown.show()
        self.inserv_ui.startingMapDropdown.setText(map_name)
        scenario = self.inserv_ui.startingScenarioDropdown.text()
        if scenario != "Select Scenario...":
            if scenario not in get_map_scenarios(map_name):
                self.starting_map = None
                self.inserv_ui.startingScenarioDropdown.setText("Select Scenario...")
            else:
                self.starting_map = get_scenario_name(map_name, scenario.replace(" ", "_"))

    def set_starting_scenario(self, scenario):
        self.inserv_ui.startingScenarioDropdown.setText(scenario)
        map_name = self.inserv_ui.startingMapDropdown.text()
        self.starting_map = get_scenario_name(map_name, scenario.replace(" ", "_"))

    def _generate_map_menu(self):
        menu = QMenu(self.inserv_ui.startingMapDropdown)

        for map_name in get_all_scenarios():
            self.map_actions[map_name] = QAction(map_name, self.window)
            self.map_actions[map_name].triggered.connect(partial(self.set_starting_map, map_name))
            menu.addAction(self.map_actions[map_name])

        return menu

    def _generate_scenario_menu(self, map_name):
        menu = QMenu(self.inserv_ui.startingScenarioDropdown)
        self.scenario_actions = {}

        for scenario in get_map_scenarios(map_name):
            scenario = scenario.replace("_", " ")
            self.scenario_actions[scenario] = QAction(scenario, self.window)
            self.scenario_actions[scenario].triggered.connect(partial(self.set_starting_scenario, scenario))
            menu.addAction(self.scenario_actions[scenario])

        return menu
