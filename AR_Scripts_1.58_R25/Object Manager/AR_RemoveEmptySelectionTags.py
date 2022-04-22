"""
AR_RemoveEmptySelectionTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveEmptySelectionTags
Version: 1.0.1
Description-US: Removes empty selection tags from selected object(s) or from all objects if no selection.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (30.03.2022) - Support for R25
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
 
def RemoveEmptySelectionTag(op, selection):
    selectionTags = [5673, # Polygon selection
                     5674, # Point selection
                     5701] # Edge selection
    if op is None:
        return
    while op:
        tags = op.GetTags() # Get tags of object
        if selection:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                for t in tags: # Iterate through tags
                    if t.GetType() in selectionTags: # If tag is a selection tag
                        baseSelect = t.GetBaseSelect() # Get base select
                        if baseSelect.GetCount() == 0: # If empty selection tag
                            doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Record undo
                            t.Remove() # Delete tag
        else:
            for t in tags: # Iterate through tags
                if t.GetType() in selectionTags: # If tag is a selection tag
                    baseSelect = t.GetBaseSelect() # Get base select
                    if baseSelect.GetCount() == 0: # If empty selection tag
                        doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Record undo
                        t.Remove() # Delete tag
        op = GetNextObject(op)
    return True

def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get selected objects
    start_object = doc.GetFirstObject() # Get first object
    if len(selection) != 0:
        RemoveEmptySelectionTag(start_object, True)
    else:
        RemoveEmptySelectionTag(start_object, False)
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()