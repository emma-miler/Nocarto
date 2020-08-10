
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QWidget
from PyQt5 import QtGui, QtWidgets, uic, QtCore

import sys
import mapper
import shortcutDialog
import fileIO

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setupUi()

        # TODO: implement proper translation and scaling
        self.zoomLevel = 100
        self.screenOffset = [0, 0]

        self.setMinimumSize(500, 500)


        #map = fileIO.parseFile("test.mm")

        #self.mapper = mapper.FreeFormMap(map)
        self.mapper = mapper.FreeFormMap()
        self.mapper.setMinimumSize(500, 500)
        self.setCentralWidget(self.mapper)

        # Setting up statusbar
        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("background-color: rgb(8,8,8)")

        # Toggle debug rendering
        # TODO: make this change render modes
        self.debugAction = QtWidgets.QAction("Debug Rendering")
        self.debugBox = QtWidgets.QCheckBox("Debug Rendering")
        self.debugBox.clicked.connect(lambda event: print(event))
        self.statusBar.addWidget(self.debugBox)

        # Toggle snapping button
        self.snapAction = QtWidgets.QAction("Toggle Snapping")
        self.snapBox = QtWidgets.QCheckBox("Toggle Snapping")
        self.snapBox.clicked.connect(lambda event: self.toggleSnap(event))
        self.statusBar.addWidget(self.snapBox)


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
        # shortcuts list
        self.shortcutAction = QtWidgets.QAction("Shortcuts...", self)
        self.shortcutAction.triggered.connect(self.showShortcutDialog)
        self.helpMenu.addAction(self.shortcutAction)
        self.menuBar.addAction(self.shortcutAction)

        self.shortcutList = []

        # Create node
        self.createNode = QtWidgets.QAction("Create Node", self)
        self.createNode.setShortcut("Return")
        self.createNode.triggered.connect(self.mapper.createNewNode)
        self.addAction(self.createNode)
        self.shortcutList.append(self.createNode)

        # Edit node
        self.editNode = QtWidgets.QAction("Edit Node", self)
        self.editNode.setShortcut("Space")
        self.editNode.triggered.connect(lambda: self.mapper.setEditNode(True))
        self.addAction(self.editNode)
        self.shortcutList.append(self.editNode)

        #self.showShortcutDialog(None)
    
    def toggleSnap(self, event):
        self.mapper.snapMode = event
        self.update()

    def showShortcutDialog(self, event):
        dialog = shortcutDialog.ShortcutDialog(self.shortcutList)
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
    