"""
AR_SelectTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectTags
Version: 1.0
Description-US: DEFAULT: Select object(s) tag(s). SHIFT: Keeps the old selection.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

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

def Select(lst):
    """
    Set all bitmap.

    Args:
        lst: (todo): write your description
    """
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(lst):
    """
    Deselect bitstrings.

    Args:
        lst: (todo): write your description
    """
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetTags(op):
    """
    Returns the next operator for the given op.

    Args:
        op: (todo): write your description
    """
    op = op.GetTags() # Get tags
    if op == None: # If object is none
        return pred # Return old object
    else: # Otherwise
        return op # Return the object

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "None":
        for s in selection: # Loop through selection
            Select(GetTags(s)) # Select the object
            Deselect([s]) # Deselect original item
    elif keyMod == "Shift":
        for s in selection:
            Select(GetTags(s))

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()