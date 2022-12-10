import pandas as pd
import sys
from PyQt5.QtWidgets import *

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