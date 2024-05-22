from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:")
        if okPressed and text != '':
            print(text)

if __name__ == '__main__':
    app = QApplication([])
    ex = Example()
    app.exec_()