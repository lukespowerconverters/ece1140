import sqlite3
import pandas as pd

#class track_info:
lines = []

db_conn = sqlite3.connect("ece1140/TrackModel/data/trackmodel.db")
c = db_conn.cursor()

def read_new_data():
    ## Read in the entire excel file, iterate through each sheet
    track_excel_file = pd.ExcelFile('ece1140/TrackModel/track_layout_2.0.xlsx')
    num_sheets = len(track_excel_file.sheet_names)

    for sheet in track_excel_file.sheet_names:
        if sheet.find('Line') != -1:
            new_line = pd.read_excel(
                'ece1140/TrackModel/track_layout_2.0.xlsx', 
                sheet_name = sheet,
                header = 0)
            lines.append([sheet, new_line])

    ## Add all lines to the database
    for line in lines:
        table_name = line[0]
        table = line[1]
        table.to_sql(table_name, db_conn, if_exists='replace', index=False)

    ## Create a new train table
    #new_train_table()

def new_train_table():
    ## Create new table in the SQLite database
    c.execute(
        """
        CREATE TABLE Trains (
            TrainID TEXT PRIMARY KEY,
            Line TEXT,
            Location TEXT
        );
        """
    )

def new_station_list():
    stations = []

    c.execute(
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
    infra_info = c.fetchall()
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

read_new_data()
new_station_list()