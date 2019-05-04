import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, QWidget,QPushButton, QAction,  QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap


class App1(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 status bar example - pythonspot.com'

        self.initUI()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.statusBar().showMessage('상태바  ')

        okButton = QPushButton('&OK', self)
        cancelButton = QPushButton('Cancel', self)

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        vbox = QVBoxLayout()
        vbox.addWidget(okButton)
        vbox.addWidget(cancelButton)

        self.setLayout(vbox)

        self.center()
        self.resize(1000, 800)
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App1()
    sys.exit(app.exec_())