"""
AR_ToggleTintedBorder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ToggleTintedBorder
Version: 1.0.1
Description-US: Toggle opacity of tinted border in viewport, press shift to set custom value.
Note: Run the script from stored file location where you have writing permissions.
      The script creates a dat file for storing state of tinted border.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.1. (07.10.2020) - Added ALT-modifier, set custom border color with hex color code
"""
# Libraries
import c4d, os, re
from c4d import gui

# Functions
def GetKeyMod():
    """
    Retrieves the key from the key.

    Args:
    """
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

def HexToRgb(value):
    """
    Convert the color from rgb to hsv.

    Args:
        value: (str): write your description
    """
    value = value.replace(' ', '').replace('\n', '').replace('\r', '') # Remove spaces
    value = value.lstrip('#') # Strip '#' symbol from value
    lv = len(value) # Length of the input
    #print value
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():
    """
    The main routine.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    bd = doc.GetActiveBaseDraw() # Get active basedraw
    bc = c4d.BaseContainer() # Initialize base container
    path, fn = os.path.split(__file__) # Get path of the script
    data = os.path.join(path, 'AR_ToggleTintedBorder.txt') # data file path
    #try: # Try to execute following script
    f = open(data.decode('utf-8')) # Open file for reading
    value = float(f.readline()) # Get value from data file
    f.close() # Close file
    keyMod = GetKeyMod() # Get keymodifier
    if keyMod == "Shift":
        userValue = gui.InputDialog('Value') # Store user given value
        if userValue is not '':
            userValue = userValue.replace(',','.') # Replace comma to dot, if found
            numbers = re.compile('\d+(?:\.\d+)?') # Regular expression
            userValue = float(numbers.findall(userValue)[0]) # Strip anything else but numbers
            if userValue > 1: # If value is bigger than one
                value = userValue / 100.0 # Divide value by 100
            else: # If value is not bigger than one
                value = userValue # Set value to userValue
            f = open(data.decode('utf-8'), 'w') # Open file for writing
            f.write(str(value)) # Write value to file
            f.close() # Close file
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = value # Set opacity to custom
    elif keyMod == "None":
        if bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] == 0: # If tinted border's opacity is 0
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = value # Set opacity
        else: # If tinted border's opacity is not 0
            f = open(data.decode('utf-8'), 'w') # Open file for writing
            f.write(str(bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY])) # Write current value to file
            f.close() # Close file
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 0 # Set opacity to 0
    elif keyMod == "Ctrl":
        bd[c4d.BASEDRAW_DATA_TINTBORDER] = not bd[c4d.BASEDRAW_DATA_TINTBORDER] # Toggle 'Tinted Border' checkbox
    elif keyMod == "Alt": # Change border color
        userColor = gui.InputDialog('Value', '#000000') # Store user given value
        if userColor is not '':
            rgb = HexToRgb(userColor)
            color = c4d.Vector(float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255) # Convert rgb to c4d form
            bd[c4d.BASEDRAW_DATA_TINTBORDER_COLOR] = color # Set border color

    #except: # If something went wrong
        #pass # Do nothing
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()