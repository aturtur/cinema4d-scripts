"""
AR_MergeMoGraphSelectionTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MergeMoGraphSelectionTags
Version: 1.0
Description-US: Merges selected MoGraph Selection Tag into one tag
Note: If you have nested MoGraph Generator, disable parent generators before running this script

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

TO DO: Now you have to select object and the tags, modify the script that you only have to select the tags!

"""
# Libraries
import c4d
from c4d.modules import mograph as mo

# Functions
def MergeMoGraphSelectionTags(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    md = mo.GeGetMoData(obj) # Get MoGraph data
    mgSelTag = c4d.BaseTag(1021338) # Initialize MoGraph selection tag
    selection = c4d.BaseSelect() # Initialize a base select
    tags = obj.GetTags() # Get object's tags
    for t in tags: # Iterate through tags
        if t.GetType() == 1021338: # If MoGraph Selection Tag
            if t.GetBit(c4d.BIT_ACTIVE): # If tag is selected
                selection.Merge(mo.GeGetMoDataSelection(t)) # Merge selections
    obj.InsertTag(mgSelTag, obj.GetLastTag()) # Insert tag to object
    doc.AddUndo(c4d.UNDOTYPE_NEW, mgSelTag) # Record undo for inserting a new tag
    mo.GeSetMoDataSelection(mgSelTag, selection) # Set MoGraph selection

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active object(s)
    for obj in selection: # Loop through selection
        MergeMoGraphSelectionTags(obj) # Create MoGraph selection tag for every clone
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    print ("ok")

# Execute main()
if __name__=='__main__':
    main()