"""
AR_TakeMaterialPreviews

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TakeMaterialPreviews
Version: 1.0.0
Description-US: Creates take for each selected material assigned to selected object

Written for Maxon Cinema 4D 2024.1.0
Python version 3.11.4

Change log:
1.0.0 (26.12.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def GetLastTake(mainTake):
    nextTake = mainTake.GetDown()
    while nextTake:
        prevTake = nextTake
        nextTake = nextTake.GetNext()
    return prevTake

def CreateTake(material, materialTag, obj):
    doc.StartUndo() # Start recording undos

    # Take stuff
    takeData  = doc.GetTakeData() # Get take data
    mainTake  = takeData.GetMainTake() # Get main take
    childTake = mainTake.GetDown() # Get first child take

    newTake = takeData.AddTake("", mainTake, childTake) # Add take
    newTake.SetName(material.GetName()) # Set name
    takeData.InsertTake(newTake, GetLastTake(mainTake), c4d.INSERT_AFTER) # Move take
    takeData.SetCurrentTake(newTake) # Set current/active take

    undoClone = materialTag.GetClone() # Get clone of material tag
    materialTag[c4d.TEXTURETAG_MATERIAL] = material # Set matertial
    materialTag[c4d.TEXTURETAG_PROJECTION] = 6 # UVW Mapping
    newTake.AutoTake(takeData, materialTag, undoClone) # Modify take

    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, newTake) # Add undo for creating a take
    doc.EndUndo() # Stop recording undos

def main():
    materials = doc.GetMaterials() # Get materials
    selectedMaterials = [] # Initialize an array for selected materials
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE) == True: # If material is selected
            selectedMaterials.append(m) # Add material to array

    obj = doc.GetActiveObject() # Get selected object

    takeData  = doc.GetTakeData() # Get take data
    mainTake  = takeData.GetMainTake() # Get main take
    childTake = mainTake.GetDown() # Get first child take

    materialTag = c4d.BaseTag(5616) # Initialize a material tag
    obj.InsertTag(materialTag) # Insert material tag
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, materialTag) # Add undo step

    for m in selectedMaterials: # Iterate through selected materials
        CreateTake(m, materialTag, obj) # Create take
        takeData.SetCurrentTake(childTake) # Set current/active take

    c4d.EventAdd() # Refresh Cinema 4D

if __name__ == '__main__':
    main()