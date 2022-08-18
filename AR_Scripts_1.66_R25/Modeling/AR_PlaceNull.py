"""
AR_PlaceNull

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PlaceNull
Version: 1.0.0
Description-US: Creates null to current axis matrix

Default: Selects the null and deselects the previous objects
Shift: No selection change

Written for Maxon Cinema 4D R25.010
Python version 3.9.1
"""

# Libraries
import c4d
from c4d.modules import snap

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

def main():
    keyMod = GetKeyMod() # Get key modifier
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(1) # Get selected objects    
    c4d.CallCommand(431000012) # Axis Workplane
    mat = snap.GetWorkplaneMatrix(doc, doc.GetBaseDraw(0)) # Get workplanes' matrix
    null = c4d.BaseObject(c4d.Onull) # Initialize a null object
    null.SetMg(mat) # Set matrix
    c4d.CallCommand(431000007) # Align Workplane to Y
    doc.InsertObject(null) # Insert object to document
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Record undo for inserting new object

    if keyMod == "None": # Default action
        null.SetBit(c4d.BIT_ACTIVE) # Select the null
        if len(selection) != 0: # If there are any objects
            for s in selection: # Iterate through objects
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Record undo for deselecting object
                s.DelBit(c4d.BIT_ACTIVE) # Deselect object

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()