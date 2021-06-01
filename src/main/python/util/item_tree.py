
from PyQt5 import QtCore


# This code modified from https://gist.github.com/zhanglongqi/6994c2bc611bacb4c68f

class TreeItem(QtCore.QVariant):
    def __init__(self, data, parent=None, *__args):
        super().__init__(*__args)
        self.parentItem = parent
        self.itemData = data
        self.checkState = False
        self.childItems = []

    def append_child(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def children(self):
        return self.childItems

    def child_count(self):
        return len(self.childItems)

    def column_count(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def update_check_state(self):
        """Update the check state for this item based on the values of its children."""
        print("{}: {}".format(self.data(0), self.child_count()))
        if self.child_count() == 0:
            return
        if all(self.childItems[0].get_check_state() == i.get_check_state() for i in self.childItems):
            self.checkState = self.childItems[0].get_check_state()
        else:
            self.checkState = QtCore.Qt.PartiallyChecked

    def set_check_state(self, state):
        """Set the check state for this item and update its children."""
        print("Setting {} to state {}".format(self.data(0), state))
        if type(state) == bool:
            self.checkState = QtCore.Qt.Checked if state else QtCore.Qt.Unchecked
        else:
            self.checkState = state

        for item in self.childItems:
            item.checkState = self.checkState

        self.parent().update_check_state()

    def toggle_check(self):
        """Toggle the check value of this item and update its children or parent."""
        if self.checkState == QtCore.Qt.Checked:
            self.set_check_state(False)
        else:
            # Handles PartiallyChecked
            self.set_check_state(True)

    def get_check_state(self):
        return self.checkState


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(["Map/Scenario"])
        self.add_from_maps_data(data)
        self.check_col = 0

        self.last_action = None

    def get_root(self):
        return self.rootItem

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().column_count()
        else:
            return self.rootItem.column_count()

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.CheckStateRole and index.column() == self.check_col:
            return item.get_check_state()

        if role == QtCore.Qt.DisplayRole:
            return item.data(index.column())

        return None

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.column() == self.check_col:
            if role == QtCore.Qt.EditRole:
                return False
            if role == QtCore.Qt.CheckStateRole:
                item = index.internalPointer()
                item.toggle_check()
                self.last_action = (item, item.get_check_state())

                self.dataChanged.emit(index, index)
                return True

        return super(TreeModel, self).setData(index, value, role)

    def flags(self, index):
        if not index.isValid():
            return None

        if index.column() == self.check_col:
            flags = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsUserCheckable
        else:
            flags = super(TreeModel, self).flags(index)

        return flags

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

    def get_parent_of_data(self, data):
        for item in self.rootItem.children():
            if data in [i.data(0) for i in item.children()]:
                return item.data(0)

        return None

    def add_from_maps_data(self, obj: dict):
        for map_name in obj.keys():
            self.add_data(map_name, self.rootItem)
            parent = self.rootItem.child(self.rootItem.child_count() - 1)
            for scenario in obj[map_name]["gametypes"]:
                self.add_data(scenario.replace("_", " "), parent)

    def add_data(self, string, parent):
        new_item = TreeItem([string], parent)
        parent.append_child(new_item)
