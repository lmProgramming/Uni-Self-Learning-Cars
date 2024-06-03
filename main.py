from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui
from neat_training import main as start_simulation
from simulation.player_test import test_drive
import sys
import os
import qdarktheme # type: ignore
import platform

from gui.gui_main import UiMain

class Main(QMainWindow):
    def __init__(self, app) -> None:
        super().__init__()
        
        self.ui = UiMain(self.open_main_menu_screen)
        
        self.setCentralWidget(self.ui)
        
        self.ui.setupUi(self, dimensions=(800, 600))
        
        self.ui.default_simulation_button.clicked.connect(self.start_simulation)
        self.ui.parameters_simulation_button.clicked.connect(self.open_parameters_screen)
        self.ui.map_menu_button.clicked.connect(self.open_map_screen)
        self.ui.load_saved_training_button.clicked.connect(self.open_load_saved_screen)        
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
        
    def open_load_saved_screen(self) -> None:
        self.ui.QtStack.setCurrentIndex(3)
        self.setWindowTitle("Saved Training Data")
        
    def start_test_drive(self) -> None:
        test_drive()
        
def set_dark_theme(app) -> None:
    dark_palette: QtGui.QPalette = qdarktheme.load_palette()
    
    app.setStyle("Fusion" if platform.release() == "10" else "Windows")
    app.setPalette(dark_palette)
    
def open_main_menu():
    app = QApplication(sys.argv)
    
    set_dark_theme(app)
    
    showMain = Main(app)
    showMain.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    open_main_menu()
