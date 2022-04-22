"""
AR_MoSelection

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoSelection
Version: 1.0.0
Description-US: Create MoGraph selection for every clone. Shift: Shared tag for given IDs. Ctrl: Individual tags for given IDs

Written for Maxon Cinema 4D R25.010
Python version 3.9.1
"""

# Libraries
import c4d
from c4d.modules import mograph as mo
from c4d import gui as g

# Global variables
prefix = "MG" 
sep    = "_"

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

def CheckMoGraphSelectionTags(obj):
    global prefix
    global sep

    msNums = [] # Initialize a list
    tags = obj.GetTags() # Get object's tags
    for tag in tags: # Loop through tags
        if tag.GetName().split(sep)[0] == prefix:
            msNums.append(int(tag.GetName().split(sep)[1]))
    if len(msNums) != 0:
        return max(msNums) + 1
    else: # If no any old MoGraph selection tags found with custom prefix
        return 0

def MoGraphSelectionForEveryClone(obj):
    global prefix
    global sep

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    try: # Try to execute following
        md = mo.GeGetMoData(obj) # Get MoGraph data
        cnt = md.GetCount() # Get clone count
        for i in range(0, cnt): # Loop through clones
            tag = c4d.BaseTag(1021338) # Initialize MoGraph selection tag
            tag[c4d.ID_BASELIST_NAME] = prefix+sep+str(i)
            s = c4d.BaseSelect() # Initialize BaseSelect
            obj.InsertTag(tag, obj.GetLastTag()) # Insert tag to object
            doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Add undo command for inserting tag
            s.Select(i) # Select clone
            mo.GeSetMoDataSelection(tag, s) # Set selection to tag
    except: # If something went wrong
        pass # Do nothing

def MoGraphSelectionFromRange(obj, keyMod):
    global prefix
    global sep

    userInput = g.InputDialog("Selected IDs for "+obj.GetName(),"") # User input dialog
    if userInput == "": return
    baseList = userInput.split(",") # Split user input to list
    add = [] # Initialize empty list
    finalList = []  # Initialize empty list
    for x in baseList: # Loop through list items
        rng = x.split("-") # Split range value (e.g. 5-15)
        if len(rng) > 1:
            for i in range(int(rng[0]),int(rng[1])+1):
                add.append(i)
    fullList = baseList + add
    for f in fullList:
        if type(f) == int:
            finalList.append(f)
        if type(f) != int:
            if f.find("-") == -1:
                finalList.append(f)

    if keyMod == "Shift":
        num = CheckMoGraphSelectionTags(obj) # Check MG number
        t = c4d.BaseTag(1021338) # Initialize MoGraph Selection tag
        t[c4d.ID_BASELIST_NAME] = prefix+sep+str(num) # Set tag name
        s = c4d.BaseSelect() # Initialize BaseSelect
        for f in finalList: # Loop through list
            s.Select(int(f)) # Select items
        obj.InsertTag(t, obj.GetLastTag()) # Insert tag to object
        doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
        mo.GeSetMoDataSelection(t, s) # Set MoGraph selection

    elif keyMod == "Ctrl":
        for i, f in enumerate(finalList): # Loop through list
            num = CheckMoGraphSelectionTags(obj) # Check MG number
            t = c4d.BaseTag(1021338) # Initialize MoGraph Selection tag
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

    if keyMod == "None":
        for obj in selection: # Loop through selection
            MoGraphSelectionForEveryClone(obj) # Create MoGraph selection for every clone
    if keyMod == "Shift" or keyMod == "Ctrl":
        for obj in selection: # Loop through selection
            MoGraphSelectionFromRange(obj, keyMod) # Create MoGraph selection
            
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()