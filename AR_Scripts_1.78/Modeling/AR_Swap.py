"""
AR_Swap

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Swap
Version: 1.0.1
Description-US: Swaps selected objects between each other.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (19.01.2022) - R25 update
"""

# Libraries
import c4d
from c4d import utils as u
from c4d.gui import GeDialog

# GUI IDs
GRP_MAIN = 1000
GRP_BTN  = 1008

CHK_POS  = 1001
CHK_SCL  = 1002
CHK_ROT  = 1003
CHK_OM   = 1004

BTN_OK   = 2001
BTN_CNL  = 2002

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

def GetGlobalPosition(obj): # Get object's global position
    return obj.GetMg().off

def GetGlobalRotation(obj): # Get object's global rotation
    return u.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj): # Get object's global scale
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalPosition(obj, pos): # Set object's global position
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot): # Set object's global rotation
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector(m.v1.GetLength(),
                       m.v2.GetLength(),
                       m.v3.GetLength())
    m = u.HPBToMatrix(rot)
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SetGlobalScale(obj, scale): # Set object's global scale
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SwapObjects(p, s, r, h):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    bc = c4d.BaseContainer() # Initialize Base Container
    tempNullA = c4d.BaseObject(c4d.Onull) # Initialize temporary Null object
    tempNullB = c4d.BaseObject(c4d.Onull)
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE) # Get selection
    objA = selection[0] # Get object A
    objB = selection[1] # Get objet B

    #matA = objA.GetMg() # Get object A's global matrix
    #matB = objB.GetMg() # Get object B's global matrix

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, objA) # Add undo for changing object A
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, objB) # Add undo for changing object B
    tempNullA.InsertBefore(objA) # Insert temp Null A before object A
    tempNullB.InsertBefore(objB) # Insert temp Null B before object B

    if h == True: # If 'Swap in Object Manager' is checked
        objA.InsertAfter(tempNullB) # Move object
        objB.InsertAfter(tempNullA) # Move object

    if p == True: # If 'Position' is checked
        posA = GetGlobalPosition(objA) # Get object A's global position
        posB = GetGlobalPosition(objB) # Get object B's global position
        SetGlobalPosition(objA, posB) # Set new position for A
        SetGlobalPosition(objB, posA) # Set new position for B

    if s == True: # If 'Scale' is checked
        sclA = GetGlobalScale(objA) # Get object A's global scale
        sclB = GetGlobalScale(objB) # Get object B's global scale
        SetGlobalScale(objA, sclB) # Set new scale for A
        SetGlobalScale(objB, sclA) # Set new scale for B

    if r == True: # If 'Rotation' is checked
        rotA = GetGlobalRotation(objA) # Get object A's global rotation
        rotB = GetGlobalRotation(objB) # Get object B's global rotation
        SetGlobalRotation(objA, rotB) # Set new rotation for A
        SetGlobalRotation(objB, rotA) # Set new rotation for B

    #objA.SetMg(matB) # Set new matrix to object A
    #objB.SetMg(matA) # Set new matrix to object B
    
    tempNullA.Remove() # Delete temporary objects
    tempNullB.Remove()
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    return True # Everything is fine

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create the dialog
    def CreateLayout(self):
        self.SetTitle("Swap") # Set dialog title

        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 1, 1) # Begin Main group
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space

        self.AddCheckbox(CHK_POS, c4d.BFH_LEFT, 0, 0, "Position")
        self.AddCheckbox(CHK_SCL, c4d.BFH_LEFT, 0, 0, "Scale")
        self.AddCheckbox(CHK_ROT, c4d.BFH_LEFT, 0, 0, "Rotation")
        self.AddCheckbox(CHK_OM, c4d.BFH_LEFT, 0, 0, "Swap in Object Manager")

        self.SetBool(CHK_POS, True)
        self.SetBool(CHK_SCL, True)
        self.SetBool(CHK_ROT, True)

        self.GroupEnd() # End Main group

        # Buttons
        self.GroupBegin(GRP_BTN, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin Buttons group
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(BTN_CNL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End Buttons group

        return True

    # Processing GUI events
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        bc = c4d.BaseContainer() # Initialize a base container

        p = self.GetBool(CHK_POS)
        s = self.GetBool(CHK_SCL)
        r = self.GetBool(CHK_ROT)
        h = self.GetBool(CHK_OM)

        # User presses Cancel button
        if paramid == BTN_CNL:
            self.Close() # Close dialog
        
        # User presses Ok button
        if paramid == BTN_OK:
            SwapObjects(p, s, r, h) # Run the main function
            self.Close() # Close dialog

        # User presses ESC key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        # User presses ENTER key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close() # Close dialog

        return True # Everything is fine

#
def main():
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "None":
        SwapObjects(True, True, True, False) # Pos, Scl, Rot
    elif keyMod == "Shift":
        dlg = Dialog() # Create a dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog
    elif keyMod == "Ctrl":
        SwapObjects(False, False, False, True) # Hierarchy only

# Execute main()
if __name__=='__main__':
    main()