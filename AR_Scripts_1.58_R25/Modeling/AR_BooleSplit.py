"""
AR_BooleSplit

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_BooleSplit
Version: 1.0.0
Description-US: Splits selected objects in half

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

To do:
- Option to convert boole setup to single object (current state to object + connect and delete)
"""

# Libraries
import c4d
from c4d.gui import GeDialog

# GUI IDs
GRP_MAIN    = 1000
GRP_BTN     = 1008
GRP_CHECK   = 1016

COMBO_AXIS  = 1001
COMBO_SPACE = 1009
COMBO_MODE  = 1018

TEXT_AXIS   = 1008
TEXT_SPACE  = 1010
TEXT_SIZE   = 1016
TEXT_MODE   = 1021

EDIT_SIZE   = 1017

AXIS_XP     = 1002
AXIS_XM     = 1003
AXIS_YP     = 1004
AXIS_YM     = 1005
AXIS_ZP     = 1006
AXIS_ZM     = 1007

MODE_COPY   = 1019 
MODE_INST   = 1020

SPC_LOCAL   = 1011
SPC_GLOBAL  = 1012

CHECK_HQ    = 1013
CHECK_SINGLE= 1014
CHECK_HIDE  = 1015

CHECK_PIVOT = 1022

BTN_OK      = 2001
BTN_CANCEL  = 2002

# Functions
def Offset(obj, axis, size):
    if axis == AXIS_XP: # X+
        obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = size * 0.5
    elif axis == AXIS_XM: # X-
        obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = -size * 0.5
    elif axis == AXIS_YP: # Y+
        obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = size * 0.5
    elif axis == AXIS_YM: # Y-
        obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = -size * 0.5
    elif axis == AXIS_ZP: # Z+
        obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = size * 0.5
    elif axis == AXIS_ZM: # Z-
        obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = -size * 0.5
    return

def BooleCut(mode, space, axis, hq, single, hide, size, pivot):
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if len(selection) == 0:
        return False

    cube = c4d.BaseObject(c4d.Ocube) # Init a cube object
    cube.SetName("Cut Cube") # Set cube's name

    if mode == MODE_COPY:
        pass 
    elif mode == MODE_INST:
        null = c4d.BaseObject(c4d.Onull) # Init a null object
        null.SetName("Boole Null") # Set null's name
        null[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
        null[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1    
        cube.InsertUnder(null) # Insert cube under null
        doc.AddUndo(c4d.UNDOTYPE_NEW, null) # Add undo for inserting null to doc
        doc.InsertObject(null) # Insert null to document

    cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_X] = size # Set cube's size
    cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Y] = size
    cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Z] = size

    Offset(cube, axis, size) # Offset cube object

    for s in selection:
        boole = c4d.BaseObject(1010865) # Init a boole object
        boole.SetName("Boole "+s.GetName()) # Set boole's name
        boole[c4d.BOOLEOBJECT_HIGHQUALITY] = hq
        boole[c4d.BOOLEOBJECT_SINGLE_OBJECT] = single
        boole[c4d.BOOLEOBJECT_HIDE_NEW_EDGES] = hide
        boole.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_SET) # Unfold
        doc.AddUndo(c4d.UNDOTYPE_NEW, boole) # Add undo for inserting boole object to doc
        
        if pivot == True:
            pivotNull = c4d.BaseObject(c4d.Onull) # Init a pivot null
            pivotNull.SetName("Pivot") # Set name
            pivotNull.InsertUnder(boole)

        if space == SPC_LOCAL:
            boole.SetMg(s.GetMg()) # Set boole's global matrix
        boole.InsertBefore(s) # Insert boole to doc before 's' object

        if mode == MODE_INST:
            instance = c4d.BaseObject(5126) # Init a instance object
            instance.SetName(cube.GetName()+"_Instance") # Set instance's name
            instance[c4d.INSTANCEOBJECT_LINK] = cube # Set instance link
            
            if pivot == True:
                instance.InsertUnder(pivotNull) # Insert instance object under pivot null
            else:
                instance.InsertUnder(boole) # Insert instance object under boole
            
            if space == SPC_LOCAL:
                instance.SetMg(boole.GetMg()) # Set instance's global matrix
                Offset(instance, axis, size)
            if space == SPC_GLOBAL:
                instance.SetMg(cube.GetMg()) # Set instance's global matrix

        elif mode == MODE_COPY:
            cubeCopy = cube.GetClone()
            cubeCopy.InsertUnder(boole) # Insert instance object under boole
            
            if pivot == True:
                cubeCopy.InsertUnder(pivotNull) # Insert instance object under pivot null
            else:
                cubeCopy.InsertUnder(boole) # Insert instance object under boole
            
            if space == SPC_LOCAL:
                cubeCopy.SetMg(boole.GetMg()) # Set instance's global matrix
                Offset(cubeCopy, axis, size)
            if space == SPC_GLOBAL:
                cubeCopy.SetMg(cube.GetMg()) # Set instance's global matrix

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo for changing 's' object's position in the object hierarchy
        s.InsertUnder(boole) # Insert 's' object under boole

        if space == SPC_LOCAL:
            s.SetMg(boole.GetMg())


    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
    return True

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create the dialog
    def CreateLayout(self):
        self.SetTitle("Boole Cut") # Set dialog title

        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 2, 1) # Begin Main group
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space

        self.AddStaticText(TEXT_MODE, c4d.BFH_LEFT, 0, 13, "Mode", 0)

        self.AddComboBox(COMBO_MODE, c4d.BFH_LEFT, 70, 13)
        self.AddChild(COMBO_MODE, MODE_COPY, "Copy")
        self.AddChild(COMBO_MODE, MODE_INST, "Instance")

        self.SetInt32(COMBO_MODE, MODE_INST) # Set default value

        self.AddStaticText(TEXT_SPACE, c4d.BFH_LEFT, 0, 13, "Space", 0)

        self.AddComboBox(COMBO_SPACE, c4d.BFH_LEFT, 60, 13)
        self.AddChild(COMBO_SPACE, SPC_GLOBAL, "Global")
        self.AddChild(COMBO_SPACE, SPC_LOCAL, "Local")

        self.SetInt32(COMBO_SPACE, SPC_GLOBAL) # Set default space

        self.AddStaticText(TEXT_AXIS, c4d.BFH_LEFT, 0, 13, "Axis", 0)

        self.AddComboBox(COMBO_AXIS, c4d.BFH_LEFT, 50, 13)
        self.AddChild(COMBO_AXIS, AXIS_XP, "X+")
        self.AddChild(COMBO_AXIS, AXIS_XM, "X-")
        self.AddChild(COMBO_AXIS, AXIS_YP, "Y+")
        self.AddChild(COMBO_AXIS, AXIS_YM, "Y-")
        self.AddChild(COMBO_AXIS, AXIS_ZP, "Z+")
        self.AddChild(COMBO_AXIS, AXIS_ZM, "Z-")

        self.SetInt32(COMBO_AXIS, AXIS_XP) # Set default axis

        self.AddStaticText(TEXT_SIZE, c4d.BFH_LEFT, 0, 13, "Size", 0)
        self.AddEditNumberArrows(EDIT_SIZE, c4d.BFH_LEFT, 50, 13)

        self.SetInt32(EDIT_SIZE, 10000) # Set default size

        self.GroupEnd() # End Main group

        # Boolean settings
        self.GroupBegin(GRP_CHECK, c4d.BFH_CENTER, 1, 3, "Boolean settings")
        self.GroupBorder(c4d.BORDER_BLACK)
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space

        self.AddCheckbox(CHECK_HQ, c4d.BFH_LEFT, 0, 0, "High Quality")
        self.AddCheckbox(CHECK_SINGLE, c4d.BFH_LEFT, 0, 0, "Create single object")
        self.AddCheckbox(CHECK_HIDE, c4d.BFH_LEFT, 0, 0, "Hide new edges")

        self.SetBool(CHECK_HQ, True) # Set default value
        self.SetBool(CHECK_HIDE, True) # Set default value
        
        self.GroupEnd() # End Check group
        
        # Pivot null
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 2, 1) # Begin Main group
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space
        
        self.AddCheckbox(CHECK_PIVOT, c4d.BFH_LEFT, 0, 0, "Add Pivot Null")
        
        self.GroupEnd() # End Main group
        
        # Buttons
        self.GroupBegin(GRP_BTN, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin Buttons group
        self.GroupBorderSpace(5, 5, 5, 5) # Add border space

        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End Buttons group

        return True

    # Processing GUI events
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        bc = c4d.BaseContainer() # Initialize a base container

        mode   = self.GetInt32(COMBO_MODE) # Get 'mode' option
        space  = self.GetInt32(COMBO_SPACE) # Get 'space' option
        axis   = self.GetInt32(COMBO_AXIS) # Get 'axis' option
        hq     = self.GetBool(CHECK_HQ) # Get 'high quality' option
        single = self.GetBool(CHECK_SINGLE) # Get 'high quality
        hide   = self.GetBool(CHECK_HIDE) # Get 'hide new edges'' option
        size   = self.GetInt32(EDIT_SIZE) # Get 'size'
        pivot  = self.GetBool(CHECK_PIVOT) # Get 'pivot' option

        if hq == False:
            self.Enable(CHECK_SINGLE, False)
            self.Enable(CHECK_HIDE, False)
            pass
        elif hq == True:
            self.Enable(CHECK_SINGLE, True)
            self.Enable(CHECK_HIDE, True)
            pass

        # User presses Cancel button
        if paramid == BTN_CANCEL:
            self.Close() # Close dialog
        
        # User presses Ok button
        if paramid == BTN_OK:
            BooleCut(mode, space, axis, hq,single, hide, size, pivot) # Run the main function
            self.Close() # Close dialog

        # User presses ESC key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        # User presses ENTER key
        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            BooleCut(mode, space, axis, hq,single, hide, size, pivot) # Run the main function
            self.Close() # Close dialog

        return True # Everything is fine

dlg = Dialog() # Create a dialog object
dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog


#ChangeNBit()