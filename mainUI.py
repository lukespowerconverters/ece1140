import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd
from import_excel import get_sheets
#from create_track_layout import create_track_map

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        ## Add tabs to the home screen
        #  Tab 1 -- Home
        self.home = QWidget()
        self.home.layout = QVBoxLayout()
        
        # self.label = QLabel(self)
        # self.track_map = QPixmap('track layout.png')
        # self.label.setPixmap(self.track_map)

        self.subsection_info = QTableWidget()
        self.subsection_info.setRowCount(2)
        self.subsection_info.setColumnCount(10)
        self.subsection_info.setVerticalHeaderLabels(['Line', 'Section', 'Block #', 'Block Length (m)',
                                                      'Block Grade (%)', 'Speed Limit (km/hr)', 'Elevation',
                                                      'Failure', 'Stop Signal', 'Switch Status'])
        # self.home.layout.addWidget(self.track_map)
        self.home.layout.addWidget(self.subsection_info)

        #  Tab 2 -- Edit Track Layout
        self.edit_tab = QWidget()
        self.edit_tab.layout = QVBoxLayout()

        label = QLabel("Edit Track Layout")
        self.setCentralWidget(label)

        self.add = QPushButton()
        self.edit = QPushButton()
        self.remove = QPushButton()
        self.edit_tab.layout.addWidget(self.add)
        self.edit_tab.layout.addWidget(self.edit)
        self.edit_tab.layout.addWidget(self.remove)

        #  Tab 3 -- Track Information
        self.info = QWidget()
        self.info.layout = QVBoxLayout()

        self.red = QWidget()
        self.green = QWidget()
        self.red.layout = QVBoxLayout()
        self.green.layout = QVBoxLayout()

        self.red_table = QTableWidget()
        self.green_table = QTableWidget()
        self.red.layout.addWidget(self.red_table)
        self.green.layout.addWidget(self.green_table)

        self.tabs3 = QTabWidget()
        self.tabs3.addTab(self.red, 'Red Line')
        self.tabs3.addTab(self.green, 'Green Line')

        self.info.layout.addWidget(self.tabs3)

        #  Add all 3 tabs to the home screen
        self.tabs = QTabWidget()
        self.tabs.setGeometry(QtCore.QRect(6, 9, 741, 481))
        self.tabs.addTab(self.home, 'Home')
        self.tabs.addTab(self.edit_tab, 'Edit Track Layout')
        self.tabs.addTab(self.info, 'Track Information')

        self.layout.addWidget(self.tabs)

    def loadSubsectionData(self, table, line, section, block_num):
        if line == 'red':
            worksheet_name = 'Red Line'
        elif line == 'green':
            worksheet_name = 'Green Line'

        df = pd.read_excel('track_layout.xlsx', worksheet_name)
        # Find matching block number and section ID, get other info
        for j in range(151):
            if (df[1][j] == section) & (df[2][j] == block_num):
                block_length = df[3][j]
                block_grade = df[4][j]
                speed_limit = df[5][j]
                elevation = df[8][j]
                break
        
        # Add current data to the subsection table
        cell = QTableWidgetItem(str(line))
        table.setItem(0, 1, cell)
        cell = QTableWidgetItem(str(section))
        table.setItem(1, 1, cell)
        cell = QTableWidgetItem(str(block_num))
        table.setItem(2, 1, cell)
        cell = QTableWidgetItem(str(block_length))
        table.setItem(3, 1, cell)
        cell = QTableWidgetItem(str(block_grade))
        table.setItem(4, 1, cell)
        cell = QTableWidgetItem(str(speed_limit))
        table.setItem(5, 1, cell)
        cell = QTableWidgetItem(str(elevation))
        table.setItem(6, 1, cell)
        

    def loadExcelData(self, excel_file_dir, worksheet_name, table):
        df = pd.read_excel(excel_file_dir, worksheet_name)
        if df.size == 0:
            return

        df.fillna('', inplace=True)
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                table.setItem(row[0], col_index, tableItem)

        table.setColumnWidth(2, 300)

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = App()

    ## Propagate tables with correct data
    #  Read and take in excel data
    excel_file_path = 'track_layout.xlsx'
    worksheets = get_sheets('track_layout.xlsx')

    #  Add then to the corresponding tables
    myApp.loadExcelData(excel_file_path, worksheets[0], myApp.red_table)
    myApp.loadExcelData(excel_file_path, worksheets[1], myApp.green_table)

    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')
