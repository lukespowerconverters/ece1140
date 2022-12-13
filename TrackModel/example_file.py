from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
 
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons


 
# app = QApplication(sys.argv)
# win = QMainWindow()
# win.setGeometry(400,400,300,300)
# win.setWindowTitle("TrackModel")
  
# button = QPushButton(win)
# button.setText("Import Track Model")
# button.clicked.connect(file_dialog)
# button.move(50,50)
 
# win.show()
# sys.exit(app.exec_())