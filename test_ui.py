from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.layout = QVBoxLayout()

        # Add three tabs
        self.tabs = QTabWidget(self.centralwidget)
        
        self.tab1 = QWidget()
        self.table1 = QTableWidget(self.tab1)

        self.tab2 = QWidget()
        self.h = QWidget()
        self.g = QWidget()
        self.tabs2 = QTabWidget(self.tab2)
        self.tabs2.setGeometry(QtCore.QRect(10, 60, 491, 461))
        self.tabs2.addTab(self.h, 'h')
        self.tabs2.addTab(self.g, 'g')

        self.tab3 = QWidget()

        self.tabs.setGeometry(QtCore.QRect(10, 9, 741, 481))
        self.tabs.addTab(self.tab1, '1')
        self.tabs.addTab(self.tab2, '2')
        self.tabs.addTab(self.tab3, '3')

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.sub_table = QTableWidget(self)
        # self.layout.addWidget(self.sub_table)
        # self.track_map = QPixmap('track layout.png')
        # self.layout.addWidget(self.track_map)

        # # Available inputs to test
        # self.subsection_info.setRowCount(2)
        # self.subsection_info.setColumnCount(10)
        # self.subsection_info.setVerticalHeaderLabels(['Line', 'Section', 'Block #', 'Commanded Speed',
        #                                               'Commanded Authority', 'Switch Control Decision',
        #                                               'Light Signal Control Decision', 'Gate Control Decision'])

        
if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())