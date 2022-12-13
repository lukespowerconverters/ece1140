import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog

class track_information:
    lines = []
    filepath = NotImplemented

    db_conn = sqlite3.connect("ece1140/TrackModel/data/trackmodel.db")
    c = db_conn.cursor()

    def file_load(self, widget):
        file, check = QFileDialog.getOpenFileName(
            parent = widget,
            caption = "Select a file",
            directory = os.getcwd(),
            filter = "Microsoft Excel Worksheet (*.xlsx *.xls)"
        )
        trackfile = file
        if check:
            self.set_filepath(trackfile)
            print(trackfile)
        self.read_new_data()

    def set_filepath(self, fp):
        self.filepath = fp

    def read_new_data(self):
        ## Read in the entire excel file, iterate through each sheet
        track_excel_file = pd.ExcelFile(self.filepath)
        num_sheets = len(track_excel_file.sheet_names)

        for sheet in track_excel_file.sheet_names:
            if sheet.find('Line') != -1:
                new_line = pd.read_excel(
                    self.filepath, 
                    sheet_name = sheet,
                    header = 0)
                self.lines.append([sheet, new_line])

        ## Add all lines to the database
        for line in self.lines:
            table_name = line[0]
            table = line[1]
            table.to_sql(table_name, self.db_conn, if_exists='replace', index=False)

        ## Create a new train table
        #new_train_table()

    def new_train_table(self):
        ## Create new table in the SQLite database
        self.c.execute(
            """
            CREATE TABLE Trains (
                TrainID TEXT PRIMARY KEY,
                Line TEXT,
                Location TEXT
            );
            """
        )

    def new_station_list(self):
        stations = []

        self.c.execute(
            """
            SELECT
                Line,
                "Block Number",
                Infrastructure,
                "Station Side"
            FROM 
                'Green Line';
            """
        )

        infra_info = self.c.fetchall()
        for infra in infra_info:
            #print(infra[2])
            str_infra = str(infra[2]).upper()
            found = str_infra.find("STATION")
            if found != -1:
                name = str_infra[(found + 9):]

                ## Get rid of switch info, just want station name
                semi = name.find(";")
                if semi != -1:
                    name = name[:semi]

                ## format
                name = name.strip()
                print(name, " ", str(infra[3]))


# track_info = track_information()
# track_info.read_new_data()
# track_info.new_station_list()