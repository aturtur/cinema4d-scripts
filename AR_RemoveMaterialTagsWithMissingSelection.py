"""
AR_RemoveMaterialTagsWithMissingSelection

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveMaterialTagsWithMissingSelection
Description-US: Removes material tags that has missing selection restriction
Written for Maxon Cinema 4D R21.026
"""
# Libraries
import c4d

# Functions
def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get selected objects
    for s in selection: # Iterate through selected objects
        materialTags = [] # Init an array
        selectionTags = [] # Init an array
        tags = s.GetTags() # Get object's tags
        for t in tags: # Collect tags
            if t.GetType() == 5616: # If material tag
                materialTags.append(t)
            if t.GetType() == 5673: # Poylgon selection tag
                selectionTags.append(t.GetName())

        for m in materialTags: # Iterate through material tags
            restriction = m[c4d.TEXTURETAG_RESTRICTION] # Get polygon restriction
            if restriction not in selectionTags: # If not found in polygon selection tags
                if restriction != "":
                    doc.AddUndo(c4d.UNDO_DELETE, m)
                    m.Remove() # Remove tag
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main
if __name__=='__main__':
    main()