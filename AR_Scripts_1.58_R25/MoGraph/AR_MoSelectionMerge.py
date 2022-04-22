"""
AR_MoSelectionMerge

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoSelectionMerge
Version: 1.0.1
Description-US: Merges selected MoGraph Selection Tag into one tag
Note: If you have nested MoGraph Generator, disable parent generators before running this script

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

To Do:
- Option to keep old tags

Change log:
1.0.1 (29.03.2022) - Support for R25
"""

# Libraries
import c4d
from c4d.modules import mograph as mo

# Functions
def SortTags(items):
    msTags = [] # Init list for polygon selection tags
    objects = [] # Init list for objects

    # Sort
    for t in items:
        if t.GetType() == 1021338: # MoGraph selection tag
            msTags.append(t)
            objects.append(t.GetObject().GetGUID())

    objects = list(dict.fromkeys(objects)) # Remove duplicates
    return msTags, objects

def MergeMoGraphSelectionTags(msTags, objects):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document    
    nameSet = False # If name is not set
    for o in objects:
        collectedMsTags = []
        for t in msTags:
            k = t.GetObject()
            if k != None:
                if k.GetGUID() == o:
                    collectedMsTags.append(t)

        if len(collectedMsTags) >= 2:
            mgSelTag = c4d.BaseTag(1021338) # Initialize MoGraph selection tag
            selection = c4d.BaseSelect() # Initialize a base select
            nameSet = False # If name is not set
            for i in collectedMsTags: # Iterate through tags
                if not nameSet: # If name is not set
                    mgSelTag.SetName(i.GetName()) # Set name
                    nameSet = True
                selection.Merge(mo.GeGetMoDataSelection(i)) # Merge selections
            i.GetObject().InsertTag(mgSelTag, i.GetObject().GetLastTag()) # Insert tag to object
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, mgSelTag) # Record undo for inserting a new tag
            mo.GeSetMoDataSelection(mgSelTag, selection) # Set MoGraph selection
            mgSelTag.SetBit(c4d.BIT_ACTIVE) # Select tag
    for r in msTags:
        doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, r) # Record undo for deleting a tag
        r.Remove() # Detele the tag

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    collectedObjects = [] # Collect objects
    collectedTags = [] # Collect tags    
    selection = doc.GetSelection() # Get selected items    
    for s in selection: # Iterate through selection
        if (type(s).__name__ == "BaseObject"):
            collectedObjects.append(s)
        elif s.GetType() == 1021338:
            collectedTags.append(s)
    if len(collectedTags) == 0: # If no tags selected
        for i, obj in enumerate(collectedObjects):
            collectedTags = []
            tags = obj.GetTags()
            for t in tags:
                if t.GetType() == 1021338:
                    collectedTags.append(t)
            msTags, objects = SortTags(collectedTags)
            MergeMoGraphSelectionTags(msTags, objects) #Run the merge function
    else: # If tags selected
        msTags, objects = SortTags(selection)
        MergeMoGraphSelectionTags(msTags, objects) #Run the merge function    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()