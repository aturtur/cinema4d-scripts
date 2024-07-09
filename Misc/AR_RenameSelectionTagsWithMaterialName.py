"""
AR_RenameSelectionTagsWithMaterialName

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RenameSelectionTagsWithMaterialName
Version: 1.0.0
Description-US: 

Written for Maxon Cinema 4D 2024.3.2
Python version 3.11.4

Change log:
1.0.0 (14.03.2024) - Initial Release
"""

# Libraries
import c4d

# Functions
def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def Iterate(op, sel):
    if op is None: # If there is no object
        return
    while op: # While there is object
        if sel == True:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                tags = op.GetTags() # Get tags of object
                for t in tags: # Loop Through tags
                    if type(t) == c4d.TextureTag:
                        RenameTag(t)
            op = GetNextObject(op) # Get next object

        elif sel == False:
            tags = op.GetTags() # Get tags of object
            for t in tags: # Loop Through tags
                if type(t) == c4d.TextureTag:
                    RenameTag(t)
            op = GetNextObject(op) # Get next object
    return True

def RenameTag(tag):
    polySelectionName = tag[c4d.TEXTURETAG_RESTRICTION]
    polySelectionTag = SearchPolySelect(tag, polySelectionName)

    if polySelectionTag != None:
        materialName = tag[c4d.TEXTURETAG_MATERIAL].GetName()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, polySelectionTag) # Record undo for changing bits
        polySelectionTag[c4d.ID_BASELIST_NAME] = materialName
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, tag) # Record undo for changing bits
        tag[c4d.TEXTURETAG_RESTRICTION] = materialName

def SearchPolySelect(tag, name):
    obj = tag.GetObject()
    tags = obj.GetTags()

    for t in tags:
        if t.GetType() == 5673: # If polygon selection tag
            if t.GetName() == name:
                return t
    return None

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    selection     = doc.GetSelection() # Get active selection
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active objects
    selectedTags  = [] # Initialize a list
    start_object  = doc.GetFirstObject() # Get first object

    if activeObjects:
        sel = True  # There is object selection
    elif not activeObjects:
        sel = False # No object selection

    for s in selection : # Loop through selection
        if type(s) == c4d.TextureTag: # If selected item is a tag
            selectedTags.append(s) # Selected tag type is doomed

    for tag in selectedTags: # Iterate through selected tags
        RenameTag(tag)

    if len(selectedTags) == 0:
        Iterate(start_object, sel)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()