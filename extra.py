from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pandas as pd
from subsection import Ui_SubsectionWindow

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class Ui_EditTrackWindow(object):
    def openSubWindow(self):
        self.window = QMainWindow()
        self.ui = Ui_SubsectionWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, EditTrackWindow):
        EditTrackWindow.setObjectName("EditTrackWindow")
        EditTrackWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(EditTrackWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 9, 271, 351))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(310, 10, 271, 351))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.tableWidget = QtWidgets.QTableWidget(self.verticalLayoutWidget_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(9)
        self.tableWidget.setVerticalHeaderLabels(['','Line', 'Section', 'Block #', 'Block Length (m)',
                                                  'Block Grade (%)', 'Speed Limit (km/hr)', 'Elevation',
                                                  'Failure', 'Stop Signal', 'Switch Status'])
        self.verticalLayout_2.addWidget(self.tableWidget)
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 20, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(600, 60, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        EditTrackWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(EditTrackWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        EditTrackWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(EditTrackWindow)
        self.statusbar.setObjectName("statusbar")
        EditTrackWindow.setStatusBar(self.statusbar)

        self.retranslateUi(EditTrackWindow)
        QtCore.QMetaObject.connectSlotsByName(EditTrackWindow)

    def retranslateUi(self, EditTrackWindow):
        _translate = QtCore.QCoreApplication.translate
        EditTrackWindow.setWindowTitle(_translate("EditTrackWindow", "EditTrackWindow"))
        self.label.setText(_translate("EditTrackWindow", "TextLabel"))
        self.pushButton.setText(_translate("EditTrackWindow", "OK"))
        self.pushButton_2.setText(_translate("EditTrackWindow", "Cancel"))

    def loadSubsectionData(self, table, line, section, block_num):
        if line == 'red':
            worksheet_name = 'Red Line'
        elif line == 'green':
            worksheet_name = 'Green Line'

        df = pd.read_excel('track_layout.xlsx', worksheet_name)
        
        # Add current data to the subsection table
        cell = QTableWidgetItem(str(line))
        table.setItem(0, 1, cell)
        cell = QTableWidgetItem(str(section))
        table.setItem(1, 1, cell)
        cell = QTableWidgetItem(str(block_num))
        table.setItem(2, 1, cell)

    def showResults(self):
        self.close()
        self.openSubWindow()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    EditTrackWindow = QtWidgets.QMainWindow()
    ui = Ui_EditTrackWindow()
    ui.setupUi(EditTrackWindow)
    ui.loadSubsectionData(ui.tableWidget, 'red', 'A', 3)
    EditTrackWindow.show()
    sys.exit(app.exec_())