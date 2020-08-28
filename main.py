from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QWidget
from PyQt5 import QtGui, QtWidgets, QtCore

import sys
import mapper
import shortcutDialog
import fileIO

# TODO: Make some error handling dialogs
# TODO: Make Edge objects properly serialized and add them to the save/load routine
# TODO: Add user settings
# TODO: Editable shortcuts
# TODO: implement proper translation and scaling
# TODO: Add grid snapping feature?

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.parent=parent

        #self.setupUi()

        self.zoomLevel = 100
        self.screenOffset = [0, 0]

        self.setMinimumSize(500, 500)

        self.savedFileName = None

        self.setupUi()

        #map = fileIO.parseFile("test.mm")

        self.newWidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.newWidget.setLayout(self.layout)



        #self.mapper = mapper.FreeFormMap(map)
        self.mapper = mapper.FreeFormMap(parent=self)
        #self.mapper.setMinimumSize(1000, 1000)

        self.setCentralWidget(self.mapper)
        self.newWidget.setStyleSheet("background-color: blue")

        #self.layout.addWidget(self.mapper)
        #self.layout.addWidget(self.listView)

        # Setting up statusbar
        self.statusBar = QtWidgets.QStatusBar(parent=self)
        self.setStatusBar(self.statusBar)
        self.statusBar.setStyleSheet("background-color: rgb(8,8,8)")

        # Toggle debug rendering
        # TODO: make this change render modes
        self.debugAction = QtWidgets.QAction("Enable AntiAliasing")
        self.debugBox = QtWidgets.QCheckBox("Enable AntiAliasing")
        self.debugBox.clicked.connect(self.setMapperAA)
        self.statusBar.addWidget(self.debugBox)
        self.debugBox.click()

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


        # Edit menu
        self.editMenu = QtWidgets.QMenu("Edit")
        self.menuBar.addMenu(self.editMenu)

        # Undo action
        self.undoAction = QtWidgets.QAction("Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.undoAction.triggered.connect(self.undo)
        self.editMenu.addAction(self.undoAction)

        # Redo action
        self.redoAction = QtWidgets.QAction("Redo", self)
        self.redoAction.setShortcut("Ctrl+Y")
        self.redoAction.triggered.connect(self.redo)
        self.editMenu.addAction(self.redoAction)


        # Help menu
        self.helpMenu = QtWidgets.QMenu("Help")
        self.menuBar.addMenu(self.helpMenu)
        # shortcuts list
        self.shortcutAction = QtWidgets.QAction("Shortcuts...", self)
        self.shortcutAction.triggered.connect(self.showShortcutDialog)
        self.helpMenu.addAction(self.shortcutAction)
        self.menuBar.addAction(self.shortcutAction)

        self.shortcutList = []

        # TODO: add some of these to the edit menu

        # Create node
        self.createNode = QtWidgets.QAction("Create Node", self)
        self.createNode.setShortcut("Return")
        self.createNode.triggered.connect(self.mapperCreateNode)
        self.addAction(self.createNode)
        self.shortcutList.append(self.createNode)

        # Edit node
        self.editNode = QtWidgets.QAction("Edit Node", self)
        self.editNode.setShortcut("Space")
        self.editNode.triggered.connect(self.mapperEditNode)
        self.addAction(self.editNode)
        self.shortcutList.append(self.editNode)

        # Delete node
        self.deleteNode = QtWidgets.QAction("Delete Node", self)
        self.deleteNode.setShortcut("Delete")
        self.deleteNode.triggered.connect(self.mapperDeleteNode)
        self.addAction(self.deleteNode)
        self.shortcutList.append(self.deleteNode)

    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","NoCarto Map Files (*.ncm)", options=options)
        if fileName:
            newMap = fileIO.openFile(fileName) # Generate a nodelist from the file
            self.deleteMapper() # Remove the current map widget
            self.mapper = mapper.FreeFormMap(newMap, "freemap") # Create a new map widget and set it as the central widget
            self.setCentralWidget(self.mapper)
            self.savedFileName = fileName # update the filename used when saving
            self.setMapperAA(self.debugBox.isChecked())
    
    def importFile(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;FreeMind Files (*.mm)", options=options)
        if fileName:
            newMap = fileIO.parseFile(fileName) # Generate a nodelist from the file
            self.deleteMapper() # Remove the current map widget
            self.mapper = mapper.FreeFormMap(newMap, "mindmap") # Create a new map widget and set it as the central widget
            self.setCentralWidget(self.mapper)
            self.setMapperAA(self.debugBox.isChecked())

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
            node.setParent(None)
        self.mapper.deleteLater()

    # Important notice:
    # The following functions are linked to QActions, and are simply to pass on a signal to the mapper
    # The reason they are separate functions is because the mapper object can be destroyed
    # If the mapper is replaced, the reference to the object is not updated in the actions.
    # This means that the action will try to access a non-existent object, crashing the program
    
    def mapperCreateNode(self):
        self.mapper.handleAction("createNode")

    def mapperEditNode(self):
        self.mapper.handleAction("editNode")

    def mapperDeleteNode(self):
        self.mapper.handleAction("deleteNode")

    def setMapperAA(self, event): 
        self.mapper.enableAA = event
        #self.mapper.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing, event)
        self.update() # redraw screen

    def showShortcutDialog(self, event):
        dialog = shortcutDialog.ShortcutDialog(self.shortcutList)
        dialog.exec()

    def undo(self):
        self.mapper.undo()

    def redo(self):
        self.mapper.redo()

    def setupUi(self):
        self.setWindowTitle('NoCarto')
        frameGm = self.frameGeometry()
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(0).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        self.showMaximized()

def main():
    qapp = QApplication(sys.argv)
    gui = MainWindow()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    main()
    