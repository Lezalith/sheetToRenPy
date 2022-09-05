####### File stuff ################################################################################

# Folder into which results are placed.
BASE_OUTPUT_FOLDER = "images/"

# Defaults when creating the .rpy file with an image statement.
DEFAULT_RPY_PAUSE = 0.1
DEFAULT_RPY_REPEAT = False
DEFAULT_RPY_PROPERTIES = None

import sys

if len(sys.argv):
    print("Script had nothing dragged on it.\nLetting the user to pick a file.")

# Lets you pick a file and returns it.
import easygui

def pickFile():

    # Open the prompt.
    a = easygui.fileopenbox( title = "Pick .png or .jpg to split:" )

    # Raise exception if a file wasn't picked
    if not a:
        raise Exception("No file was selected!")
        
    # Return the file path.
    return a

# File PATH with extension.
sheet_file_path = pickFile()

# File NAME with extension.
sheet_file = sheet_file_path.split("\\")[-1]

# Check if extension is ".png" or ".jpg"
if sheet_file.split(".")[-1] not in ["png", "jpg"]:
    raise Exception("Selected image has to be a .png or .jpg!")

# File name without extension.
sheet_fileName = ".".join(sheet_file.split(".")[:-1])

# print(sheet_file_path)
# print(sheet_file)
# print(sheet_fileName)


####### Preparing a directory for the output ######################################################

# For checking and creating directories.
import os 

# Folder inside which all results are placed.

# If the directory doesn't already exist...
if not os.path.isdir(BASE_OUTPUT_FOLDER):

    # ...create it.
    os.mkdir(BASE_OUTPUT_FOLDER) 

# Folder inside which this result will be placed, in the form of "BASE_OUTPUT_FOLDER/sheet_fileName/"
sheet_output_dir = BASE_OUTPUT_FOLDER + sheet_fileName + "/"
 
# This folder must not already exist.
if os.path.isdir(sheet_output_dir):
    raise Exception("It looks like the directory for output, \"{}\", exists already!".format( sheet_output_dir ))

# Create the directory.
os.mkdir(sheet_output_dir)


####### Sheet into frames ###########################################################################

# Module responsible for all the image manipulation.
from PIL import Image

# Load in chosen file.
im = Image.open(sheet_file_path)

# # TEST VALUES ######### 
# framesize = (120, 80)
# gridsize = (1, 6)
# amount_of_frames = gridsize[0] * gridsize[1]
# #######################

# Input values: 
framesize = eval(raw_input("Please give the size of one frame. This needs to be a tuple of (px width, px heigth) -- "))
gridsize = eval(raw_input("Please give the total size of grid. This needs to be a tuple of (rows, columns) -- "))

amount_of_frames = raw_input("How many frames are there? int, default of (num of rows given * num of cols given) -- ")
if not amount_of_frames:
    amount_of_frames = gridsize[0] * gridsize[1]
else:
    amount_of_frames = eval(amount_of_frames)

# List of file paths to individual frames.
# Used in creating the .rpy file.
paths_to_frames = []

# Dimensions of the picked image.
image_width, image_height = im.size

# Dimensions of one frame.
frame_width = image_width // gridsize[1]
frame_height = image_height // gridsize[0]

# Index of the currently-being-iterated-over frame.
frame_index = 0

# For every row...
for row_index in range(gridsize[0]):

    # For every column inside that row...
    for column_index in range(gridsize[1]):

        # Top left corner of crop.
        x = frame_width * column_index
        y = frame_height * row_index

        # Bottom right corner of crop.
        x_end = frame_width * (column_index + 1)
        y_end = frame_height * (row_index + 1)

        print("Creating a frame (coords:({}, {})): [{}, {}], [{}, {}]".format(row_index + 1, column_index + 1, x, y, x_end, y_end))

        # Created frame image.
        frame = im.crop( (x, y, x_end, y_end) )

        # Filename of the saved frame.
        # Format is "[chosen file without extension][index of the frame].png"
        save_file_name = sheet_output_dir + "{}{}.png".format(sheet_fileName, frame_index)

        # Save the frame image.
        frame.save(save_file_name)

        # Save the frame path to a list.
        # Used in creating the .rpy file.
        paths_to_frames.append(save_file_name)

        # Up the index for the next iteration.
        frame_index += 1

        # End the loop if max amount of frames was given.
        if frame_index >= amount_of_frames:
            break

    # End the loop if max amount of frames was given.
    if frame_index >= amount_of_frames:
        break

print("\nSuccessfully saved all frames into \"{}\"\n\n###########################################################\n".format(sheet_output_dir))


####### Optionally creating a .rpy file.

create_rpy = raw_input("Would you like to create a .rpy file with an image statement, defining the image for you?\nType in \"y\" if so. --")

# Negative input.
if not create_rpy == "y":

    print("\n###########################################################\n\nSkipped creating the .rpy file.")

    # End the script.
    input()


####### Settings for creating a Ren'Py image statement. ###########################################

print("\nYou will now be asked for some settings.\nDefault values are chosen when nothing is typed in.\n")

pause_interval = raw_input("Pause interval between frames? float, default is DEFAULT_RPY_PAUSE -- ")

# Default
if not pause_interval:
    pause_interval = DEFAULT_RPY_PAUSE

### Whether the animation should repeat. ############################
add_repeat = raw_input("Should the animation repeat? (\"y\" or \"n\", default is DEFAULT_RPY_REPEAT) -- ")

# Negative input.
if add_repeat == "n":

    add_repeat = False

elif add_repeat == "y":

    add_repeat = True

else:

    add_repeat = DEFAULT_RPY_REPEAT

### Properties that will be added onto the first line. ##############
### These will be in effect throughout the whole animation. #########
properties = raw_input("Add some properties onto the first line? (Properties written like you would in ATL, DEFAULT_RPY_PROPERTIES by default) -- ")

# If none are given, the line won't be added at all.
if not properties:

    properties = DEFAULT_RPY_PROPERTIES


####### Creating a .rpy file with an image statement. #############################################

# Path of the .rpy file with extension.
rpy_file_path = sheet_output_dir + sheet_fileName + ".rpy"

# Create the file.
with open(rpy_file_path, "w+") as f:

    # Image statement (first line)
    statement = "image " + sheet_fileName + ":\n"

    f.write(statement)

    # Add properties onto the first line if any were given.
    if properties is not None:

        properties = "    " + properties + "\n"

        f.write(properties)

    # Write an image path, followed by a pause of given interval.
    for frame_path in paths_to_frames:

        f.write( "    " + "\"" + frame_path + "\"\n" )
        f.write( "    " + "pause " + str(pause_interval) + "\n" )

    # Optionally finish with a repeat.
    if add_repeat:

        f.write("    repeat")

print("\n###########################################################\n\nSuccessfully saved the .rpy file as \"{}\"".format(rpy_file_path))