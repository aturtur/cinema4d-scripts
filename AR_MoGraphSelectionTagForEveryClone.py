"""
AR_MoGraphSelectionTagForEveryClone

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoGraphSelectionTagForEveryClone
Description-US: Creates MoGraph Selection Tag for every clone
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d.modules import mograph as mo

# Functions
def MgSelTagForEveryClone(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    try: # Try to execute following
        md = mo.GeGetMoData(obj) # Get MoGraph data
        cnt = md.GetCount() # Get clone count
        for i in reversed(xrange(0, cnt)): # Loop through clones
            tag = c4d.BaseTag(1021338) # Initialize MoGraph selection tag
            tag[c4d.ID_BASELIST_NAME] = "ms_"+str(i)
            s = c4d.BaseSelect() # Initialize BaseSelect
            obj.InsertTag(tag) # Insert tag to object
            doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Add undo command for inserting tag
            s.Select(i) # Select clone
            mo.GeSetMoDataSelection(tag, s) # Set selection to tag
    except: # If something went wrong
        pass # Do nothing

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active object(s)
    for obj in selection: # Loop through selection
        MgSelTagForEveryClone(obj) # Create MoGraph selection tag for every clone
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()