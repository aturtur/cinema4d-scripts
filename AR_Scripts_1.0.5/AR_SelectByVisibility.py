"""
AR_SelectByVisibility

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: SelectByVisibility
Version: 1.0
Description-US: Selects objects by visibility
Default: Select objects that are visible in editor.
Shift: Select objects that are visible in render.
Alt: Select objects that are invisible in editor.
Alt+Shift: Select objects that are invisible in render.
Ctrl: Deselect objects that are visible in editor.
Alt+Ctrl: Deselect objects that are invisible in editor.
Ctrl+Shift: Deselect objects that are visible in render.
Alt+Strl+Shift: Deselect objects that are invisible in render.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d import utils as u

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

def GetNextObject(op):
    """
    Returns the next op.

    Args:
        op: (todo): write your description
    """
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def Select(lst):
    """
    Set all bitmap of a bitmap.

    Args:
        lst: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    for l in lst: # Iterate through objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo
        l.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(lst):
    """
    Deselect bit bitmap.

    Args:
        lst: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    for l in lst: # Iterate through objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo
        l.DelBit(c4d.BIT_ACTIVE) # Deselect object

def CollectByVisibility(op, keyMod):
    """
    Given a list of tuples of ( dese ). dese. dese operation ).

    Args:
        op: (todo): write your description
        keyMod: (str): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selectionList = []
    deselectionList = []
    if op is None:
        return
    while op:
        # Select
        if keyMod == "None": # Default: Select visible in editor: On
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 0: # On
                selectionList.append(op) # Add object to the selection list
        elif keyMod == "Shift": # Shift: Select visible in render: On
            if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 0: # On
                selectionList.append(op) # Add object to the selection list
        elif keyMod == "Alt": # Alt: Select visible in editor: Off
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 1: # Off
                selectionList.append(op) # Add object to the selection list
        elif keyMod == "Alt+Shift": # Alt+Shift: Select visible in render: Off
            if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1: # Off
                selectionList.append(op) # Add object to the selection list

        # Deselect
        elif keyMod == "Ctrl": # Ctrl: Deselect visible in editor: On
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 0: # On
                deselectionList.append(op) # Add object to deselction list
        elif keyMod == "Alt+Ctrl": # Alt+Ctrl: Deselect visible in editor: Off
            if op[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] == 1: # Off
                deselectionList.append(op) # Add object to deselction list
        elif keyMod == "Ctrl+Shift": # Ctrl+Shift: Deselect visible in render: On
            if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 0: # On
                deselectionList.append(op) # Add object to deselction list
        elif keyMod == "Alt+Ctrl+Shift": # Alt+Ctrl+Shift: Deselect visible in render: Off
            if op[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] == 1: # Off
                deselectionList.append(op) # Add object to deselction list
        op = GetNextObject(op) # Get next object

    return selectionList, deselectionList

def main():
    """
    The main function.

    Args:
    """
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    #try: # Try to execute following script
    #selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active objects
    start_object = doc.GetFirstObject() # Get first object
    selectionList, deselectionList = CollectByVisibility(start_object, keyMod) # Do the thing
    Select(selectionList) # Select objects
    Deselect(deselectionList) # Deselect objects
    #except: # If something went wrong
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__ == "__main__":
    main()