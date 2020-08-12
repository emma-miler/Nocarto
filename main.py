
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QWidget
from PyQt5 import QtGui, QtWidgets, uic, QtCore

import sys
import mapper
import shortcutDialog
import fileIO

# TODO: Make some error handling dialogs

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setupUi()

        # TODO: implement proper translation and scaling
        self.zoomLevel = 100
        self.screenOffset = [0, 0]

        self.setMinimumSize(500, 500)

        self.savedFileName = None

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
        # Open action
        self.openAction = QtWidgets.QAction("Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.openFile)
        self.fileMenu.addAction(self.openAction)

        self.fileMenu.addSeparator()

        # Save action
        self.saveAction = QtWidgets.QAction("Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.saveFile)
        self.fileMenu.addAction(self.saveAction)
        # Save as action
        self.saveAsAction = QtWidgets.QAction("Save as...", self)
        self.saveAsAction.setShortcut("Ctrl+Shift+S")
        self.saveAsAction.triggered.connect(self.saveAsFile)
        self.fileMenu.addAction(self.saveAsAction)
        
        self.fileMenu.addSeparator()

        # Import action
        self.importAction = QtWidgets.QAction("Import...", self)
        self.importAction.setShortcut("Ctrl+Shift+I")
        self.importAction.triggered.connect(self.importFile)
        self.fileMenu.addAction(self.importAction)

        # Help menu
        self.helpMenu = QtWidgets.QMenu("Help")
        self.menuBar.addMenu(self.helpMenu)
        # shortcuts list
        self.shortcutAction = QtWidgets.QAction("Shortcuts...", self)
        self.shortcutAction.triggered.connect(self.showShortcutDialog)
        self.helpMenu.addAction(self.shortcutAction)
        self.menuBar.addAction(self.shortcutAction)    


    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","NoCarto Map Files (*.ncm)", options=options)
        if fileName:
            map = fileIO.openFile(fileName) # Generate a nodelist from the file
            self.deleteMapper() # Remove the current map widget
            self.mapper = mapper.FreeFormMap(map, "freemap") # Create a new map widget and set it as the central widget
            self.setCentralWidget(self.mapper)
            self.savedFileName = fileName # update the filename used when saving
    
    def importFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;FreeMind Files (*.mm)", options=options)
        if fileName:
            map = fileIO.parseFile(fileName) # Generate a nodelist from the file
            self.deleteMapper() # Remove the current map widget
            self.mapper = mapper.FreeFormMap(map, "mindmap") # Create a new map widget and set it as the central widget
            self.setCentralWidget(self.mapper)

    def saveFile(self):
        if self.savedFileName is None: # Check if we already have a known file we can write to, otherwise, open save as dialog
            self.saveAsFile()
        else:
            fileIO.saveFile(self.mapper, self.savedFileName)
    
    def saveAsFile(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        dialog.setDefaultSuffix("ncm")
        dialog.setNameFilter("NoCarto Map (*.ncm)")
        if dialog.exec_() == QtWidgets.QFileDialog.Accepted:
            fileIO.saveFile(self.mapper, dialog.selectedFiles()[0])
            self.savedFileName = dialog.selectedFiles()[0]
    
    
    def deleteMapper(self):
        for node in self.mapper.nodes.values():
            del(node)
        self.mapper.deleteLater()
    
    def toggleSnap(self, event): # TODO: deprecate this, probably
        self.mapper.snapMode = event
        self.update()

    def showShortcutDialog(self, event):
        dialog = shortcutDialog.ShortcutDialog(self.mapper.shortcutList)
        dialog.exec()

    def setupUi(self):
        self.setWindowTitle('NoCarto')
        self.showMaximized()

def main():
    qapp = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    main()
    