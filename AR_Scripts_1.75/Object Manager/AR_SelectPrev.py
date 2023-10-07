"""
AR_SelectPrev

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectPrev
Version: 1.0.3
Description-US: Default: Selects previous object. Shift: Keeps the old selection

Written for Maxon Cinema 4D 2023.1.0
Python version 3.9.1

Change log:
1.0.3 (10.09.2023) - Bug fix
1.0.2 (18.11.2022) - Hotkey fix
1.0.1 (20.01.2022) - R25 update
"""

# Libraries
import c4d

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

def Select(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetPrev(op, safe):
    pred = op # Store old object
    op = op.GetPred() # Get previous object
    if op == None: # If object is none
        if safe: # If safe mode is enabled
            return pred # Return old object
        return None # Return none
    else: # Otherwise
        return op # Return the object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active objects
    keyMod = GetKeyMod() # Get keymodifier

    if (keyMod == "None") or (keyMod == "Alt"):
        for s in selection: # Loop through selection
            Deselect(s) # Deselect original object
            Select(GetPrev(s, True)) # Select previous object
    elif (keyMod == "Shift") or (keyMod == "Alt+Shift"):
        for s in selection:
            Select(GetPrev(s, True))
    elif (keyMod == "Ctrl") or (keyMod == "Alt+Ctrl"):
        for s in selection:
            Deselect(s) # Deselect original object
            Select(GetPrev(s, False))
    elif (keyMod == "Ctrl+Shift") or (kayMod == "Alt+Ctrl+Shift"):
        for s in selection:
            Select(GetPrev(s, False))

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()