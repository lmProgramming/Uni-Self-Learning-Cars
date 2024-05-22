import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QMainWindow

class ScrollableGallery(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Scrollable Gallery of Widgets')
        self.setGeometry(100, 100, 800, 600)
        
        # Create a central widget and set layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        
        mainLayout = QVBoxLayout(centralWidget)
        
        # Create scroll area
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(scrollArea)
        
        # Create a container widget and set a layout for it
        container = QWidget()
        scrollArea.setWidget(container)
        containerLayout = QVBoxLayout(container)
        
        # Add a stretch at the end to push all widgets to the top
        containerLayout.addStretch()
        
    def createRow(self, map_name):
        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        
        # Map Name
        mapLabel = QLabel(map_name)
        rowLayout.addWidget(mapLabel)
        
        # Rename Button
        renameButton = QPushButton('Rename')
        rowLayout.addWidget(renameButton)
        
        # Delete Button
        deleteButton = QPushButton('Delete')
        rowLayout.addWidget(deleteButton)
        
        # Edit Button
        editButton = QPushButton('Edit')
        rowLayout.addWidget(editButton)
        
        return rowWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = ScrollableGallery()
    gallery.show()
    sys.exit(app.exec_())