"""
AR_Dot

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Dot
Version: 1.3.0
Description-US: Creates a separator null

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.3.0 (30.10.2022) - Added python tag to keep the name
1.2.0 (16.11.2022) - Added options feature
1.1.0 (18.08.2022) - A bit more advanced
1.0.0 (02.05.2022) - First version
"""

# Libraries
import c4d, os, re
import sys
from c4d import gui
from c4d import storage
from c4d.gui import GeDialog

# Global variables
GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_BTNS        = 1002

DOT_STR_NAME    = 2001
DOT_NAME        = 2002
DOT_STR_COL     = 2003
DOT_COL         = 2004

BTN_OK          = 7001
BTN_CANCEL      = 7002

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):

        # Stuff...
        optionsFile = CheckFiles()
        f = open(optionsFile,"r")
        nameValue = f.readline().replace("\n", "") # Get name value from the file
        colorValue = f.readline().split(",") # Get color value from the file
        color = c4d.Vector(float(colorValue[0].strip()), float(colorValue[1].strip()), float(colorValue[2].strip()))
        f.close() # Close file

        #f = open(optionsFile, 'w') # Open the file for writing

        self.SetTitle("Dot settings") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=200, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=2, groupflags=1, initw=200, inith=0)
        self.AddStaticText(DOT_STR_NAME, c4d.BFH_LEFT, inith=13, name="Dot name")
        self.AddEditText(DOT_NAME, c4d.BFH_RIGHT, initw=70, inith=13)
        self.SetString(DOT_NAME, nameValue)
        self.AddStaticText(DOT_STR_COL, c4d.BFH_LEFT, inith=13, name="Dot color")
        self.AddColorField(DOT_COL, c4d.BFH_RIGHT, initw=70, inith=13, colorflags=c4d.DR_COLORFIELD_POPUP)
        self.SetColorField(DOT_COL, color, 1, 1, c4d.DR_COLORFIELD_ENABLE_COLORWHEEL)
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
            name = self.GetString(DOT_NAME)
            color = self.GetColorField(DOT_COL)["color"]
            optionsFile = CheckFiles()
            f = open(optionsFile,"w")
            f.write(name+"\n"+str(color[0])+","+str(color[1])+","+str(color[2]))
            f.close() # Close file
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            name = self.GetString(DOT_NAME)
            color = self.GetColorField(DOT_COL)["color"]
            optionsFile = CheckFiles()
            f = open(optionsFile,"w")
            f.write(name+"\n"+str(color[0])+","+str(color[1])+","+str(color[2]))
            f.close() # Close file
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

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_Dot.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write(" \n0.235,0.239,0.239") # Default values
        f.close()
    return filePath

def CreateTag(obj, name, color):
    pyTag = c4d.BaseTag(1022749) # Initialize a python tag
    pyTag[1041670] = True # Enable icon color
    pyTag[c4d.ID_BASELIST_ICON_COLOR] = color # Color
    pyTag[c4d.ID_BASELIST_NAME] = "Auto Name"
    pyCode = "# Libraries\n\
import c4d\n\
\n\
# Functions\n\
def main():\n\
\tname = \""+ name +"\"\n\
\tif op.GetObject().GetName != name: # If not blank name\n\
\t\top.GetObject().SetName(name) # Set blank name"
    pyTag[c4d.TPYTHON_CODE] = pyCode # Assign python code
    obj.InsertTag(pyTag) # Insert pyTag to the object

def CreateDot():
    optionsFile = CheckFiles()
    f = open(optionsFile,"r")
    nameValue = f.readline().replace("\n", "") # Get name
    colorValue = f.readline().split(",") # Get color
    color = c4d.Vector(float(colorValue[0].strip()), float(colorValue[1].strip()), float(colorValue[2].strip()))
    f.close() # Close file
    null = c4d.BaseObject(c4d.Onull) # Init a null object
    CreateTag(null, nameValue, color) # Add python tag
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

    if keyMod == "Alt+Ctrl+Shift": # Change settings
        dlg = Dialog() # Create dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog
        pass
    else: # Create Dot
        if len(selection) == 0: # If no selected objects
            null = CreateDot()
            doc.InsertObject(null) # Insert null to the project
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Add undo step for inserting a new object
        else: # Otherwise
            for x in selection: # Iterate through objects
                null = CreateDot()
                if (keyMod == "None") or (keyMod == "Alt") or (keyMod == "Ctrl"):
                    null.InsertAfter(x) # Insert null after the object
                elif (keyMod == "Shift") or (keyMod == "Alt+Shift") or (keyMod == "Ctrl+Shift"):
                    null.InsertBefore(x) # Insert null before the object
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Add undo step for inserting a new object
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()