
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDesktopWidget, QWidget
from PyQt5 import QtGui, QtWidgets, uic, QtCore

import sys
import mapper

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__()

        self.setupUi()

        self.zoomLevel = 100
        self.screenOffset = [0, 0]

        self.setMinimumSize(500, 500)


        #self.layout = QtWidgets.QVBoxLayout()
        #self.newWidget = QtWidgets.QMdiArea()
        self.mapper = mapper.FreeFormMap()
        self.mapper.setMinimumSize(500, 500)
        #self.newWidget.setLayout(self.layout)
        self.setCentralWidget(self.mapper)

        #self.newWidget.documentMode()

        #self.canvas = QtWidgets.QFrame()
        #self.newWidget.addSubWindow(self.canvas)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.addWidget(QtWidgets.QPushButton())
        self.statusBar.setStyleSheet("background-color: rgb(8,8,8)")

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
    