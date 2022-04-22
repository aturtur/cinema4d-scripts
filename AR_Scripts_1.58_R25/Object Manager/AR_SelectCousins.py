"""
AR_SelectCousins

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectCousins
Version: 1.0
Description-US: DEFAULT: Selects the object's Cousins. CTRL: Deselect original selection.

Written for Maxon Cinema 4D R25.010
Python version 3.9.1
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

def Select(lst):
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(lst):
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetCousins(op):
    pred = op # Store old object
    op = op.GetUp().GetUp() # Get parent object
    if op == None: # If object is none
            return [pred] # Return old object
    else: # Otherwise
        parents = op.GetChildren() # Get children
        children = []
        for p in parents:
            children = children + p.GetChildren()
        return children # Return the object(s)

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active objects
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "None":
        for s in selection: # Loop through selection
            Select(GetCousins(s)) # Select parent object
    elif keyMod == "Ctrl":
        for s in selection:
            Select(GetCousins(s))
        for s in selection:
            Deselect([s]) # Deselect original object


    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()