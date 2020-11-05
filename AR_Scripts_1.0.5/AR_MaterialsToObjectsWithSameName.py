"""
AR_MaterialsToObjectsWithSameName

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MaterialsToObjectsWithSameName
Version: 1.0.0
Description-US: Puts materials to objects that has same name. Supports object selection.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

"""
# Libraries
import c4d
from c4d import gui

# Functions
def GetNextObject(op):
    """
    Returns the next op.

    Args:
        op: (todo): write your description
    """
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def InsertMaterialTag(op, m):
    """
    Create a new tag.

    Args:
        op: (todo): write your description
        m: (todo): write your description
    """
    tag = c4d.BaseTag(5616) # Initialize a material tag
    tag[c4d.TEXTURETAG_MATERIAL] = m # Assign material to the material tag
    tag[c4d.TEXTURETAG_PROJECTION] = 6 #UVW Mapping
    op.InsertTag(tag) # Insert tag to the object
    doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Record undo for adding tag

def MatsToObjsWithSameName(op, m, selection, doc):
    """
    Perform a mats of the given operations *

    Args:
        op: (todo): write your description
        m: (todo): write your description
        selection: (str): write your description
        doc: (str): write your description
    """
    if op is None:
        return
    while op:
        if selection:
            if op.GetName() == m.GetName(): # If there are object
                if op.GetBit(c4d.BIT_ACTIVE): # If object is selected
                    InsertMaterialTag(op, m) # Insert material tag to selected object
        else:
            if op.GetName() == m.GetName(): # If there are object
                InsertMaterialTag(op, m) # Insert material tag to the object
        op = GetNextObject(op)
    return True

def main():
    """
    The main function.

    Args:
    """
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get active objects
    materials = doc.GetMaterials() # Get all materials
    startObject = doc.GetFirstObject() # Get the first object of the document
    for m in materials: # Iterate through materials
        MatsToObjsWithSameName(startObject, m, selection, doc) # Run the main function            
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
        
# Execute main()
if __name__=='__main__':
    main()