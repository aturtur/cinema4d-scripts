"""
AR_MoGraphSelectionFromGivenRange

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoGraphSelectionFromGivenRange
Description-US: Create MoGraph selection from given range
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d.modules import mograph as mo
from c4d import gui as g

# Functions
def MoGraphSelectionFromRange(obj):
    #try:
    tag = obj.GetLastTag() # Get last tag of object
    tags = obj.GetTags() # Get object's tags
    md = mo.GeGetMoData(obj) # Get MoGraph data
    cnt = md.GetCount() # Get clone count
    prefix = "ms" # Prefix for selection tag
    sep = "_" # Separator for selection tag
    p = 0 # Initialize iteration variable
    userInput = g.InputDialog("Selected IDs for "+obj.GetName(),"") # User input dialog
    baseList = userInput.split(",") # Split user input to list
    add = [] # Initialize empty list
    finalList = []  # Initialize empty list
    for x in baseList: # Loop through list items
        rng = x.split("-") # Split range value (e.g. 5-15)
        if len(rng)>1:
            for i in xrange(int(rng[0]),int(rng[1])+1):
                add.append(i)
    fullList = baseList+add
    for f in fullList:
        if type(f) is int:
            finalList.append(f)
        if type(f) is not int:
            if f.find("-") is -1:
                finalList.append(f)
    for k in reversed(tags): # Loop through tags
        if k.GetName().split("_")[0] == prefix:
            p = p+1 # Increase iteration
    t = c4d.BaseTag(1021338) # Initialize MoGraph Selection tag
    t[c4d.ID_BASELIST_NAME] = prefix+sep+str(p) # Set tag name
    s = c4d.BaseSelect() # Initialize BaseSelect
    for f in finalList: # Loop through list
        s.Select(int(f)) # Select items
    obj.InsertTag(t) # Insert tag to object
    doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
    mo.GeSetMoDataSelection(t, s) # Set MoGraph selection

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in selection: # Loop through selection
        MoGraphSelectionFromRange(obj) # Create MoGraph selection
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()