### TESTING CODE ###
from trackmodel import TrackModel
from extra import track_information
track = TrackModel()



### UNIT TESTS FOR THE TRACK MODEL ###

#*****************************************
# Load track model
#*****************************************

## Test use case
file = track_information()
file.set_filepath('ece1140/TrackModel/track_layout_2.0.xlsx')

## Import track model layout data file
def get_file():
    file.read_new_data()
    sql_query = """SELECT name FROM sqlite_master WHERE type='table'"""
    file.c.execute(sql_query)
    tables = file.c.fetchall()

    # Correct number of data tables created
    assert len(tables) == 6, "Correct number of tables created in local SQL database is 6"

    # Table data entered correctly

get_file()

## Delete all tables in the database
def clear_db():
    file.read_new_data()
    file.delete_tables()

    sql_query = """SELECT name FROM sqlite_master WHERE type='table'"""
    file.c.execute(sql_query)
    tables = file.c.fetchall()

    # Correct number of data tables created
    assert len(tables) == 0, "Correct number of tables created in local SQL database is 0"

clear_db()

## Import station data into SQL tables
def get_station_info():
    file.read_new_data()
    sql_query = """SELECT * FROM Stations"""
    file.c.execute(sql_query)
    stations = file.c.fetchall()

    # Correct number of stations in the table
    assert len(stations) == 26, "Correct number of stations is 26"

get_station_info()

## Import switch data into SQL tables
def get_switch_info():
    file.read_new_data()
    sql_query = """SELECT * FROM Switches"""
    file.c.execute(sql_query)
    switches = file.c.fetchall()

    # Correct number of switches in the table
    assert len(switches) == 13, "Correct number of switches is 13"

get_switch_info()

## Correct number of lines
def num_of_lines():
    assert len(track.lines) == 2, "Correct number of lines is 2"

## Correct number of blocks per the green line
def num_of_blocks_green():
    file.read_new_data()
    sql_query = """SELECT * FROM 'Green Line'; """
    file.c.execute(sql_query)
    green_blocks = file.c.fetchall()

    assert len(green_blocks) == 150, "Correct number of blocks is 150"

num_of_blocks_green()

## Correct number of blocks per the red line
def num_of_blocks_red():
    file.read_new_data()
    sql_query = """SELECT * FROM 'Red Line'; """
    file.c.execute(sql_query)
    red_blocks = file.c.fetchall()

    assert len(red_blocks) == 76, "Correct number of blocks is 76"

num_of_blocks_red()

#*****************************************
# Display track properties
#*****************************************

## Grade for random track blocks correct

## Elevation for random track blocks correct

## Length for random track blocks correct

## Speed limit for random track blocks correct

## Direction of travel for random track blocks correct

## Railway crossings for random blocks of travel correct


#*****************************************
# 
#*****************************************