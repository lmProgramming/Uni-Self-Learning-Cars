import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QInputDialog, QMessageBox

from scrollable_gallery import ScrollableGallery
from map_scripts.map_tools import rename_map, delete_map
from map_scripts.map_reader import read_map_txt
from map_scripts.map_maker import create_edit_map

class MapGallery(ScrollableGallery):
    def __init__(self, dimensions):
        super().__init__(dimensions)
        self.rows = []

    def populateGallery(self, map_names):
        for map_name in map_names:
            self.createMapRow(map_name)
        self.stretch_items()
        
    def createMapRow(self, map_name):
        mapLabel = QLabel(map_name)
        renameButton = QPushButton('Rename')
        deleteButton = QPushButton('Delete')
        editButton = QPushButton('Edit')
        
        # Connect buttons to functions
        renameButton.clicked.connect(lambda: self.renameMap(mapLabel))
        deleteButton.clicked.connect(lambda: self.deleteMap(mapLabel))
        editButton.clicked.connect(lambda: self.editMap(map_name))
        
        self.createRow([mapLabel, renameButton, deleteButton, editButton])
        
        self.rows.append((map_name, mapLabel))

    def renameMap(self, mapLabel):
        new_name, ok = QInputDialog.getText(self, 'Rename Map', 'Enter new name:')
        if ok and new_name:
            new_name = rename_map(mapLabel.text(), new_name)
            mapLabel.setText(new_name)

    def deleteMap(self, mapLabel):
        rowWidget = mapLabel.parentWidget()
        reply = QMessageBox.question(self, 'Delete Map', 'Are you sure you want to delete this map?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_map(mapLabel.text())
            rowWidget.setParent(None)

    def editMap(self, map_name):
        create_edit_map(*read_map_txt(map_name), map_name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = MapGallery([800, 300, 600, 400])
    gallery.show()
    sys.exit(app.exec_())