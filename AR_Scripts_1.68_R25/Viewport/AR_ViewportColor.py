"""
AR_ViewportColor

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ViewportColor
Version: 1.0.0
Description-US: Changes the viewport backgound color
Note: The change is permanent.

Written for Maxon Cinema 4D R26.107
Python version 3.9.1

Change log:
1.0.0 (23.08.2022) - Initial version
"""

# Libraries
import c4d, os
from c4d import storage
from c4d import gui

def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_ViewportColor.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("333333 # Default Cinema 4D R26\n91a3a9 # Houdini Light (Average)\na9a9a9 # Houdini Grey\n000000 # Houdini Dark\n4a545e # Maya (Average)") # Default value
        f.close()
    return filePath

def Prefs(id):
    return c4d.plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

def hex_to_rgb(value):
    lv = len(value)
    rgb = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return c4d.Vector(float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255)

def main():

    keyMod = GetKeyMod() # Get keymodifier

    # Put 'Background Gradient' off, if it's on
    if Prefs(465001625)[c4d.PREF_VIEW_DISPLAYFILTER_GRADIENT] == True:
        Prefs(465001625)[c4d.PREF_VIEW_DISPLAYFILTER_GRADIENT] = False

    optionsFile = CheckFiles() # Get options file

    if keyMod == "None":
        colors = [] # Initialize an array for colors
        f = open(optionsFile) # Open the file for reading
        for line in f: # Iterate through every row
            line = line.rstrip('\n') # Strip newline stuff
            line = line.split("#")[0] # Remove comment
            line = line.strip() # remove white spaces
            rgb  = hex_to_rgb(line) # convert hex to rgb
            colors.append(rgb)

        currentColor = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND)
        color = currentColor # Temp

        if currentColor in colors:
            index = colors.index(currentColor)
            index = (index + 1) % len(colors)
        else:
            index = 0
        color = colors[index]

    elif keyMod == "Shift":
        hexColor = gui.InputDialog("HEX color", "")
        color = hex_to_rgb(hexColor) # convert hex to rgb

    elif keyMod == "Alt+Ctrl+Shift":
        storage.GeExecuteFile(optionsFile) # Open options file for editing
        pass

    c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND, color)
    c4d.EventAdd()
    pass

# Execute main()
if __name__=='__main__':
    main()