"""
AR_TagsSelect

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TagsSelect
Version: 1.1.0
Description-US: Select object(s) tag(s). Shift: Add to selection Ctrl: Remove from selection

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.1.0 (24.09.2022) - Updated logic similar to AR_TagsDelete script
1.0.1 (24.03.2022) - Updated for R25
"""

# Libraries
import c4d

# Global variables
keepTags = [5604, # PolygonTag
            5600] # PointTag]

# Functions
def Select(lst):
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(lst):
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def SelectTags(op, tag, sel):
    if op is None: # If there is no object
        return
    while op: # While there is object
        if sel == True:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                if tag != None: # If tag is not 'None'
                    tags = op.GetTags() # Get tags of object
                    for t in tags: # Loop Through tags
                        if t.GetType() == tag.GetType():
                            doc.AddUndo(c4d.UNDOTYPE_BITS, t) # Record undo for changing bits
                            t.SetBit(c4d.BIT_ACTIVE) # Select tag
                else:
                    tags = op.GetTags() # Get tags of object
                    for t in tags: # Loop Through tags
                        if t.GetType() not in keepTags:
                            doc.AddUndo(c4d.UNDOTYPE_BITS, t) # Record undo for changing bits
                            t.SetBit(c4d.BIT_ACTIVE) # Select tag
            doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
            op.DelBit(c4d.BIT_ACTIVE) # Deselect object
            op = GetNextObject(op) # Get next object
        elif sel == False:
            if tag != None: # If tag is not 'None'
                tags = op.GetTags() # Get tags of object
                for t in tags: # Loop Through tags
                    if t.GetType() == tag.GetType():
                        doc.AddUndo(c4d.UNDOTYPE_BITS, t) # Record undo for changing bits
                        t.SetBit(c4d.BIT_ACTIVE) # Select tag
            else:
                tags = op.GetTags() # Get tags of object
                for t in tags: # Loop Through tags
                    if t.GetType() not in keepTags:
                        doc.AddUndo(c4d.UNDOTYPE_BITS, t) # Record undo for changing bits
                        t.SetBit(c4d.BIT_ACTIVE) # Select tag
            doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
            op.DelBit(c4d.BIT_ACTIVE) # Deselect object
            op = GetNextObject(op) # Get next object
    return True

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get active selection

    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag, c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag, c4d.modules.character.CAWeightTag,
    c4d.VariableTag, c4d.modules.graphview.XPressoTag, c4d.VertexColorTag, c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags
    selection = doc.GetSelection() # Get active selection
    activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active objects
    selectedTags = [] # Initialize a list
    start_object = doc.GetFirstObject() # Get first object

    if activeObjects:
        sel = True  # There is object selection
    elif not activeObjects:
        sel = False # No object selection

    for s in selection : # Loop through selection
        if type(s) in commonTags: # If selected item is a tag
            if type(s) not in keepTags: # If tag is not listed in keepTags
                selectedTags.append(s) # Selected tag type is doomed

    for tag in selectedTags: # Iterate through selected tags
        SelectTags(start_object, tag, sel) # Do the thing

    if len(selectedTags) == 0:
        SelectTags(start_object, None, sel) # Do the thing

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()