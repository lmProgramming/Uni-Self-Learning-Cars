from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

import sys

class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main) -> None:
        Main.setObjectName("Main Menu")
        #Main.resize(*dimensions)

        self.QtStack = QtWidgets.QStackedLayout()

        self.main_menu = QtWidgets.QWidget()
        self.parameters_menu = QtWidgets.QWidget()

        self.Window1UI()
        self.Window2UI()

        self.QtStack.addWidget(self.main_menu)
        self.QtStack.addWidget(self.parameters_menu)

    def Window1UI(self):
        self.main_menu.resize(800, 480)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)    

        #PushButton1#
        self.PushButton1 = QtWidgets.QPushButton()
        self.PushButton1.setText("BUTTON 1")
        layout.addWidget(self.PushButton1)

        #PushButton2#
        self.PushButton2 = QtWidgets.QPushButton()
        self.PushButton2.setText("BUTTON 2")
        layout.addWidget(self.PushButton2)

    def Window2UI(self):
        self.parameters_menu.resize(800, 480)
        self.parameters_menu.setStyleSheet("background: red")