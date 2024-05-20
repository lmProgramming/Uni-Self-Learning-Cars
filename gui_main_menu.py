'''
Do funkcjonalności chciałbym dodać jeszcze możliwość modyfikacji pliku konfiguracyjnego NEAT za pomocą GUI. 
GUI pozwalałoby na szeroką interakcję z mapami: dodanie nowej mapy, a także modyfikacja lub usunięcie istniejącej. 
Mapy planuję zapisać w formacie JSON lub CSV i przechowują pozycje ścian, pozycję startową oraz pozycje "bramek", które nagradzają 
samochód za przejechanie przez nie. Planuję dodać zbieranie i wizualizowanie statystyk agentów: np. zależność między fitness a czasem trenowania 
czy zależność między fitness a wielkością sieci neuronowej. Potrzebne więc będą moduły NumPy i Matplotlib. Lider każdej generacji byłby oznaczony 
podczas jazdy po mapie. Przy tworzeniu nowej symulacji, można podać parę parametrów, na przykład to, czy wszystkie samochody startują z punktu 
startowego pod tym samym kątem albo to, czy mapy zmieniają się co parę generacji, by ograniczyć overfitting.
Spróbuję użyć Cythona lub CPythona do optymalizacji wykrywania odległości do ścian przez samochody (podstawa ich poruszania się).
Tryb konsolowy pozwoli zrobić wszystko, co jest dostępne w głównym menu GUI (w którym można zmienić parametry symulacji, uruchomić ją, wczytać 
zapis sieci neuronowych poprzednio wytrenowanych). W menu GUI podczas gry będzie można przejrzeć statystyki i wrócić do menu głównego, a także 
kliknąć samochód, by w rogu zobaczyć jego sieć neuronową z wartościami aktualizowanymi na żywo.
Dodatkowo użyję Regexa, by sparsować na przykład nazwę pliku zawierającego poprzednie dane treningowe, by wyciągnąć z tego na przykład datę zapisu.
Użyję modułu abc, by stworzyć abstrakcyjną klasę Car oraz klasy dziedziczące PlayerCar i ComputerCar - będzie można więc przejechać się samochodem po 
mapie, by je przetestować.
'''

from pyqt_search_bar import SearchBar
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QPushButton, QLabel, QDateTimeEdit, QCheckBox, QFrame
from typing import Optional
from neat_and_pygame import main as start_simulation

WIDTH = 900
HEIGHT = 800

ERROR_WIDTH = 300
ERROR_HEIGHT = 200

MAX_TEXT_HEIGHT = 40

LOG_CHAR_LIMIT = 60

SHOW_SPECIFIC_DETAILS = True

class MainMenu(QMainWindow):
    def __init__(self, app: QApplication, dimensions: Optional[tuple[int, int, int, int]]=None) -> None:
        super().__init__()
        self.app: QApplication = app
        
        self.setWindowTitle("Main Menu")
        
        if dimensions is None:
            dimensions = self.get_centre_dimensions(WIDTH, HEIGHT)
        
        self.setGeometry(*dimensions)
        
        self.setMaximumSize(*dimensions[2:])
        
        self.setup_ui()
    
    def setup_main_layout(self) -> QVBoxLayout:
        main_layout = QVBoxLayout()
        
        self.start_simulation_button = QPushButton("Start Simulation", self)
        self.start_simulation_button.clicked.connect(self.start_simulation)
        main_layout.addWidget(self.start_simulation_button)

        self.make_map_button = QPushButton("Make Map", self)
        self.make_map_button.move(0, 50)
        self.make_map_button.clicked.connect(self.make_map)
        main_layout.addWidget(self.make_map_button)
                
        return main_layout

    def start_simulation(self) -> None:
        start_simulation()

    def make_map(self) -> None:
        print("Making map...")
    
    def create_text_with_label(self, label_text):
        layout = QVBoxLayout()
        
        label = QLabel(label_text)
        layout.addWidget(label)
        
        text = QTextEdit()   
        text.setReadOnly(True)     
        text.setMaximumHeight(MAX_TEXT_HEIGHT)
        
        layout.addWidget(text)
        
        return layout, text
            
    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)     
        
        layout.addLayout(self.setup_main_layout())   
    
    def get_centre_dimensions(self, width, height) -> tuple[int, int, int, int]:   
        primary_screen_dimensions = self.app.primaryScreen().size()
            
        x = primary_screen_dimensions.width() // 2 - width // 2
        y = primary_screen_dimensions.height() // 2 - height // 2
        
        return x, y, width, height
      
if __name__ == "__main__":
    app = QApplication([])
    window = MainMenu(app)
    window.show()
    app.exec_()