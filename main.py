from ast import Global
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import * 
from PyQt5 import uic
import sys, time, os, random

BUFFER_SIZE = 100
usedBuffer = 0
mutex = QtCore.QMutex()

class MainWindow(QtWidgets.QMainWindow):
    
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    ui_path = os.path.dirname(os.path.abspath(__file__))
    self.ui = uic.loadUi(os.path.join(ui_path, 'mainWindow.ui'), self)
    
    self.iniciar.clicked.connect(self.run_simulation)
    
    self.semaphores_UI_init()
    
  def produce(self, ammount):
    global usedBuffer
    mutex.lock()
    print("produce", ammount)
    self.turn_producer_ON()
    self.turn_consumer_OFF()
    usedBuffer += ammount
    self.bufferProgressBar.setValue(usedBuffer)
    mutex.unlock()
    
  def consume(self, ammount):
    global usedBuffer
    mutex.lock()
    print("consume", ammount)
    self.turn_producer_OFF()
    self.turn_consumer_ON()
    usedBuffer += ammount
    self.bufferProgressBar.setValue(usedBuffer)
    mutex.unlock()

  def run_simulation(self):
    self.producer = Producer(parent=None)
    self.consumer = Consumer(parent=None)
    
    self.producer.finished.connect(self.producer.terminate)
    self.producer.progress.connect(self.produce)
    self.producer.full.connect(self.turn_buffer_OFF)
    self.producer.not_full.connect(self.turn_buffer_ON)
    
    self.consumer.finished.connect(self.consumer.terminate)
    self.consumer.progress.connect(self.consume)
    self.consumer.empty.connect(self.turn_buffer_OFF)
    self.consumer.not_empty.connect(self.turn_buffer_ON)
    
    self.producer.start()
    self.consumer.start()

    self.iniciar.setEnabled(False)
    
      
  def semaphores_UI_init(self):
    self.productorOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.productorOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.consumidorOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.consumidorOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.bufferOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.bufferOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
  
  def turn_producer_ON(self):
    self.productorOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: rgb(14, 216, 31);"
                                    "}")
    self.productorOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    
  def turn_producer_OFF(self):
    self.productorOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.productorOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: rgb(255, 0, 0);"
                                    "}")
    
  def turn_consumer_ON(self):
    self.consumidorOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: rgb(14, 216, 31);"
                                    "}")
    self.consumidorOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    
  def turn_consumer_OFF(self):
    self.consumidorOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.consumidorOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: rgb(255, 0, 0);"
                                    "}")    
  
  def turn_buffer_ON(self):
    self.bufferOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: rgb(14, 216, 31);"
                                    "}")
    self.bufferOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")    
  
  def turn_buffer_OFF(self):
    self.bufferOn.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: black;"
                                    "}")
    self.bufferOff.setStyleSheet("QGroupBox"
                                    "{"
                                    "background-color: rgb(255, 0, 0);"
                                    "}")   
    
class Producer(QtCore.QThread):
  
  progress = QtCore.pyqtSignal(int)
  full = QtCore.pyqtSignal()
  not_full = QtCore.pyqtSignal()
  
  global usedBuffer
  
  def __init__(self, parent=None):
    super(Producer, self).__init__(parent)
  
  def run(self):
      while True:
        if usedBuffer != BUFFER_SIZE:
          time.sleep(random.uniform(0,1))
          self.not_full.emit()
          self.progress.emit(10)
        else:
          self.full.emit()
      return

class Consumer(QtCore.QThread):
  
  progress = QtCore.pyqtSignal(int)
  empty = QtCore.pyqtSignal()
  not_empty = QtCore.pyqtSignal()
  
  global usedBuffer
  
  def __init__(self, parent=None):
    super(Consumer, self).__init__(parent)
    
  def run(self):
    while True:
      if usedBuffer != 0:
        time.sleep(random.uniform(0,1))
        self.not_empty.emit()
        self.progress.emit(-10)
      else:
        self.empty.emit()

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())
