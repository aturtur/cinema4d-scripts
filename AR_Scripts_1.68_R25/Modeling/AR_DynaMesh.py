"""
AR_DynaMesh

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DynaMesh
Version: 1.0.1
Description-US: Remeshes selected object with ZRemesher.

Note: Requires Cinema 4D R26!

Written for Maxon Cinema 4D R26.013
Python version 3.9.1

Change log:
1.0.1 (17.09.2022) - Support for material
1.0.0 (20.04.2022) - Initial version
"""

# Librarires
import c4d
from c4d import utils as u
from c4d.gui import GeDialog
from c4d import storage
import os

# Variables

GRP_MAIN  = 1000
GRP_FCTR  = 1001
GRP_CHK   = 1002
GRP_BTN   = 1003

BTN_OK    = 2001
BTN_CNL   = 2002

NUM_FCTR  = 3000
TXT_FCTR  = 3001

CHK_SYM_X = 4000
CHK_SYM_Y = 4001
CHK_SYM_Z = 4002

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

def GetFolderSeparator():
    if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN: # If operating system is Windows
        return "\\"
    else: # If operating system is Mac or Linux
        return "/"

def loadSettings():
    optionsFile = CheckFiles()
    f = open(optionsFile) # Open the file for reading
    optionsArray = [] # Initialize an array for options
    for line in f: # Iterate through every row
        line = line.rstrip('\n') # Strip newline stuff
        optionsArray.append(line)
    f.close() # Close the file
    options = {
        'factor'    : float(optionsArray[0]),
        'symmetry_x': int(optionsArray[1]),
        'symmetry_y': int(optionsArray[2]),
        'symmetry_z': int(optionsArray[3])
    }
    return options

def saveSettings(factor, x, y, z):
    optionsFile = CheckFiles() #
    f = open(optionsFile, 'w') # Open the file for writing
    settings = [str(factor),
                str(int(x)),
                str(int(y)),
                str(int(z))]

    settings = "\n".join(settings) # Create a string from an array
    f.write(settings) # Write settings to the file
    f.close() # Close the file
    return True # Everything is fine

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_DynaMesh.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("1.0\n0\n0\n0") # Default settings
        f.close()
    return filePath

def CurrentStateToObject(doc, op):
    res = u.SendModelingCommand(command=c4d.MCOMMAND_CURRENTSTATETOOBJECT, list=[op], doc=doc)
    if res is False: # If modeling command failed
        return None # Return 'None'
    elif not isinstance(res, list): # If didn't returned a list
        return None # Return 'None'
    return res[0]

def toBool(x):
    return x in ("True","true",True)

def DynaMesh(doc, op, settings):
    if op == None: return

    name = op.GetName() # Get object's name
    remesh = c4d.BaseObject(1054750) # Init remesh object
    remesh.SetName(name) # Set name
    remesh[c4d.ID_REMESHALGORITHM] = 1 # Set 'Algorithm' to 'ZRemesher'
    remesh[c4d.ID_REMESH_POLYGONTARGET_MODE] = 1 # Set 'Polygon Target Mode' to 'Mesh Density'

    remesh[c4d.ID_REMESH_POLYGONSCALE] = float(settings['factor']) # Set 'Mesh Density'

    remesh[c4d.ID_REMESH_QUADREMESH_SYMMETRYX] = int(settings['symmetry_x']) # Symmetric X
    remesh[c4d.ID_REMESH_QUADREMESH_SYMMETRYY] = int(settings['symmetry_y']) # Symmetric Y
    remesh[c4d.ID_REMESH_QUADREMESH_SYMMETRYZ] = int(settings['symmetry_z']) # Symmetric Z

    doc.InsertObject(remesh, pred=op)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, remesh)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)
    op.InsertUnder(remesh) # Add remesh to project

    tags = op.GetTags()
    for t in tags:
        if t.GetType() == 5616:
            cloneTag = t.GetClone() # Clone texture tag
            remesh.InsertTag(cloneTag) # Insert texture tag to remesh
            doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
            t.Remove() # Remove tag

    obj = CurrentStateToObject(doc, remesh)
    doc.InsertObject(obj, pred=remesh)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, obj)

    remesh.Remove() # Remove remesh object
    doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, remesh)

    obj.SetBit(c4d.BIT_ACTIVE) # Select object
    op.DelBit(c4d.BIT_ACTIVE) # Deselect object

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create the dialog
    def CreateLayout(self):
        global settings

        settings = loadSettings()

        self.SetTitle("DynaMesh") # Set dialog title

        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 1, 1) # Begin Main group
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space

        self.GroupBegin(GRP_FCTR, c4d.BFH_CENTER, 2, 1) # Begin Main group
        self.AddStaticText(TXT_FCTR, c4d.BFH_LEFT, name="Factor")
        self.AddEditNumberArrows(NUM_FCTR, c4d.BFH_LEFT, 70, 0)
        self.GroupEnd() # End Buttons group

        self.GroupBegin(GRP_CHK, c4d.BFH_CENTER, 1, 3, "Checkboxes") # Begin Buttons group
        self.AddCheckbox(CHK_SYM_X, c4d.BFH_LEFT, 0, 0, "Symmetric X")
        self.AddCheckbox(CHK_SYM_Y, c4d.BFH_LEFT, 0, 0, "Symmetric Y")
        self.AddCheckbox(CHK_SYM_Z, c4d.BFH_LEFT, 0, 0, "Symmetric Z")
        self.GroupEnd() # End Buttons group

        self.SetReal(NUM_FCTR, float(settings['factor']), min=0.01, max=100.00, step=0.01)
        self.SetBool(CHK_SYM_X, int(settings['symmetry_x']))
        self.SetBool(CHK_SYM_Y, int(settings['symmetry_y']))
        self.SetBool(CHK_SYM_Z, int(settings['symmetry_z']))

        self.GroupEnd() # End Main group

        # Buttons
        self.GroupBegin(GRP_BTN, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin Buttons group
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Remesh") # Add button
        self.AddButton(BTN_CNL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End Buttons group

        return True

    # Processing GUI events
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global settings

        bc = c4d.BaseContainer() # Initialize a base container

        f = self.GetInt32(NUM_FCTR)
        x = self.GetBool(CHK_SYM_X)
        y = self.GetBool(CHK_SYM_Y)
        z = self.GetBool(CHK_SYM_Z)

        # User presses Cancel button
        if paramid == BTN_CNL:
            self.Close() # Close dialog

        # User presses Ok button
        if paramid == BTN_OK:
            saveSettings(f, x, y, z)
            DynaMesh(doc, op, settings)
            self.Close() # Close dialog

        # User presses ESC key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        # User presses ENTER key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            saveSettings(f, x, y, z)
            DynaMesh(doc, op, settings)
            self.Close() # Close dialog

        return True # Everything is fine

def main():
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "Shift":
        dlg = Dialog() # Create a dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog
    else:
        settings = loadSettings()
        DynaMesh(doc, op, settings)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

    pass

if __name__ == '__main__':
    main()