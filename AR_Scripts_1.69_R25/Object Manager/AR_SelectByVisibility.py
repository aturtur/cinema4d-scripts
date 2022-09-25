"""
AR_SelectByVisibility

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectByVisibility
Version: 1.0.2
Description-US: Selects objects by visibility

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.2 (26.06.2022) - Fixed script name
1.0.1 (29.03.2022) - Updated for R25
"""

# Libraries
import c4d
from c4d import gui
from c4d.gui import GeDialog
from c4d import utils as u

# Variables
GRP_MAIN = 1000
GRP_MINI = 1001
GRP_SOLO = 1002

TXT_VIEW = 2001
TXT_RENDER = 2002

COMBO_VIEW = 2003
COMBO_RENDER = 2004

OPT_ANY = 3001
OPT_ON  = 3002
OPT_OFF = 3003
OPT_DEFAULT = 3004

CHK_USESEL = 5001

BTN_SELECT = 4001
BTN_DESELECT = 4002

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

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def Select(lst):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    for l in lst: # Iterate through objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo
        l.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(lst):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    for l in lst: # Iterate through objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo
        l.DelBit(c4d.BIT_ACTIVE) # Deselect object

def CollectObjects(op):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    objectList = []
    if op is None:
        return
    while op:
        objectList.append(op)
        op = GetNextObject(op) # Get next object
    return objectList

def CheckObjects(objects, editor, render):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selectionList = []
    for op in objects:
        # Editor
        if editor == OPT_ANY:
            if render == OPT_ANY:
                selectionList.append(op) # Add object to the selection list
            elif render == OPT_ON:
                if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 0: # On
                    selectionList.append(op)
            elif render == OPT_OFF:
                if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1: # Off
                    selectionList.append(op)
            elif render == OPT_DEFAULT:
                if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 2: # Default
                    selectionList.append(op)

        elif editor == OPT_ON:
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 0:
                if render == OPT_ANY:
                    selectionList.append(op)
                elif render == OPT_ON:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 0:
                        selectionList.append(op)
                elif render == OPT_OFF:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1:
                        selectionList.append(op)
                elif render == OPT_DEFAULT:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 2:
                        selectionList.append(op)

        elif editor == OPT_OFF:
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 1:
                if render == OPT_ANY:
                    selectionList.append(op)
                elif render == OPT_ON:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 0:
                        selectionList.append(op)
                elif render == OPT_OFF:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1:
                        selectionList.append(op)
                elif render == OPT_DEFAULT:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 2:
                        selectionList.append(op)

        elif editor == OPT_DEFAULT:
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 2:
                if render == OPT_ANY:
                    selectionList.append(op)
                elif render == OPT_ON:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 0:
                        selectionList.append(op)
                elif render == OPT_OFF:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1:
                        selectionList.append(op)
                elif render == OPT_DEFAULT:
                    if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 2:
                        selectionList.append(op)

    return selectionList

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()

    # Create Dialog
    def CreateLayout(self):
        # ----------------------------------------------------------------------------------------
        self.SetTitle("Select by Visibility") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 1, 1) # Begin 'Main' group
        self.GroupBorderSpace(9, 0, 9, 9)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MINI, c4d.BFH_CENTER, 2, 1) # Begin 'Mini' group

        self.AddStaticText(TXT_VIEW, c4d.BFH_LEFT, 0, 13, "Editor", 0)
        self.AddComboBox(COMBO_VIEW, c4d.BFH_LEFT, 80, 13)
        self.AddChild(COMBO_VIEW, OPT_ANY, "Any")
        self.AddChild(COMBO_VIEW, OPT_DEFAULT, "Default")
        self.AddChild(COMBO_VIEW, OPT_ON, "On")
        self.AddChild(COMBO_VIEW, OPT_OFF, "Off")

        self.SetInt32(COMBO_VIEW, OPT_ON)

        self.AddStaticText(TXT_RENDER, c4d.BFH_LEFT, 0, 13, "Render", 0)
        self.AddComboBox(COMBO_RENDER, c4d.BFH_LEFT, 80, 13)
        self.AddChild(COMBO_RENDER, OPT_ANY, "Any")
        self.AddChild(COMBO_RENDER, OPT_DEFAULT, "Default")
        self.AddChild(COMBO_RENDER, OPT_ON, "On")
        self.AddChild(COMBO_RENDER, OPT_OFF, "Off")

        self.SetInt32(COMBO_RENDER, OPT_ANY)

        self.GroupEnd() # Begin 'Mini' group

        self.GroupBegin(GRP_SOLO, c4d.BFH_CENTER, 2, 1) # Begin 'Solo' group
        self.GroupBorderSpace(0, 5, 0, 0)
        self.AddCheckbox(CHK_USESEL, c4d.BFH_LEFT, 0, 13, "Use current selection")
        self.GroupEnd() # Begin 'Solo' group

        self.GroupBegin(GRP_MINI, c4d.BFH_CENTER, 2, 1) # Begin 'Mini' group
        self.GroupBorderSpace(0, 5, 0, 0)
        self.AddButton(BTN_SELECT, c4d.BFH_LEFT, name="Select") # Add button
        self.AddButton(BTN_DESELECT, c4d.BFH_LEFT, name="Deselect") # Add button
        self.GroupEnd() # Begin 'Mini' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # Begin 'Main' group
        # ----------------------------------------------------------------------------------------
        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document

        # Actions here
        if paramid == BTN_SELECT: # If 'Select' button pressed
            editor = self.GetInt32(COMBO_VIEW)
            render = self.GetInt32(COMBO_RENDER)
            usesel = self.GetBool(CHK_USESEL)
            
            doc.StartUndo() # Start recording undos

            if usesel == True:
                selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
                Deselect(selection)
                selectionList = CheckObjects(selection, editor, render)
                Select(selectionList)

            else:
                start_object = doc.GetFirstObject()
                objectList = CollectObjects(start_object)
                selectionList = CheckObjects(objectList, editor, render)
                Select(selectionList)
            
            doc.EndUndo() # Stop recording undos

        if paramid == BTN_DESELECT: # If 'Deselect' button pressed
            editor = self.GetInt32(COMBO_VIEW)
            render = self.GetInt32(COMBO_RENDER)

            doc.StartUndo() # Start recording undos
            start_object = doc.GetFirstObject()
            objectList = CollectObjects(start_object)
            selectionList = CheckObjects(objectList, editor, render)
            Deselect(selectionList)
            doc.EndUndo() # Stop recording undos

        c4d.EventAdd() # Refresh Cinema 4D
        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2, 5, 5) # Open dialog