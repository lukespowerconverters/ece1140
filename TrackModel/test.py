### TESTING CODE ###
import TrackModel

track = TrackModel()



### UNIT TESTS FOR THE TRACK MODEL ###

#*****************************************
# Load track model
#*****************************************

## Import only .xlsx type files

## Export file data into GUI tables

## Correct number of lines
def num_of_lines():
    assert len(track.lines) == 2, "Correct number of lines is 2"

## Correct number of blocks per line
def num_of_blocks_green():
    green_line = track.get_line("green")
    assert len(green_line.blocks) == 150, "Correct number of blocks is 150"

def num_of_blocks_red():
    red_line = track.get_line("red")
    assert len(red_line.blocks) == 76, "Correct number of blocks is 76"

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