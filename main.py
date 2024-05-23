from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from neat_and_pygame import main as start_simulation
from player_test import test_drive
from maps.map_maker import create_edit_map as create_new_map
import sys
import os

from gui_main import UiMain

class Main(QMainWindow):
    def __init__(self, app) -> None:
        super().__init__()
        
        self.ui = UiMain()
        
        self.setCentralWidget(self.ui)
        
        self.ui.setupUi(self, dimensions=(800, 600))
        
        self.ui.default_simulation_button.clicked.connect(self.start_simulation)
        self.ui.parameters_simulation_button.clicked.connect(self.open_parameters_screen)
        self.ui.map_menu_button.clicked.connect(self.open_map_screen)
        
        self.ui.test_ride_button.clicked.connect(self.start_test_drive)
                
        self.resize(800, 600) 
        
        self.open_main_menu_screen()
        
        self.setWindowIcon(QtGui.QIcon(os.path.join("imgs", "car_img.png")))
        
    def start_simulation(self) -> None:
        start_simulation()
        
    def open_main_menu_screen(self) -> None:
        self.ui.QtStack.setCurrentIndex(0)
        self.setWindowTitle("Main Menu") 
        
    def open_parameters_screen(self) -> None:
        self.ui.QtStack.setCurrentIndex(1)
        self.setWindowTitle("Parameters") 
        
    def open_map_screen(self) -> None:
        self.ui.QtStack.setCurrentIndex(2)
        self.setWindowTitle("Maps")
        
    def start_test_drive(self) -> None:
        test_drive()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main(app)
    showMain.show()
    sys.exit(app.exec_())
