"""
AR_TakeMatte

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TakeMatte
Version: 1.0.0
Description-US: Creates matte take from selected materials.

NOTE: Create one child take (clone of the main take) to make this script fully function correctly

Written for Maxon Cinema 4D 2024.1.0
Python version 3.11.4

Change log:
1.0.0 (25.12.2023) - Initial realease
"""

# Libraries
import c4d
from c4d import gui
from c4d.gui import GeDialog

# Global variables
GRP_MAIN     = 1000
GRP_OPTIONS  = 1001
GRP_BUTTONS  = 1002

STR_TAKENAME = 4000
STR_WHITE    = 4001
STR_BLACK    = 4002

OPT_TAKENAME = 2000
OPT_WHITE    = 2001
OPT_BLACK    = 2002

BTN_OK       = 3000
BTN_CANCEL   = 3001

# Functions
def SearchMaterial(name):
    materials = doc.GetMaterials() # Get materials
    for m in materials: # Iterate through materials
        if m.GetName() == name: # If material name matches
            return m # Return material

def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectMaterialTags(op):
    materialTags = []
    if op is None:
        return
    while op:
        tags = op.GetTags()
        for t in tags:
            if t.GetType() == 5616: # Material tag
                    materialTags.append(t)
        op = GetNextObject(op)
    return materialTags

def GetLastTake(mainTake):
    nextTake = mainTake.GetDown()
    while nextTake:
        prevTake = nextTake
        nextTake = nextTake.GetNext()
    return prevTake

def CreateTake(takeName, whiteMaterial, blackMaterial):
    doc.StartUndo() # Start recording undos

    # Collect stuff
    materials = doc.GetMaterials() # Get materials
    materialTags = CollectMaterialTags(doc.GetFirstObject()) # Get all material tags

    if len(materials) == 0: # If no materials
        return False

    if len(materialTags) == 0: # If no material tags
        return False

    # Selected materials
    selectedMaterials    = [] # Initialize array for selected materials
    notSelectedMaterials = [] # Initialize array for non selected materials
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE) == True: # If materials is selected
            selectedMaterials.append(m) # Add material to array
        else:
            notSelectedMaterials.append(m) # Add material to array

    if len(selectedMaterials) == 0: # If no selected materials
        return False

    # Take stuff
    takeData  = doc.GetTakeData() # Get take data
    mainTake  = takeData.GetMainTake() # Get main take
    childTake = mainTake.GetDown() # Get first child take
        
    newTake = takeData.AddTake("", mainTake, childTake) # Add take

    newTake.SetName(takeName) # Set name

    takeData.SetCurrentTake(newTake) # Set current/active take
    takeData.InsertTake(newTake, GetLastTake(mainTake), c4d.INSERT_AFTER)

    # Material tags
    for t in materialTags: # Iterate through material tags

        for s in notSelectedMaterials: # Iterate through non selected materials
            if t[c4d.TEXTURETAG_MATERIAL] == s: # If material tag is using selected material
                tClone = t.GetClone() # Get clone of the material tag
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, t) # Add undo for modifying tag
                t[c4d.TEXTURETAG_MATERIAL] = blackMaterial # Set white material
                newTake.AutoTake(takeData, t, tClone) # Modify take

        for s in selectedMaterials: # Iterate through selected materials
            if t[c4d.TEXTURETAG_MATERIAL] == s: # If material tag is using selected material
                tClone = t.GetClone() # Get clone of the material tag
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, t) # Add undo for modifying tag
                t[c4d.TEXTURETAG_MATERIAL] = whiteMaterial # Set white material
                newTake.AutoTake(takeData, t, tClone) # Modify take

    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, newTake) # Add undo for creating a take
    doc.EndUndo() # Stop recording undos

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()

    # Create Dialog
    def CreateLayout(self):
        # ----------------------------------------------------------------------------------------
        self.SetTitle("Matte Take") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 1, 1) # Begin 'Main' group
        self.GroupBorderSpace(9, 0, 9, 9)
        # ----------------------------------------------------------------------------------------
        # Options
        self.GroupBegin(GRP_OPTIONS, c4d.BFH_LEFT, 2, 1, "Options") # Begin 'Anchor' group
        self.GroupBorderSpace(5, 5, 5, 0)

        self.AddStaticText(STR_TAKENAME, c4d.BFH_LEFT, name = "Take Name")
        self.AddEditText(OPT_TAKENAME, c4d.BFH_LEFT, 150, 10)

        self.AddStaticText(STR_WHITE, c4d.BFH_LEFT, name = "White Material")
        self.AddEditText(OPT_WHITE, c4d.BFH_LEFT, 150, 10)

        self.AddStaticText(STR_BLACK, c4d.BFH_LEFT, name = "Black Material")
        self.AddEditText(OPT_BLACK, c4d.BFH_LEFT, 150, 10)

        self.GroupEnd() # End 'Anchor' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_BUTTONS, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        # Buttons
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Ok") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_LEFT, name="Cancel") # Add button
        self.GroupEnd() # End 'Buttons' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # Begin 'Main' group
        # ----------------------------------------------------------------------------------------
        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        renderData = doc.GetActiveRenderData() # Get document render data

        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button pressed
            self.Close() # Close dialog

        if paramid == BTN_OK: # If 'Ok' button pressed
            takeName = self.GetString(OPT_TAKENAME) # Get take name
            if takeName == "":
                return False

            whiteName = self.GetString(OPT_WHITE) # Get white material name
            if whiteName == "":
                return False

            blackName = self.GetString(OPT_BLACK) # Get black material name
            if whiteName == "":
                return False

            whiteMaterial = SearchMaterial(whiteName) # Search white material
            if whiteMaterial == None:
                return False

            blackMaterial = SearchMaterial(blackName) # Search black material
            if blackMaterial == None:
                return False

            CreateTake(takeName, whiteMaterial, blackMaterial)

            c4d.EventAdd() # Refresh Cinema 4D

        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2, 5, 5) # Open dialog