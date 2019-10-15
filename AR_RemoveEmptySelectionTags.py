"""
AR_RemoveEmptySelectionTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveEmptySelectionTags
Description-US: Removes empty selection tags from selected object's
Written for Maxon Cinema 4D R21.026
"""
# Libraries
import c4d

# Functions
def main():
    selectionTags = [5673, # Polygon selection
                     5674, # Point selection
                     5701] # Edge selection
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get selected objects
    for s in selection: # Iterate through selection
        tags = s.GetTags() # Get object's tags
        for t in tags: # Iterate through tags
            if t.GetType() in selectionTags: # If tag is a selection tag
                baseSelect = t.GetBaseSelect() # Get base select
                if baseSelect.GetCount() == 0: # If empty selection tag
                    doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Record undo
                    t.Remove() # Delete tag

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()