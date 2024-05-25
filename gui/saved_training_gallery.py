import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox
from neat_save_load import delete_checkpoint, get_saved_checkpoints, get_config, get_timestamp
from neat_training import load_checkpoint

from gui.scrollable_gallery import ScrollableGallery
from simulation.simulation_config import SimulationConfig

class SavedTrainingGallery(ScrollableGallery):
    def __init__(self, dimensions):
        super().__init__(dimensions)
        self.rows = []

    def populateGallery(self, saved_training_filenames):
        for saved_training_filename in saved_training_filenames:
            self.createSavedTrainingRow(saved_training_filename)
        self.stretch_items()
        
    def createSavedTrainingRow(self, saved_training_filename):
        saved_training_label = QLabel(saved_training_filename)
        deleteButton = QPushButton('Delete')
        loadButton = QPushButton('Load')
        
        deleteButton.clicked.connect(lambda: self.deleteCheckpoint(saved_training_label))
        loadButton.clicked.connect(lambda: self.loadCheckpoint(saved_training_filename))
        
        self.createRow([saved_training_label, deleteButton, loadButton])
        
        self.rows.append((saved_training_filename, saved_training_label))

    def deleteCheckpoint(self, checkpointLabel) -> None:
        rowWidget = checkpointLabel.parentWidget()
        reply = QMessageBox.question(
            self, 'Delete Map', 'Are you sure you want to delete this map?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            delete_checkpoint(checkpointLabel.text())
            rowWidget.setParent(None)

    def loadCheckpoint(self, checkpoint) -> None:
        timestamp: str = get_timestamp(checkpoint)
        simulation_config: SimulationConfig = get_config(timestamp)
        load_checkpoint(simulation_config, checkpoint)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = SavedTrainingGallery([800, 300, 600, 400])
    gallery.populateGallery(get_saved_checkpoints())
    gallery.show()
    sys.exit(app.exec_())