import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMainWindow, QInputDialog, QMessageBox

class ScrollableGallery(QMainWindow):
    def __init__(self, dimensions):
        super().__init__()
        self.initUI(dimensions)

    def initUI(self, dimensions) -> None:
        self.setGeometry(*dimensions)
        
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
        self.containerLayout = QVBoxLayout(container)
                
    def createRow(self, widgets):
        rowWidget = QWidget()
        rowLayout = QHBoxLayout(rowWidget)
        
        for widget in widgets:
            rowLayout.addWidget(widget)      
        
        self.containerLayout.addWidget(rowWidget)
    
    def stretch_items(self) -> None:        
        self.containerLayout.addStretch()
