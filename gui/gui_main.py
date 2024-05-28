from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QCheckBox, QHBoxLayout, QBoxLayout, QWidget, QSpacerItem, QSizePolicy
from map_scripts.map_tools import get_map_names
from neat_training import main as start_simulation
from map_scripts.map_maker import create_new_map as create_new_map
from neat_save_load import get_saved_checkpoints
from simulation.simulation_config import SimulationConfig
from typing import List
from gui.map_gallery import MapGallery
from gui.saved_training_gallery import SavedTrainingGallery
from gui.checkable_combo_box import CheckableComboBox

class UiMain(QtWidgets.QWidget):
    def __init__(self, open_main_menu_screen):
        super().__init__()
        self.QtStack = QtWidgets.QStackedLayout()  # Initialize QStackedLayout
        self.setLayout(self.QtStack)  # Set QStackedLayout as the layout for this widget
        
        self.open_main_menu_screen = open_main_menu_screen

    def setupUi(self, Main, dimensions) -> None:
        self.main_menu = QtWidgets.QWidget()
        
        self.parameters_menu = UiParametersMenu(self.create_top_bar(QHBoxLayout(), "Parameters"), dimensions)
        self.map_menu = MapMenu(self.create_top_bar(QHBoxLayout(), "Maps"), dimensions)
        self.saved_training_menu = UiLoadTraining(self.create_top_bar(QHBoxLayout(), "Saved Training"), dimensions)

        self.main_menu_Ui(dimensions)       

        self.QtStack.addWidget(self.main_menu)
        self.QtStack.addWidget(self.parameters_menu)
        self.QtStack.addWidget(self.map_menu)
        self.QtStack.addWidget(self.saved_training_menu)

    def main_menu_Ui(self, dimensions) -> None:
        self.main_menu.resize(*dimensions)
                        
        layout = QVBoxLayout()    

        self.default_simulation_button = QtWidgets.QPushButton("Start Default Simulation")
        layout.addWidget(self.default_simulation_button)

        self.parameters_simulation_button = QtWidgets.QPushButton("Start Simulation with Parameters")
        layout.addWidget(self.parameters_simulation_button)
        
        self.map_menu_button = QtWidgets.QPushButton("Maps")
        layout.addWidget(self.map_menu_button)
                
        self.load_saved_training_button = QtWidgets.QPushButton("Load Saved Training Data")
        layout.addWidget(self.load_saved_training_button)
        
        self.test_ride_button = QtWidgets.QPushButton("Solo Test")
        layout.addWidget(self.test_ride_button)
        
        self.main_menu.setLayout(layout)
        
    def create_top_bar(self, layout: QBoxLayout, title: str) -> QBoxLayout:
        top_bar = QtWidgets.QWidget()
        top_bar_layout = QHBoxLayout(top_bar)

        back_button = QtWidgets.QPushButton("Back")  
        back_button.clicked.connect(self.open_main_menu_screen)             

        title_label = QtWidgets.QLabel(title)  
        title_label.setStyleSheet("font-weight: bold;")

        top_bar_layout.addWidget(back_button, 100)
        top_bar_layout.addWidget(title_label, 500)

        top_bar.setFixedHeight(50)

        layout.addWidget(top_bar)
        layout.setStretch(0, 0)

        return layout
        
class MapMenu(QtWidgets.QWidget):
    def __init__(self, top_bar_layout, dimensions) -> None:
        super().__init__()
        self.resize(*dimensions)
        
        layout = QVBoxLayout()    
        
        layout.addLayout(top_bar_layout)
        
        self.create_new_map_button = QtWidgets.QPushButton("Create New Map")
        self.create_new_map_button.clicked.connect(self.create_new_map)        
        layout.addWidget(self.create_new_map_button)
        
        self.map_gallery = QtWidgets.QWidget()
        layout.addWidget(self.map_gallery)

        map_layout = QGridLayout()
        self.map_gallery.setLayout(map_layout)

        map_names: List[str] = get_map_names()

        map_gallery_dimensions = [10, dimensions[1] // 2, dimensions[0] * 9 // 10, dimensions[1] // 2]
        self.map_gallery = MapGallery(map_gallery_dimensions)
        self.map_gallery.populateGallery(map_names)
            
        layout.addWidget(self.map_gallery)
        
        self.setLayout(layout)
        
    def create_new_map(self) -> None:
        create_new_map()
        
class FixedHeightWidget(QWidget):
    def __init__(self, height, parent=None):
        super().__init__(parent)
        self.setFixedHeight(height)
        
BAR_HEIGHT = 50
        
class UiParametersMenu(QtWidgets.QWidget):
    def __init__(self, top_bar_layout, dimensions) -> None:
        super().__init__()
        self.resize(*dimensions)
        
        layout = QVBoxLayout()    
        fixed_height_widget = FixedHeightWidget(BAR_HEIGHT)
        fixed_height_widget.setLayout(top_bar_layout)
        layout.addWidget(fixed_height_widget)
                             
        options_layout = QVBoxLayout()
        
        options_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.car_count_label = QtWidgets.QLabel()
        options_layout.addWidget(self.car_count_label)        
        self.car_count_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        self.car_count_slider.valueChanged.connect(self.update_car_count_label)
        self.car_count_slider.setValue(50)
        self.car_count_slider.setRange(2, 200)               
        options_layout.addWidget(self.car_count_slider)               
        
        self.hidden_layers_count_label = QtWidgets.QLabel()
        options_layout.addWidget(self.hidden_layers_count_label)        
        self.hidden_layers_count_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        self.hidden_layers_count_slider.setRange(0, 10)
        self.hidden_layers_count_slider.valueChanged.connect(self.update_hidden_layers_label)
        self.hidden_layers_count_slider.setValue(1)        
        options_layout.addWidget(self.hidden_layers_count_slider)

        self.random_angle_label = QtWidgets.QLabel("Random Angle")
        options_layout.addWidget(self.random_angle_label)   
        self.random_angle = QCheckBox()
        self.random_angle.setChecked(True)
        options_layout.addWidget(self.random_angle)
        
        self.map_pool_label = QtWidgets.QLabel("Map Pool")
        options_layout.addWidget(self.map_pool_label)
        self.map_pool = CheckableComboBox()        
        map_names: List[str] = get_map_names()
        self.map_pool.addItems(map_names)
        self.map_pool.on_selection_changed = self.update_start_button_state
        options_layout.addWidget(self.map_pool)
        
        options_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
                                        
        layout.addLayout(options_layout)                
                
        self.start_parameters_simulation_button = QtWidgets.QPushButton("Start Simulation")
        self.start_parameters_simulation_button.clicked.connect(self.start_simulation_with_parameters)
        self.start_parameters_simulation_button.setFixedHeight(BAR_HEIGHT)
        layout.addWidget(self.start_parameters_simulation_button)
                
        self.update_start_button_state()
        
        self.setLayout(layout)    
        
    @property
    def maps(self) -> CheckableComboBox:
        return self.map_pool.currentData()
    
    @property
    def has_maps(self) -> bool:
        return len(self.maps) > 0
        
    def update_start_button_state(self, *args) -> None:
        has_maps = self.has_maps
        self.start_parameters_simulation_button.setEnabled(has_maps)
        if not has_maps:
            self.start_parameters_simulation_button.setToolTip("Add at least one map to map pool to start the simulation.")
        else:
            self.start_parameters_simulation_button.setToolTip("")
    
    def update_car_count_label(self, value) -> None:
        self.car_count_label.setText(f"Car Count: {value}")
        
    def update_hidden_layers_label(self, value) -> None:
        self.hidden_layers_count_label.setText(f"Hidden Layers Count: {value}")
        
    def start_simulation_with_parameters(self) -> None:
        config = SimulationConfig(
            num_iterations=100, 
            map_pool=self.map_pool.currentData(), 
            hidden_layers=self.hidden_layers_count_slider.value(), 
            random_angle=self.random_angle.isChecked(),
            ray_count=8,
            initial_population=self.car_count_slider.value())
        start_simulation(config)
        
class UiLoadTraining(QtWidgets.QWidget):
    def __init__(self, top_bar_layout, dimensions) -> None:
        super().__init__()
        self.resize(*dimensions)
        
        layout = QVBoxLayout()    
        fixed_height_widget = FixedHeightWidget(BAR_HEIGHT)
        
        top_bar_layout.addStretch(1)
        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.populate_gallery)
        top_bar_layout.addWidget(self.refresh_button)
        
        fixed_height_widget.setLayout(top_bar_layout)
        layout.addWidget(fixed_height_widget)
        
        training_gallery_dimensions = [10, dimensions[1] // 2, dimensions[0] * 9 // 10, dimensions[1] // 2]                             
        self.saved_training_gallery = SavedTrainingGallery(training_gallery_dimensions)
        self.populate_gallery()
        
        layout.addWidget(self.saved_training_gallery)
        self.setLayout(layout)    
        
    def populate_gallery(self) -> None:
        self.saved_training_gallery.populateGallery(get_saved_checkpoints())
        
def ui_element_with_label_hlayout(label: str, element: QWidget) -> QHBoxLayout:
    layout = QHBoxLayout()
    layout.addWidget(QtWidgets.QLabel(label))
    layout.addWidget(element)
    return layout