from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from neat_and_pygame import main as start_simulation, test_drive
import sys

from gui_main import UiMain

class Main(QMainWindow):
    def __init__(self, app) -> None:
        super().__init__()
               
        self.ui = UiMain()   
                
        self.setCentralWidget(self.ui)
                    
        self.ui.setupUi(self, dimensions=(800, 600))
        
        self.ui.default_simulation_button.clicked.connect(start_simulation)
        self.ui.parameters_simulation_button.clicked.connect(self.open_parameters_screen)
        self.ui.test_ride_button.clicked.connect(self.start_test_drive)
                
        self.resize(800, 600) 
        
        self.open_main_menu_screen()
        
    def open_main_menu_screen(self) -> None:
        self.ui.QtStack.setCurrentIndex(0)
        self.setWindowTitle("Main Menu") 
        
    def open_parameters_screen(self) -> None:
        self.ui.QtStack.setCurrentIndex(1)
        self.setWindowTitle("Parameters") 
        
    def OpenWindow2(self) -> None:
        self.ui.QtStack.setCurrentIndex(2)
        self.setWindowTitle("Another Screen")
        
    def start_test_drive(self) -> None:
        test_drive()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main(app)
    showMain.show()  # Ensure the main window is shown
    sys.exit(app.exec_())
