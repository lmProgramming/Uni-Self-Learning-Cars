from typing import Literal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

ERROR_WIDTH = 300
ERROR_HEIGHT = 200

class ErrorPopup(QWidget):
    def __init__(self, message, dimensions):
        QWidget.__init__(self)
        
        self.setWindowTitle("Error!")
        
        self.setGeometry(*dimensions)
        
        self.setup_ui(message)        
        
    def setup_ui(self, message):
        layout = QVBoxLayout(self)
        
        label = QLabel(self)
        label.setText(message)
        layout.addWidget(label)
        
        button = QPushButton(self)
        button.setText("Close")
        button.clicked.connect(self.close)
        layout.addWidget(button)
        
        self.setLayout(layout)
        
def create_error_popup(message, start_position=[0,0]) -> ErrorPopup:
    popup = ErrorPopup(message, (*start_position, ERROR_WIDTH, ERROR_HEIGHT))
    popup.show()
    
    return popup