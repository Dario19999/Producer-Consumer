from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import * 
from PyQt5 import uic
import sys, time, os

class MainWindow(QtWidgets.QMainWindow):
    
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    ui_path = os.path.dirname(os.path.abspath(__file__))
    self.ui = uic.loadUi(os.path.join(ui_path, 'mainWindow.ui'), self)
        
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())
