"""
AR_MoGraphSelectionTagsFromSelectedClones

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoGraphSelectionTagsFromSelectedClones
Version: 1.0
Description-US: Creates MoGraph Selection Tags for every selected clones

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d.modules import mograph as mo

#Functions
def MgSelTagsFromSelectedClones(obj):
    """
    Extracts a token from a - bgSel object.

    Args:
        obj: (todo): write your description
    """
    tag = obj.GetLastTag() # Get object's last tag
    tags = obj.GetTags() # Get object's tags
    md = mo.GeGetMoData(obj) # Get object's MoGraph data
    cnt = md.GetCount() # Get clone count
    selection = mo.GeGetMoDataSelection(tag) # Get selection from MoGraph selection tag
    prefix = "ms" # Prefix
    sep = "_" # Separator
    x = 0 # Initialize iteration variable
    for k in tags: # Loop through reversed list of tags
        if k.GetName().split("_")[0] == prefix:
            x = x + 1 # Increase iteration variable
    for i in xrange(0,cnt): # Loop through reversed list of clones
        if selection.IsSelected(i) == True:
            t = c4d.BaseTag(1021338) # Initialize MoGraph selection tag
            t[c4d.ID_BASELIST_NAME] = prefix+sep+str(x) # Set tag name
            s = c4d.BaseSelect() # Initialize BaseSelect
            s.Select(i) # Select clone
            obj.InsertTag(t, obj.GetLastTag()) # Insert new tag to object
            doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
            mo.GeSetMoDataSelection(t, s) # Set MoGraph selection
            x = x + 1 # Increase iteration variable
    tag.Remove() # Remove old tag
    doc.AddUndo(c4d.UNDOTYPE_DELETE, tag) # Add undo command for removing tag

def main():
    """
    The main routine.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active object(s)
    for obj in selection: # Loop through selection
        MgSelTagsFromSelectedClones(obj) # Create MoGraph selection tags from selected clones
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()