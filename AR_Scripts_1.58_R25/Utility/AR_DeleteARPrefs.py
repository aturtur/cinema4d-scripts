"""
AR_DeleteARPrefs

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DeleteARPrefs
Version: 1.0.0
Description-US: Deletes aturtur folder in prefs location

Written for Maxon Cinema 4D R25.117
Python version 3.9.1
"""

# Libraries
import os
import shutil
import c4d
from c4d import storage
from c4d import gui

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

def main():
    keyMod   = GetKeyMod() # Get keyboard modifier
    folder   = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get preference folder path
    arFolder = os.path.join(folder, "aturtur") # Aturtur folder
    if os.path.exists(arFolder) and os.path.isdir(arFolder): # If folder exists and the type is a folder
        if keyMod == "None":
            confirm = gui.QuestionDialog("Really wanna delete\nAR_Scripts saved settings?") # Ask if user really wants to remove the folder
            if confirm: # If pressed yes
                shutil.rmtree(arFolder) # Remove the folder
                gui.MessageDialog("Settings folder for AR_Scripts\nis now removed!")
        elif keyMod == "Shift":
            if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN: # If operating system is Windows
                os.startfile(arFolder)
            else: # If operating system is Mac
                os.system('open "%s"' % arFolder)

    else: # Otherwise
        gui.MessageDialog("No settings folder found\nfor AR_Scripts!")

# Execute main()
if __name__=='__main__':
    main()