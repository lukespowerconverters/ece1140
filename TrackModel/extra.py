import os
import sqlite3
import pandas as pd
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog

class track_information:
    lines = []
    stations = []
    switches = []
    filepath = "track_layout_2.0.xlsx"

    db_conn = sqlite3.connect("trackmodel.db")
    c = db_conn.cursor()

    def get_headers_red(self):
        """
        get the column names of the specified table
        """
        sql =  '''SELECT * FROM 'Red Line';'''
        cols = self.c.execute(sql)
        headers = []
        for col in cols.description:
            headers.append(str(col[0]))
        return headers

    def get_headers_green(self):
        """
        get the column names of the specified table
        """
        sql =  '''SELECT * FROM 'Green Line';'''
        cols = self.c.execute(sql)
        headers = []
        for col in cols.description:
            headers.append(str(col[0]))
        return headers

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

    def delete_tables(self):
        ## Delete the existing tables in the database
        self.c.execute("""DROP table IF EXISTS 'Blue Line'""")
        self.c.execute("""DROP table IF EXISTS 'Red Line'""")
        self.c.execute("""DROP table IF EXISTS 'Green Line'""")
        self.c.execute("""DROP table IF EXISTS Trains""")
        self.c.execute("""DROP table IF EXISTS Stations""")
        self.c.execute("""DROP table IF EXISTS Switches""")

    def set_filepath(self, fp):
        self.filepath = fp

    def read_new_data(self):
        ## Clear current database
        self.delete_tables()
        
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

        ## Create a new train, station, and switch table
        self.new_train_table()
        self.new_station_table()
        self.new_switch_table()

        ## Propogate the newly created tables
        self.new_station_list()
        self.new_switch_list()

        ## Get rid of null rows in the line tables
        self.format_line_tables()

    def new_train_table(self):
        check = """DROP table IF EXISTS Trains"""
        self.c.execute(check)
        
        """
        create a new table for the active trains in the SQL database
        """
        sql = ''' CREATE TABLE Trains (
                    TrainID TEXT PRIMARY KEY,
                    Line TEXT,
                    "Current Location" TEXT
                ) '''
        self.c.execute(sql)
        self.db_conn.commit()

    def new_station_table(self):
        check = """DROP table IF EXISTS Stations"""
        self.c.execute(check)

        """
        create a new table in the SQL database for the station list
        """
        sql = ''' CREATE TABLE Stations (
                    StationID TEXT,
                    Line TEXT,
                    "Block Number" INTEGER,
                    "Station Side" TEXT
                  ) '''
        self.c.execute(sql)
        self.db_conn.commit()

    def new_switch_table(self):
        check = """DROP table IF EXISTS Switches"""
        self.c.execute(check)
        
        """
        create a new table in the SQL database for the switches
        """
        sql = ''' CREATE TABLE Switches (
                    SwitchID INTEGER,
                    Line TEXT,
                    "Block 1" INTEGER,
                    "Block 2" INTEGER,
                    "Block 3" INTEGER,
                    "Block 4" INTEGER
                )'''
        self.c.execute(sql)
        self.db_conn.commit()

    def propogate_station_table(self, value):
        """
        propogate the station table with the values from the stations list
        :param value:
        """
        prop =  ''' INSERT INTO
                        Stations (
                            StationID,
                            Line,
                            "Block Number",
                            "Station Side"
                        )
                    VALUES (?,?,?,?); '''
        self.c.execute(prop, value)
        self.db_conn.commit()

    def propogate_switch_table(self, value):
        """
        propogate the switch table with the values from the switches list
        :param value:
        """
        prop =  ''' INSERT INTO
                        Switches (
                            SwitchID,
                            Line,
                            "Block 1",
                            "Block 2",
                            "Block 3",
                            "Block 4"
                        )
                    VALUES (?,?,?,?,?,?); '''
        self.c.execute(prop, value)
        self.db_conn.commit()

    def new_station_list(self):
        self.stations = []
        
        ## Get specified station info from the track info data
        green = """ SELECT
                        Line,
                        "Block Number",
                        Infrastructure,
                        "Station Side"
                    FROM 
                        'Green Line'; """
        red = """ SELECT
                        Line,
                        "Block Number",
                        Infrastructure,
                        "Station Side"
                    FROM 
                        'Red Line'; """

        ## Iterate through retrieved station data
        for i in range(2):
            if (i == 0):
                self.c.execute(red)
            else:
                self.c.execute(green)
        
            infra_info = self.c.fetchall()
            for infra in infra_info:
                ## Get the string value of the Infrastructure column to get station info
                str_infra = str(infra[2]).upper()
                found = str_infra.find("STATION")
                if found != -1:
                    ## Station is at the current block
                    name = str_infra[(found + 9):]

                    ## format name
                    name = name.strip()
                    ## Get rid of switch info, just want station name
                    semi = name.find(";")
                    if semi != -1:
                        name = name[:semi]

                    ## Add station to new SQL station table
                    line = str(infra[0])
                    block_num = int(infra[1])
                    side = str(infra[3])
                    value = (name, line, block_num, side)
                    self.propogate_station_table(value)

                    ## Add station to list
                    self.stations.append(infra)

    def new_switch_list(self):
        self.switches = []
        
        ## Get specified switch info from the track info data
        green = """ SELECT
                        Line,
                        Infrastructure
                    FROM 
                        'Green Line'; """
        red = """ SELECT
                        Line,
                        Infrastructure
                    FROM 
                        'Red Line'; """

        ## Iterate through retrieved switch data
        for i in range(2):
            if (i == 0):
                self.c.execute(red)
            else:
                self.c.execute(green)

            num_switches = 0
            block_1 = 0; block_2 = 0; block_3 = 0; block_4 = 0
            number = 0
            infra_info = self.c.fetchall()
            line = infra_info[0][0]
            for infra in infra_info:
                ## Get the string value of the Infrastructure column to get station info
                str_infra = str(infra[1]).upper()
                found = str_infra.find("SWITCH")
                yard = str_infra.find("YARD")

                if (found != -1):
                    ## Switch is after current block
                    number = num_switches
                    num_switches += 1

                    ## format name
                    switch = str_infra.strip()

                    ## Switch leads to the yard
                    if (yard != -1):
                        ## find each block and corresponding number in switch
                        left_paren = switch.find("(")
                        dash = switch.find("-")
                        block_1 = str(switch[(left_paren + 1):dash])
                        if (block_1 == "YARD"):
                            block_1 = int(0)
                        else:
                            block_1 = int(block_1)

                        right_paren = switch.find(")")
                        block_2 = str(switch[(dash + 1):right_paren])
                        if (block_2 == "YARD"):
                            block_2 = int(0)
                        else:
                            block_2 = int(block_2)

                        block_3 = 0
                        block_4 = 0

                    ## Switch leads to another block
                    elif (found != -1) and (yard == -1):
                        ## find each block and corresponding number in switch
                        left_paren = switch.find("(")
                        dash = switch.find("-")
                        block_1 = int(switch[(left_paren + 1):dash])
                    
                        semi = switch.find(";")
                        block_2 = int(switch[(dash + 1):semi])

                        switch = switch[semi:]
                        dash = switch.find("-")
                        block_3 = int(switch[1:dash])

                        right_paren = switch.find(")")
                        block_4 = int(switch[(dash + 1):right_paren])

                    ## Add switch to new SQL switch table
                    value = (number, line, block_1, block_2, block_3, block_4)
                    self.propogate_switch_table(value)

                    ## Add station to list
                    self.switches.append(infra)

    def format_line_tables(self):
        sqlquery = """ DELETE FROM 'Red Line' WHERE "Block Number" IS NULL; """
        self.c.execute(sqlquery)
        self.db_conn.commit()

        sqlquery = """ DELETE FROM 'Green Line' WHERE "Block Number" IS NULL; """
        self.c.execute(sqlquery)
        self.db_conn.commit()

    def get_block_info(self, line, block):
        line = str(line).lower()
        sql = """"""
        if (line == "red line"):
            sql = """ SELECT * FROM 'Red Line'; """
        elif (line == "green line"):
            sql = """ SELECT * FROM 'Green Line'; """
        
        self.c.execute(sql)
        rows = self.c.fetchall()
        block = int(block)
        value = ()
        for row in rows:
            if (int(row[2]) == block):
                line = row[0]
                block = row[2]
                length = row[3]
                grade = row[4]
                speed_limit = row[5]
                elevation = row[8]
                value = (line, block, length, grade, speed_limit, elevation)
        return value