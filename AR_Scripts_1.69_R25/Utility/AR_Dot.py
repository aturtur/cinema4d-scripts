"""
AR_Dot

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Dot
Version: 1.0.1
Description-US: Creates a separator null.

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.0 (02.05.2022) - First version
1.0.1 (18.08.2022) - A bit more advanced
"""

# Libraries
import c4d

# Global variables
color = c4d.Vector(0.235, 0.239, 0.239)

# Functions
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

def CreateDot():
    global color

    null = c4d.BaseObject(c4d.Onull) # Init a null object
    null[c4d.ID_BASELIST_ICON_FILE] = "17106" # Set icon to 'Circle'
    null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Set icon color to 'Custom'
    null[c4d.ID_BASELIST_ICON_COLOR] = color # Set icon color
    null[c4d.NULLOBJECT_DISPLAY] = 14 # Set shape to 'None'
    null.SetName(" ") # Set null's name
    return null # Return the null object

def main():
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get key modifier
    selection = doc.GetSelection() # Get selected objects
    if len(selection) == 0: # If no selected objects
        null = CreateDot()
        doc.InsertObject(null) # Insert null to the project
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Add undo step for inserting a new object
    else: # Otherwise
        for x in selection: # Iterate through objects
            null = CreateDot()
            if keyMod == "None":
                null.InsertAfter(x) # Insert null after the object
            if keyMod == "Shift":
                null.InsertBefore(x) # Insert null before the object
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Add undo step for inserting a new object
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()