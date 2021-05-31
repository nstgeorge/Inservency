from util.map_manager import MapManager, get_all_scenarios, MAP_LIST_DIR

from PyQt5.QtWidgets import QFileDialog

from layout import Ui_Inservency
from util.item_tree import TreeModel

import os


class MapManagerUI:
    """Front-end representation of the MapManager class."""

    def __init__(self, inserv_ui: Ui_Inservency):
        self.map_manager = MapManager()

        self.inserv_ui = inserv_ui

        inserv_ui.saveMapListAsButton.clicked.connect(self.save_as_map_list)
        self.setup_map_list_ui()

    def save_as_map_list(self, window):
        edited_list_dir = os.path.join("src", "main", "python", MAP_LIST_DIR)
        if not os.path.isdir(edited_list_dir):
            os.makedirs(edited_list_dir)

        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptSave)

        dialog.setDirectory(edited_list_dir)
        dialog.setObjectName("Save Map List As")
        dialog.setNameFilter("Text files (*.txt)")
        dialog.setDefaultSuffix("txt")

        if dialog.exec_():
            filename = dialog.getSaveFileName(window)
            self.map_manager.save_map_list(filename)

    def setup_map_list_ui(self):
        scenario_model = TreeModel(get_all_scenarios())

        self.inserv_ui.scenarioTreeView.setModel(scenario_model)
        self.inserv_ui.scenarioTreeView.setColumnWidth(0, 500)

        scenario_model.dataChanged.connect(self.refresh_check_state)

    def refresh_check_state(self):
        # This is awful but it's the only thing that worked
        self.inserv_ui.scenarioTreeView.hide()
        self.inserv_ui.scenarioTreeView.show()
