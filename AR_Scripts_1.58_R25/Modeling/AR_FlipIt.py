"""
AR_FlipIt

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_FlipIt
Version: 1.0.0
Description-US: Flips seleceted objects.

Written for Maxon Cinema 4D R26.013
Python version 3.9.1

Change log:
1.0.0 (21.04.2022) - Initial version
"""

# Librarires
import c4d
from c4d import utils as u
from c4d.gui import GeDialog
from c4d.modules import snap
from c4d import storage
import os

# Variables
GRP_MAIN  = 1000
GRP_FCTR  = 1001
GRP_CHK   = 1002
GRP_BTN   = 1003

BTN_OK    = 2001
BTN_CNL   = 2002

COMBO_SPACE= 3000
TXT_SPACE  = 3001

SPC_WORLD  = 5000
SPC_PARENT = 5001
SPC_LOCAL  = 5002

CHK_AXIS_X = 4000
CHK_AXIS_Y = 4001
CHK_AXIS_Z = 4002
CHK_COPY   = 4003

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

def GetC4DVersion():
    c4dversion = c4d.GetC4DVersion()
    releaseVersion = int(str(c4dversion)[:2])
    buildVersion = int(str(c4dversion)[:2])
    return releaseVersion, buildVersion

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
        'space' : float(optionsArray[0]),
        'x': int(optionsArray[1]),
        'y': int(optionsArray[2]),
        'z': int(optionsArray[3]),
        'copy': int(optionsArray[4])
    }
    return options

def saveSettings(space, x, y, z, copy):
    optionsFile = CheckFiles() #
    f = open(optionsFile, 'w') # Open the file for writing
    settings = [str(space),
                str(int(x)),
                str(int(y)),
                str(int(z)),
                str(int(copy))]

    settings = "\n".join(settings) # Create a string from an array
    f.write(settings) # Write settings to the file
    f.close() # Close the file
    return True # Everything is fine

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_FlipIt.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("5000\n1\n0\n0\n0") # Default settings
        f.close()
    return filePath

def GetGlobalScale(obj): # Get object's global scale
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalScale(obj, scale): # Set object's global scale
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def FlipIt(op, settings):
    if op == None: return

    if settings['copy'] == True:
        copy = op.GetClone()
        doc.InsertObject(copy, pred=op, checknames=True)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, copy)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)
        op.DelBit(c4d.BIT_ACTIVE)
        op = copy

    oldMat = op.GetMg()
    scale = GetGlobalScale(op)

    if settings['x'] == True: # If flip X-axis
        x = -1
    else:
        x = 1

    if settings['y'] == True: # If flip Y-axis
        y = -1
    else:
        y = 1

    if settings['z'] == True: # If flip Z-axis
        z = -1
    else:
        z = 1

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)

    if settings['space'] == SPC_WORLD: # If world space
        workplane = snap.GetWorkplaneObject(doc) # Get workplane
        op.SetMg(workplane.GetMg())
        modifiedScale = c4d.Vector(scale.x * x, scale.y * y, scale.z * z)
        SetGlobalScale(op, modifiedScale)
        op.SetMg(~workplane.GetMg()*op.GetMg()*oldMat)

    elif settings['space'] == SPC_PARENT: # If parent's space
        if op.GetUp() == None:
            print("No parent object found!")
            return
        parent = op.GetUp() # Get parent
        op.SetMg(parent.GetMg())
        modifiedScale = c4d.Vector(scale.x * x, scale.y * y, scale.z * z)
        SetGlobalScale(op, modifiedScale)
        op.SetMg(~parent.GetMg()*op.GetMg()*oldMat)

    elif settings['space'] == SPC_LOCAL: # If local space
        modifiedScale = c4d.Vector(scale.x * x, scale.y * y, scale.z * z)
        SetGlobalScale(op, modifiedScale)

def Iterate(settings):
    
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get selected objects
    for s in selection: # Iterate through selected objects
        FlipIt(s, settings)
    pass

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create the dialog
    def CreateLayout(self):
        global settings

        settings = loadSettings()

        self.SetTitle("Flip It") # Set dialog title

        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 1, 1) # Begin Main group
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space

        self.GroupBegin(GRP_FCTR, c4d.BFH_CENTER, 2, 1) # Begin Main group
        self.AddStaticText(TXT_SPACE, c4d.BFH_LEFT, name="Space")
        self.AddComboBox(COMBO_SPACE, c4d.BFH_LEFT, 80, 0)

        self.AddChild(COMBO_SPACE, SPC_WORLD, "World")
        self.AddChild(COMBO_SPACE, SPC_PARENT, "Parent")
        self.AddChild(COMBO_SPACE, SPC_LOCAL, "Local")

        self.GroupEnd() # End Buttons group

        self.GroupBegin(GRP_CHK, c4d.BFH_CENTER, 1, 3, "Checkboxes") # Begin Buttons group
        self.GroupBorderSpace(0, 0, 0, 5) # Add border space
        self.AddCheckbox(CHK_AXIS_X, c4d.BFH_LEFT, 0, 0, "X-axis")
        self.AddCheckbox(CHK_AXIS_Y, c4d.BFH_LEFT, 0, 0, "Y-axis")
        self.AddCheckbox(CHK_AXIS_Z, c4d.BFH_LEFT, 0, 0, "Z-axis")
        self.GroupEnd() # End Buttons group

        self.AddCheckbox(CHK_COPY, c4d.BFH_LEFT, 0, 0, "Duplicate object")

        self.SetInt32(COMBO_SPACE, int(settings['space']))
        self.SetBool(CHK_AXIS_X, int(settings['x']))
        self.SetBool(CHK_AXIS_Y, int(settings['y']))
        self.SetBool(CHK_AXIS_Z, int(settings['z']))
        self.SetBool(CHK_COPY, int(settings['copy']))

        self.GroupEnd() # End Main group

        # Buttons
        self.GroupBegin(GRP_BTN, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin Buttons group
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Flip") # Add button
        self.AddButton(BTN_CNL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End Buttons group

        return True

    # Processing GUI events
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global settings

        bc = c4d.BaseContainer() # Initialize a base container

        space = self.GetInt32(COMBO_SPACE)
        x = self.GetBool(CHK_AXIS_X)
        y = self.GetBool(CHK_AXIS_Y)
        z = self.GetBool(CHK_AXIS_Z)
        copy = self.GetBool(CHK_COPY)

        # User presses Cancel button
        if paramid == BTN_CNL:
            self.Close() # Close dialog
        
        # User presses Ok button
        if paramid == BTN_OK:
            saveSettings(space, x, y, z, copy)
            settings = loadSettings()
            Iterate(settings)
            self.Close() # Close dialog

        # User presses ESC key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        # User presses ENTER key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            saveSettings(space, x, y, z, copy)
            settings = loadSettings()
            Iterate(settings)
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
        Iterate(settings)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

    pass

if __name__ == '__main__':
    main()