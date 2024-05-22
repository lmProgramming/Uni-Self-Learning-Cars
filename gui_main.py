from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QCheckBox, QLayout, QHBoxLayout
from maps.map_manager import get_map_names, rename_map, delete_map
from maps.map_maker import main as create_new_map
from typing import List
from scrollable_gallery import WidgetGallery

class UiMain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.QtStack = QtWidgets.QStackedLayout()  # Initialize QStackedLayout
        self.setLayout(self.QtStack)  # Set QStackedLayout as the layout for this widget

    def setupUi(self, Main, dimensions) -> None:
        self.main_menu = QtWidgets.QWidget()
        self.parameters_menu = QtWidgets.QWidget()
        self.map_menu = QtWidgets.QWidget()

        self.main_menu_Ui(dimensions)
        self.parameters_Ui(dimensions)
        self.map_menu_Ui(dimensions)

        self.QtStack.addWidget(self.main_menu)
        self.QtStack.addWidget(self.parameters_menu)
        self.QtStack.addWidget(self.map_menu)

    def main_menu_Ui(self, dimensions) -> None:
        self.main_menu.resize(*dimensions)
                        
        layout = QVBoxLayout()    

        self.default_simulation_button = QtWidgets.QPushButton("Start Default Simulation")
        layout.addWidget(self.default_simulation_button)

        self.parameters_simulation_button = QtWidgets.QPushButton("Start Simulation with Parameters")
        layout.addWidget(self.parameters_simulation_button)
        
        self.map_menu_button = QtWidgets.QPushButton("Maps")
        layout.addWidget(self.map_menu_button)
        
        self.test_ride_button = QtWidgets.QPushButton("Solo Test")
        layout.addWidget(self.test_ride_button)
        
        self.main_menu.setLayout(layout)
        
    def create_top_bar(self, layout, title: str) -> None:
        back_button = QtWidgets.QPushButton("Back")  
        back_button.clicked.connect(self.open_main_menu_screen)             
        title_label = QtWidgets.QLabel(title)      
        
        layout.addWidget(back_button, 100)
        layout.addWidget(title_label, 500)
        
    def parameters_Ui(self, dimensions) -> None:
        self.parameters_menu.resize(*dimensions)
        
        layout = QVBoxLayout()    
        
        top_bar_layout = QHBoxLayout()  
        self.create_top_bar(top_bar_layout, "Parameters")
        layout.addLayout(top_bar_layout)
                        
        options_layout = QGridLayout()

        self.car_count_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        options_layout.addWidget(self.car_count_slider, 0, 0)
        self.car_count_slider.setRange(1, 200)        
        self.car_count_label = QtWidgets.QLabel()       
        self.car_count_slider.valueChanged.connect(self.update_car_count_label)
        self.car_count_slider.setValue(50)
        options_layout.addWidget(self.car_count_label, 0, 1)
        
        self.hidden_layers_count_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        options_layout.addWidget(self.hidden_layers_count_slider, 1, 0)
        self.hidden_layers_count_slider.setRange(0, 10)
        self.hidden_layers_count_label = QtWidgets.QLabel()
        self.hidden_layers_count_slider.valueChanged.connect(self.update_hidden_layers_label)
        self.hidden_layers_count_slider.setValue(1)        
        options_layout.addWidget(self.hidden_layers_count_label, 1, 1)

        self.change_maps_button = QCheckBox()
        options_layout.addWidget(self.change_maps_button, 2, 0)
        options_layout.setAlignment(self.change_maps_button, QtCore.Qt.AlignmentFlag.AlignRight)
        self.change_maps_label = QtWidgets.QLabel("Change Maps")
        options_layout.addWidget(self.change_maps_label, 2, 1)        

        self.starting_map_dropdown = QtWidgets.QComboBox()
        
        options_layout.addWidget(self.starting_map_dropdown, 3, 0)
        map_names: List[str] = get_map_names()
        self.starting_map_dropdown.addItems(map_names)
        self.starting_map_label = QtWidgets.QLabel("Starting Map")
        options_layout.addWidget(self.starting_map_label, 3, 1)
        
        layout.addLayout(options_layout)  
        
        self.parameters_menu.setLayout(layout)    
        
    def map_menu_Ui(self, dimensions) -> None:
        self.map_menu = QtWidgets.QWidget()
        self.map_menu.resize(*dimensions)
        
        layout = QVBoxLayout()    
        
        top_bar_layout = QHBoxLayout()  
        self.create_top_bar(top_bar_layout, "Maps")
        layout.addLayout(top_bar_layout)
        
        self.create_new_map_button = QtWidgets.QPushButton("Create New Map")
        layout.addWidget(self.create_new_map_button)
        
        self.map_gallery = QtWidgets.QWidget()
        layout.addWidget(self.map_gallery)

        map_layout = QGridLayout()
        self.map_gallery.setLayout(map_layout)

        # Get the list of map names
        map_names = get_map_names()

        # Create buttons for each map
        WidgetGallery().create_gallery(map_layout, map_names, 2, 0)
        for i, map_name in enumerate(map_names):
            rename_button = QtWidgets.QPushButton(f"Rename Map {i+1}")
            delete_button = QtWidgets.QPushButton(f"Delete Map {i+1}")

            map_layout.addWidget(rename_button, i, 0)
            map_layout.addWidget(delete_button, i, 1)

            # Connect the buttons to their respective functions
            rename_button.clicked.connect(lambda _, name=map_name: rename_map(name))
            delete_button.clicked.connect(lambda _, name=map_name: delete_map(name))
        
        self.map_menu.setLayout(layout)
        
    def update_car_count_label(self, value) -> None:
        self.car_count_label.setText(f"Car Count: {value}")
        
    def update_hidden_layers_label(self, value) -> None:
        self.hidden_layers_count_label.setText(f"Hidden Layers Count: {value}")
        
    def open_main_menu_screen(self) -> None:
        self.QtStack.setCurrentIndex(0)
        self.setWindowTitle("Main Menu") 
