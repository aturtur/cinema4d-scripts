"""
AR_MoGraphSelectionTagsRange

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoGraphSelectionTagsRange
Version: 1.0
Description-US: Create MoGraph selection from given range

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d.modules import mograph as mo
from c4d import gui as g

# Functions
def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

def MoGraphSelectionFromRange(obj, keyMod):
    #try:
    userInput = g.InputDialog("Selected IDs for "+obj.GetName(),"") # User input dialog
    if userInput == "": return
    baseList = userInput.split(",") # Split user input to list
    add = [] # Initialize empty list
    finalList = []  # Initialize empty list
    for x in baseList: # Loop through list items
        rng = x.split("-") # Split range value (e.g. 5-15)
        if len(rng)>1:
            for i in range(int(rng[0]),int(rng[1])+1):
                add.append(i)
    fullList = baseList+add
    for f in fullList:
        if type(f) is int:
            finalList.append(f)
        if type(f) is not int:
            if f.find("-") is -1:
                finalList.append(f)

    if keyMod == "None":
        tags = obj.GetTags() # Get object's tags
        prefix = "ms" # Prefix for selection tag
        sep = "_" # Separator for selection tag
        msNums = []
        for k in tags: # Loop through tags
            if k.GetName().split("_")[0] == prefix:
                msNums.append(int(k.GetName().split("_")[1]))
        t = c4d.BaseTag(1021338) # Initialize MoGraph Selection tag
        if len(msNums) != 0:
            num = max(msNums) + 1
        else:
            num = 0
        t[c4d.ID_BASELIST_NAME] = prefix+sep+str(num) # Set tag name
        s = c4d.BaseSelect() # Initialize BaseSelect
        for f in finalList: # Loop through list
            s.Select(int(f)) # Select items
        obj.InsertTag(t, obj.GetLastTag()) # Insert tag to object
        doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
        mo.GeSetMoDataSelection(t, s) # Set MoGraph selection

    elif keyMod == "Shift":
        prefix = "ms" # Prefix for selection tag
        sep = "_" # Separator for selection tag
        msNums = []
        for i, f in enumerate(finalList): # Loop through list
            tags = obj.GetTags() # Get object's tags
            #for k in reversed(tags): # Loop through tags
            for k in tags: # Loop through tags
                if k.GetName().split("_")[0] == prefix:
                    msNums.append(int(k.GetName().split("_")[1]))
            t = c4d.BaseTag(1021338) # Initialize MoGraph Selection tag
            if len(msNums) != 0:
                num = max(msNums) + 1
            else:
                num = 0
            t[c4d.ID_BASELIST_NAME] = prefix+sep+str(num) # Set tag name
            s = c4d.BaseSelect() # Initialize BaseSelect
            s.Select(int(f)) # Select items
            obj.InsertTag(t, obj.GetLastTag()) # Insert tag to object

            doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
            mo.GeSetMoDataSelection(t, s) # Set MoGraph selection

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in selection: # Loop through selection
        MoGraphSelectionFromRange(obj, keyMod) # Create MoGraph selection
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()