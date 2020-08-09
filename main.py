
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QWidget
from PyQt5 import QtGui, QtWidgets, uic, QtCore

import sys
import mapper
import hotkeyDialog
import fileIO

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setupUi()

        # TODO: implement proper translation and scaling
        self.zoomLevel = 100
        self.screenOffset = [0, 0]

        self.setMinimumSize(500, 500)


        map = fileIO.parseFile("example.mm")

        self.mapper = mapper.FreeFormMap(map)
        self.mapper.setMinimumSize(500, 500)
        self.setCentralWidget(self.mapper)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.addWidget(QtWidgets.QPushButton())
        self.statusBar.setStyleSheet("background-color: rgb(8,8,8)")

        self.snapAction = QtWidgets.QAction("Toggle Snapping")
        self.snapButton = QtWidgets.QPushButton("Toggle Snapping")
        self.snapButton.clicked.connect(self.toggleSnap)
        self.statusBar.addWidget(self.snapButton)

        self.menuBar = self.menuBar()

        # File menu
        self.fileMenu = QtWidgets.QMenu("File")
        self.menuBar.addMenu(self.fileMenu)
        # Placeholder action
        self.openAction = QtWidgets.QAction("Test", self)
        self.fileMenu.addAction(self.openAction)

        # Help menu
        self.helpMenu = QtWidgets.QMenu("Help")
        self.menuBar.addMenu(self.helpMenu)
        # Hotkeys list
        self.hotkeyAction = QtWidgets.QAction("Hotkeys...", self)
        self.hotkeyAction.triggered.connect(self.showHotkeyDialog)
        self.helpMenu.addAction(self.hotkeyAction)
        self.menuBar.addAction(self.hotkeyAction)

        #self.showHotkeyDialog(None)
    
    def toggleSnap(self, event):
        self.mapper.snapMode = not self.mapper.snapMode
        self.update()

    def showHotkeyDialog(self, event):
        dialog = hotkeyDialog.HotkeyDialog([])
        dialog.exec()

    def setupUi(self):
        self.setWindowTitle('Center')
        self.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pass

def main():
    qapp = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    main()
    