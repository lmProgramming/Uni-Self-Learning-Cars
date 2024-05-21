from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

from tt import Ui_Main

class Main(QMainWindow, Ui_Main):
    def __init__(self, app, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.PushButton1.clicked.connect(self.OpenWindow1)
        self.PushButton2.clicked.connect(self.OpenWindow2)

    def OpenWindow1(self):
        self.QtStack.setCurrentIndex(1)

    def OpenWindow2(self):
        self.QtStack.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    showMain = Main(app)
    sys.exit(app.exec_())