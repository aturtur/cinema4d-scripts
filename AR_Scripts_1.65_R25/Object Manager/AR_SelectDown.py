"""
AR_SelectDown

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectDown
Version: 1.0.1
Description-US: Default: Goes down one hierarchy level. Shift: Add to old selection.

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
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
        
        parent = op.GetUp() # Get parent
        if parent.GetNBit(c4d.NBIT_OM1_FOLD) == 0: # If object is folded
            parent.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE) # Unfold

def Deselect(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetDown(op, safe):
    pred = op # Store old object
    op = op.GetDown() # Get child object
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

    if keyMod == "None":
        for s in selection: # Loop through selection
            Deselect(s) # Deselect original object
            Select(GetDown(s, True)) # Select child object
    elif keyMod == "Shift":
        for s in selection:
            Select(GetDown(s, True))
    elif keyMod == "Ctrl":
        for s in selection:
            Deselect(s) # Deselect original object
            Select(GetDown(s, False))
    elif keyMod == "Ctrl+Shift":
        for s in selection:
            Select(GetDown(s, False))


    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()