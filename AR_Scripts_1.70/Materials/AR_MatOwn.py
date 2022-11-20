"""
AR_MatOwn

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MatOwn
Version: 1.0.1
Description-US: Creates own materials for every object from existing materials. Supports object selection.

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (24.03.2022) - Updated for R25
"""

# Libraries
import c4d

# Functions
def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def IterateHierarchy(op):
    if op is None:
        return
    while op:
        CreateOwnMaterials(op)
        op = GetNextObject(op)
    return

def CreateOwnMaterials(op):
    if isinstance(op, c4d.BaseObject): # If item is instance of Base Object
        tags = op.GetTags() # Get objects tags
        for t in tags: # Loop through tags
            if type(t).__name__ == "TextureTag": # If Texture tag founded
                objname = op.GetName() # Get object's name
                mat = t.GetMaterial() # Get material
                matname = mat.GetName() # Get material name
                copy = mat.GetClone() # Clone material
                copy.SetName(objname+"_"+matname) # Set cloned material name
                doc.InsertMaterial(copy) # Insert cloned material to document
                doc.AddUndo(c4d.UNDOTYPE_NEW, copy)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, t)
                t.SetMaterial(copy) # Set cloned material to object's texture tag
    return

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active objects
        if len(selection) != 0: # If object selection
            for x in reversed(selection): # Loop through selection
                CreateOwnMaterials(x) # Run the function
        else:
            IterateHierarchy(doc.GetFirstObject()) # Iterate all objects
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()