"""
AR_ToggleTintedBorder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ToggleTintedBorder
Version: 1.0.2
Description-US: Toggle opacity of tinted border in viewport, press shift to set custom value.
Note: Run the script from stored file location where you have writing permissions.
      The script creates a dat file for storing state of tinted border.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.2 (08.04.2021) - R23 support, ALT-modifier removed and added color picker and slider to SHIFT option
1.0.1 (07.10.2020) - Added ALT-modifier, set custom border color with hex color code
"""
# Libraries
import c4d, os, re
import sys
from c4d import gui
from c4d.gui import GeDialog

GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_BTNS        = 1002
GRP_VAL         = 1003
GRP_COL         = 1004


TINT_VAL        = 2001
TINT_COL        = 2002

BTN_OK          = 7001
BTN_CANCEL      = 7002

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw  

        curValue = bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] 
        curColor = bd[c4d.BASEDRAW_DATA_TINTBORDER_COLOR]

        self.SetTitle("Tinted Border") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=300, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=1, groupflags=1, initw=300, inith=0)
        self.GroupBegin(GRP_VAL, c4d.BFH_LEFT | c4d.BFH_SCALEFIT, cols=1, rows=1, groupflags=1, initw=250, inith=0)
        self.AddEditSlider(TINT_VAL, c4d.BFH_SCALEFIT, initw=50, inith=0)
        self.SetPercent(TINT_VAL, curValue, min=0.0, max=100.0, step=1.0, tristate=False)
        self.GroupEnd()
        self.GroupBegin(GRP_COL, c4d.BFH_RIGHT, cols=1, rows=1, groupflags=1, initw=0, inith=0)
        self.AddColorField(TINT_COL, c4d.BFH_FIT, initw=70, inith=13, colorflags=0)
        self.SetColorField(TINT_COL, curColor, 1, 1, 0)
        self.GroupEnd()
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        # Buttons
        self.GroupBegin(GRP_BTNS, c4d.BFH_CENTER)
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        self.GroupEnd()
        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw
        bc = c4d.BaseContainer() # Initialize a base container
        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Accept' button is pressed
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = self.GetFloat(TINT_VAL)
            bd[c4d.BASEDRAW_DATA_TINTBORDER_COLOR] = self.GetColorField(TINT_COL)['color']
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = self.GetFloat(TINT_VAL)
            bd[c4d.BASEDRAW_DATA_TINTBORDER_COLOR] = self.GetColorField(TINT_COL)['color']
            self.Close() # Close dialog
        return True # Everything is fine

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
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    bd = doc.GetActiveBaseDraw() # Get active basedraw
    bc = c4d.BaseContainer() # Initialize base container
    path, fn = os.path.split(__file__) # Get path of the script
    data = os.path.join(path, 'AR_ToggleTintedBorder.txt') # data file path
    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(data) # Open the file for reading
    else: # If Python 2 version (R21)
        f = open(data.decode("utf-8"))
    value = float(f.readline()) # Get value from data file
    f.close() # Close file
    keyMod = GetKeyMod() # Get keymodifier
    if keyMod == "None":
        if bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] == 0: # If tinted border's opacity is 0
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = value # Set opacity
        else: # If tinted border's opacity is not 0
            if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
                f = open(data, 'w') # Open the file for writing
            else: # If Python 2 version (R21)
                f = open(data.decode("utf-8"), 'w') # Open the file for writing
            f.write(str(bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY])) # Write current value to file
            f.close() # Close file
            bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 0 # Set opacity to 0
    elif keyMod == "Shift":
        dlg = Dialog() # Create dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog
    elif keyMod == "Ctrl":
        bd[c4d.BASEDRAW_DATA_TINTBORDER] = not bd[c4d.BASEDRAW_DATA_TINTBORDER] # Toggle 'Tinted Border' checkbox
    #except: # If something went wrong
        #pass # Do nothing
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()