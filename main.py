from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import * 
from PyQt5 import uic
import sys, time, os, random

#Variables globales 
BUFFER_SIZE = 100
usedBuffer = 0
mutex = QtCore.QMutex()

#Clase MainWindow es el hilo principal de la aplicación
class MainWindow(QtWidgets.QMainWindow):
    
  #En el constructor cargamos la UI, inicializamos las señales de cada componente
  #y se inicializan los semaforos de cada elemento
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    ui_path = os.path.dirname(os.path.abspath(__file__))
    self.ui = uic.loadUi(os.path.join(ui_path, 'mainWindow.ui'), self)
    
    self.iniciar.clicked.connect(self.run_producer_consumer)
    
    self.semaphores_UI_init()
    
    self.bufferProgressBar.setStyleSheet("QProgressBar::Chunk"
                                    "{"
                                    "background-image: url(progress_bkgrnd.png);"
                                    "margin: 1px;"
                                    "}")
  
  #Produce es el método que bloquea el buffer con exclusión mutua
  #para agregar un "recurso" a la barra
  def produce(self, ammount):
    global usedBuffer
    mutex.lock() #Se hace lock del recurso para que no pueda ser accedido por otros hilos
    #Se hace toggle de los semáforos para efecto gráfico
    self.turn_producer_ON() 
    self.turn_consumer_OFF()
    #Validamos si el buffer está lleno para agregar un recurso o no
    if usedBuffer != BUFFER_SIZE:
      usedBuffer += ammount
      
    #Se "agrega" el recurso al buffer
    self.bufferProgressBar.setValue(usedBuffer)
    mutex.unlock()
    
  #Consume es el método que bloquea el buffer con exclusión mutua
  #para consumir un "recurso" a la barra
  def consume(self, ammount):
    global usedBuffer
    mutex.lock()
    self.turn_producer_OFF()
    self.turn_consumer_ON()
    if usedBuffer != 0:
      usedBuffer += ammount
    self.bufferProgressBar.setValue(usedBuffer)
    mutex.unlock()

  #Esta función es la que inicializa las señales de cada hilo y posteriormente los inicia
  #Se dispara pulsando el botón de "Iniciar Productor-Consumidor"
  def run_producer_consumer(self):
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
    
  #A partir de aquí todos los métodos son para togglear los semáforos
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
    
#La clase del productor extiende de QThread y únicamente emite un 10 que
#Se suma al buffer para representar un recurso producido
class Producer(QtCore.QThread):
  #inicializamos señales
  progress = QtCore.pyqtSignal(int)
  full = QtCore.pyqtSignal()
  not_full = QtCore.pyqtSignal()
  
  global usedBuffer
  
  def __init__(self, parent=None):
    super(Producer, self).__init__(parent)
  
  def run(self):
      while True:
        #Se valida que el buffer no esté lleno para poder producir
        if usedBuffer != BUFFER_SIZE:
          # print(usedBuffer)
          time.sleep(random.uniform(0,1))
          self.not_full.emit()
          #Además se emiten las señales para togglear los semáforos del buffer
          self.progress.emit(10)
        else:
          self.full.emit()
      return

#La clase del productor extiende de QThread y únicamente emite un -10 que
#Se suma al buffer para representar un recurso consumido
class Consumer(QtCore.QThread):
  #inicializamos señales
  progress = QtCore.pyqtSignal(int)
  empty = QtCore.pyqtSignal()
  not_empty = QtCore.pyqtSignal()
  
  global usedBuffer
  
  def __init__(self, parent=None):
    super(Consumer, self).__init__(parent)
    
  def run(self):
    while True:
      #Se valida que el buffer no esté vacío para poder consumir
      if usedBuffer != 0:
        # print(usedBuffer)
        time.sleep(random.uniform(0,1))
        self.not_empty.emit()
        self.progress.emit(-10)
      else:
        self.empty.emit()

#La función main ejecuta la app de pyqt
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())
