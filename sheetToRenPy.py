####### File stuff ################################################################################

# Lets you pick a file and returns it.
import easygui

def pickFile():

    # Open the prompt.
    a = easygui.fileopenbox( title = "Pick .png or .jpg to split:" )

    # Raise exception if a file wasn't picked
    if not a:
        raise Exception("Nothing selected!")
        
    # Return the file.
    return a

# File path with extension.
sheetFilePath = pickFile()

# File name with extension.
sheetFile = sheetFilePath.split("\\")[-1]

# Check if extension is ".png" or ".jpg"
if sheetFile.split(".")[-1] not in ["png", "jpg"]:
    raise Exception("That is not a .png nor .jpg!")

# File name without extension.
sheetFileName = ".".join(sheetFile.split(".")[:-1])

# print(sheetFilePath)
# print(sheetFile)
# print(sheetFileName)


####### Preparing a directory for the output ######################################################

# For checking and creating directories.
import os 

# Folder inside which all results are placed.
#
# This is important because this directory is included in paths inside the generated .rpy file.
# "images/" means the result inside should be placed inside a project's "images" folder.
baseOutputDir = "images/"

# If the directory doesn't already exist...
if not os.path.isdir(baseOutputDir):

    # ...create it.
    os.mkdir(baseOutputDir) 

# Folder inside which this result will be placed, in the form of "baseOutputDir/sheetFileName/"
sheetOutputDir = baseOutputDir + sheetFileName + "/"
 
# This directory must not already exist.
if os.path.isdir(sheetOutputDir):
    raise Exception("It looks like the directory for output, \"{}\", exists already!".format( baseOutputDir + sheetFileName ))

# Create the directory.
os.mkdir(sheetOutputDir)


####### Sheet into frames ###########################################################################

# For the whole process.
from PIL import Image

# Load in chosen file.
im = Image.open(sheetFilePath)

# TEST VALUES ######### 
framesize = (120, 80)
gridsize = (1, 6)
amountOfFrames = gridsize[0] * gridsize[1]
#######################

# REAL VALUES ######### 
# framesize = eval(raw_input("Please give the size of one frame. This needs to be a tuple of (px width, px heigth) -- "))
# gridsize = eval(raw_input("Please give the total size of grid. This needs to be a tuple of (rows, columns) -- "))

# pauseInterval = raw_input("Pause interval between frames? float, default is 0.1 -- ")
# # Default, if nothing given.
# if not pauseInterval:
#     pauseInterval = "0.1"

# amountOfFrames = raw_input("How many frames are there? int, default of (num of rows given * num of cols given) -- ")
# if not amountOfFrames:
#     amountOfFrames = gridsize[0] * gridsize[1]
# else:
#     amountOfFrames = eval(amountOfFrames)

#######################

# List of file paths to individual frames.
# Used in creating the .rpy file.
pathsToFrames = []

# Image dimensions
imageWidth, imageHeigth = im.size

# Frame dimensions
oneFrameWidth = imageWidth // gridsize[1]
oneFrameHeigth = imageHeigth // gridsize[0]

# Index of the currently-being-iterated-over frame.
frameIndex = 0

# For every row...
for rowIndex in range(gridsize[0]):

    # For every column inside that row...
    for columnIndex in range(gridsize[1]):

        # Top left corner of crop.
        x = oneFrameWidth * columnIndex
        y = oneFrameHeigth * rowIndex

        # Bottom right corner of crop.
        xEnd = oneFrameWidth * (columnIndex + 1)
        yEnd = oneFrameHeigth * (rowIndex + 1)

        print("Creating a frame (coords:({}, {})): [{}, {}], [{}, {}]".format(rowIndex + 1, columnIndex + 1, x, y, xEnd, yEnd))

        # Created frame.
        frame = im.crop( (x, y, xEnd, yEnd) )

        # Filename of the saved frame.
        # Format is "[chosen file without extension][index of the frame].png"
        saveFileName = sheetOutputDir + "{}{}.png".format(sheetFileName, frameIndex)

        # Save the frame.
        frame.save(saveFileName)

        # Save the frame path to a list.
        # Used in creating the .rpy file.
        pathsToFrames.append(saveFileName)

        # Up the index for the next iteration.
        frameIndex += 1

        # End the loop if max amount of frames was given.
        if frameIndex >= amountOfFrames:
            break

    # End the loop if max amount of frames was given.
    if frameIndex >= amountOfFrames:
        break

print("\nSuccessfully saved all frames into \"{}\"\n\n###########################################################\n".format(sheetOutputDir))


# ####### Optionally creating a .rpy file.

# createRpy = raw_input("Would you like to create a .rpy file with an image statement, defining the image for you?\nI do this by default, when nothing is typed in. Type \"n\" if you don't want me to. -- ")

# # Negative input.
# if createRpy == "n":

#     print("\n###########################################################\n\nSkipped creating the .rpy file.")

#     # End the script.
#     exit()


# ####### Settings for creating a Ren'Py image statement. ###########################################

# print("\nYou will now be asked for some settings.\nDefault values are chosen when nothing is typed in.\n")

# # Convert it to a float.
# else:

#     try:
#         pauseInterval = float(pauseInterval)

#     # If cannot be converted:
#     except:
#         raise Exception("Pause interval, if given, must be a whole or a decimal number.")


# ### Whether the animation should repeat. ############################
# addRepeat = raw_input("Should the animation repeat? (y/n, default is \"n\") -- ")

# # Positive input.
# if addRepeat == "y":

#     addRepeat = True

# # Negative or no input.
# elif addRepeat == "n" or not addRepeat:

#     addRepeat = False

# # Something else typed in.
# else:

#     raise Exception("Something other than \"y\", \"n\" or \"\" typed in.")


# ### Properties that will be added onto the first line. ##############
# ### These will be in effect throughout the whole animation. #########
# firstProperties = raw_input("Add some properties onto the first line? (Properties written like you would in ATL, none by default) -- ")

# # If none are given, the line won't be added at all.
# if not firstProperties:

#     firstProperties = None


# ####### Creating a .rpy file with an image statement. #############################################

# # Path of the .rpy file with extension.
# rpyFilePath = sheetOutputDir + sheetFileName + ".rpy"

# # Create the file.
# with open(rpyFilePath, "w+") as f:

#     # Image statement (first line)
#     statement = "image " + sheetFileName + ":\n"

#     f.write(statement)

#     # Add properties onto the first line if any were given.
#     if firstProperties is not None:

#         properties = "    " + firstProperties + "\n"

#         f.write(properties)

#     # Write an image path, followed by a pause of given interval.
#     for pathToFrame in pathsToFrames:

#         f.write( "    " + "\"" + pathToFrame + "\"\n" )
#         f.write( "    " + "pause " + str(pauseInterval) + "\n" )

#     # Optionally finish with a repeat.
#     if addRepeat:

#         f.write("    repeat")

# print("\n###########################################################\n\nSuccessfully saved the .rpy file as \"{}\"".format(rpyFilePath))