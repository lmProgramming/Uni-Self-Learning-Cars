from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QCheckBox
from maps.map_reader import get_map_names
from typing import List

class UiMain(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.QtStack = QtWidgets.QStackedLayout()  # Initialize QStackedLayout
        self.setLayout(self.QtStack)  # Set QStackedLayout as the layout for this widget

    def setupUi(self, Main, dimensions) -> None:
        self.main_menu = QtWidgets.QWidget()
        self.parameters_menu = QtWidgets.QWidget()

        self.main_menu_Ui(dimensions)
        self.parameters_Ui(dimensions)

        self.QtStack.addWidget(self.main_menu)
        self.QtStack.addWidget(self.parameters_menu)

    def main_menu_Ui(self, dimensions) -> None:
        self.main_menu.resize(*dimensions)
                        
        layout = QVBoxLayout()    

        self.default_simulation_button = QtWidgets.QPushButton("Start Default Simulation")
        layout.addWidget(self.default_simulation_button)

        self.parameters_simulation_button = QtWidgets.QPushButton("Start Simulation with Parameters")
        layout.addWidget(self.parameters_simulation_button)
        
        self.test_ride_button = QtWidgets.QPushButton("Solo Test")
        layout.addWidget(self.test_ride_button)
        
        self.main_menu.setLayout(layout)

    def parameters_Ui(self, dimensions) -> None:
        self.parameters_menu.resize(*dimensions)
        
        layout = QGridLayout()

        self.car_count_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(self.car_count_slider, 0, 0)
        self.car_count_slider.setRange(1, 200)        
        self.car_count_label = QtWidgets.QLabel()       
        self.car_count_slider.valueChanged.connect(self.update_car_count_label)
        self.car_count_slider.setValue(50)
        layout.addWidget(self.car_count_label, 0, 1)
        
        self.hidden_layers_count_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Orientation.Horizontal)
        layout.addWidget(self.hidden_layers_count_slider, 1, 0)
        self.hidden_layers_count_slider.setRange(0, 10)
        self.hidden_layers_count_label = QtWidgets.QLabel()
        self.hidden_layers_count_slider.valueChanged.connect(self.update_hidden_layers_label)
        self.hidden_layers_count_slider.setValue(1)        
        layout.addWidget(self.hidden_layers_count_label, 1, 1)

        self.change_maps_button = QCheckBox()
        layout.addWidget(self.change_maps_button, 2, 0)
        layout.setAlignment(self.change_maps_button, QtCore.Qt.AlignmentFlag.AlignRight)
        self.change_maps_label = QtWidgets.QLabel("Change Maps")
        layout.addWidget(self.change_maps_label, 2, 1)        

        self.starting_map_dropdown = QtWidgets.QComboBox()
        
        layout.addWidget(self.starting_map_dropdown, 3, 0)
        map_names: List[str] = get_map_names()
        self.starting_map_dropdown.addItems(map_names)
        self.starting_map_label = QtWidgets.QLabel("Starting Map")
        layout.addWidget(self.starting_map_label, 3, 1)

        self.parameters_menu.setLayout(layout)
        
    def update_car_count_label(self, value) -> None:
        self.car_count_label.setText(f"Car Count: {value}")
        
    def update_hidden_layers_label(self, value) -> None:
        self.hidden_layers_count_label.setText(f"Hidden Layers Count: {value}")
