"""
AR_SplitByPolySelection

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SplitByPolySelection
Version: 1.0
Description-US: Splits object to pieces by polygon selection tag(s)

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d import utils as u

# Functions
def RemoveTagsWithMissingSelection(op):
    materialTags = [] # Init an array
    selectionTags = [] # Init an array
    tags = op.GetTags() # Get object's tags
    for t in tags: # Collect tags
        if t.GetType() == 5616: # If material tag
            materialTags.append(t)
        if t.GetType() == 5673: # Polygon selection tag
            selectionTags.append(t.GetName())
            
    for m in materialTags: # Iterate through material tags
        restriction = m[c4d.TEXTURETAG_RESTRICTION] # Get polygon restriction
        if restriction not in selectionTags: # If not found in polygon selection tags
            if restriction != "":
                doc.AddUndo(c4d.UNDO_DELETE, m)
                m.Remove() # Remove tag
    return True

def RemoveEmptySelectionTag(op):
    selectionTags = [5673, # Polygon selection
                     5674, # Point selection
                     5701] # Edge selection
    tags = op.GetTags() # Get tags of object
    for t in tags: # Iterate through tags
        if t.GetType() in selectionTags: # If tag is a selection tag
            baseSelect = t.GetBaseSelect() # Get base select
            if baseSelect.GetCount() == 0: # If empty selection tag
                doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Record undo
                t.Remove() # Delete tag
    return True

def SplitCommand(op):
    if op != None:
        bc = c4d.BaseContainer()
        mode = c4d.MODELINGCOMMANDMODE_POLYGONSELECTION
        res = c4d.utils.SendModelingCommand(c4d.MCOMMAND_SPLIT, [op], mode, bc, doc)
        return res[0]

def SplitByPolySelection(obj):
    selectedPolys = obj.GetPolygonS()
    tags = obj.GetTags()
    for t in reversed(tags):
        if t.GetType() == 5673: # If polygon selection tag
            polygonSelection = t.GetBaseSelect()
            polygonSelection.CopyTo(selectedPolys)
            result = SplitCommand(obj)
            result.SetName(obj.GetName()+" "+t.GetName())
            result.InsertAfter(obj)
            doc.AddUndo(c4d.UNDOTYPE_NEW, result)
            RemoveEmptySelectionTag(result)
            RemoveTagsWithMissingSelection(result)

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    #try: # Try to execute following script
    selection = doc.GetActiveObjects(0) # Get active objects
    for s in selection: # Iterate through selected objects
        if s.GetType() == 5100: # If polygon object
            SplitByPolySelection(s) # Do the thing
    #except: # If something went wrong
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D  
  
# Execute main()
if __name__=='__main__':
    main()