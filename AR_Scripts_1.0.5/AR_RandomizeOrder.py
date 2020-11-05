"""
AR_RandomizeOrder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RandomizeOrder
Version: 1.0
Description-US: Randomize order of selected objects in Object Manager. Objects have to be in same level in the hierarchy!

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

To do:
    - Make it better

"""
# Libraries
import c4d
import random

# Functions
def GetKeyMod():
    """
    Retrieves the key from the key.

    Args:
    """
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

def main():
    """
    Main function.

    Args:
    """
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    #try: # Try to execute following script
    
    selection = doc.GetActiveObjects(0) # Get selected objects
    
    pO = c4d.BaseObject(c4d.Onull) # Initialize temp null
    if selection[0].GetPred() is not None: # If there is previous object
        insertPos = selection[0].GetPred() # Set insertion position to start from previous object
        insertMode = 1 # Set insert mode to 1
    elif selection[0].GetUp() is not None: # If there is no parent object
        insertPos = selection[0].GetUp() # Set insertion position to start from parent object
        insertMode = 2 # Set insert mode to 2
    else: # If there is no previous or parent object
        insertPos = selection[0] # Set insertion position to start from first object
        insertMode = 3 # Set insert mode to 3
    position = selection[0].GetPred()

    if keyMod == "None": # Random order
        random.shuffle(selection) # Randomize selected objects list
        for s in selection: # Loop through selected objects
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
            if insertMode == 1: # If insert mode is 1
                s.InsertAfter(insertPos) # Move object next to insert position
            elif insertMode == 2: # If insert mode is 2
                s.InsertUnder(insertPos) # Move object next to insert position
            else: # If insert mode is 3
                doc.InsertObject(pO) # Insert temp null to document
                s.InsertAfter(doc.GetFirstObject()) # Move object to first
                pO.Remove() # Remove temp null

    elif keyMod == "Shift": # A-Z order
        lst = [] # Initialize a list
        for s in selection: # Loop through selected objects
            lst.append([s.GetName(), s]) # Add to list
        sortedSelection = sorted(lst, key=lambda x: x[0], reverse=True) # Sort the list
        for s in sortedSelection:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s[1])
            if insertMode == 1: # If insert mode is 1
                s[1].InsertAfter(insertPos) # Move object next to insert position
            elif insertMode == 2: # If insert mode is 2
                s[1].InsertUnder(insertPos) # Move object next to insert position
            else: # If insert mode is 3
                doc.InsertObject(pO) # Insert temp null to document
                s[1].InsertAfter(doc.GetFirstObject()) # Move object to first
                pO.Remove() # Remove temp null

    elif keyMod == "Ctrl": # Z-A order
        lst = [] # Initialize a list
        for s in selection: # Loop through selected objects
            lst.append([s.GetName(), s]) # Add to list
        sortedSelection = sorted(lst, key=lambda x: x[0], reverse=False) # Sort the list
        for s in sortedSelection:
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s[1])
            if insertMode == 1: # If insert mode is 1
                s[1].InsertAfter(insertPos) # Move object next to insert position
            elif insertMode == 2: # If insert mode is 2
                s[1].InsertUnder(insertPos) # Move object next to insert position
            else: # If insert mode is 3
                doc.InsertObject(pO) # Insert temp null to document
                s[1].InsertAfter(doc.GetFirstObject()) # Move object to first
                pO.Remove() # Remove temp null


    #except: # If something went wrong
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D


# Execute main()
if __name__=='__main__':
    main()