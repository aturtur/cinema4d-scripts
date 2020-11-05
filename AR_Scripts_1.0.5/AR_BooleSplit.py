"""
AR_BooleSplit

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_BooleSplit
Version: 1.0
Description-US: Creates a boole setup from two selected objects that creates a piece effect. SHIFT: Uses instances

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

def BooleSplit(a, b, instance):
    """
    Perform an instance of python 3.

    Args:
        a: (todo): write your description
        b: (todo): write your description
        instance: (todo): write your description
    """
    booleA = c4d.BaseObject(1010865)
    booleA.SetName("Boole Subtract")

    booleB = c4d.BaseObject(1010865)
    booleB.SetName("Boole Intersect")
    booleA[c4d.BOOLEOBJECT_TYPE] = 1
    booleB[c4d.BOOLEOBJECT_TYPE] = 2

    doc.AddUndo(c4d.UNDOTYPE_NEW, booleB)
    booleB.InsertBefore(a)
    doc.AddUndo(c4d.UNDOTYPE_NEW, booleA)
    booleA.InsertBefore(booleB)

    if instance == True:
        null = c4d.BaseObject(c4d.Onull)
        null[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
        null[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

        doc.AddUndo(c4d.UNDOTYPE_NEW, null)
        null.InsertBefore(a)
        
        instanceA = c4d.BaseObject(5126)
        instanceA.SetName(a.GetName()+"_Instance")
        instanceB = c4d.BaseObject(5126)
        instanceB.SetName(b.GetName()+"_Instance")
        instanceA[c4d.INSTANCEOBJECT_LINK] = a
        instanceB[c4d.INSTANCEOBJECT_LINK] = b
        instanceA.SetMg(a.GetMg())
        instanceB.SetMg(b.GetMg())
        instanceC = instanceA.GetClone()
        instanceD = instanceB.GetClone()
        instanceA[c4d.INSTANCEOBJECT_LINK] = a
        instanceB[c4d.INSTANCEOBJECT_LINK] = b
        instanceA.InsertUnder(booleA)
        instanceB.InsertUnder(booleA)
        instanceC.InsertUnder(booleB)
        instanceD.InsertUnder(booleB)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, a)
        a.InsertUnder(null)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, b)
        b.InsertUnder(null)

    else:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, a)
        a.InsertUnder(booleA)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, b)
        b.InsertUnder(booleA)
        c = a.GetClone()
        d = b.GetClone()
        doc.AddUndo(c4d.UNDOTYPE_NEW, c)
        c.InsertUnder(booleB)
        doc.AddUndo(c4d.UNDOTYPE_NEW, d)
        d.InsertUnder(booleB)

    doc.AddUndo(c4d.UNDOTYPE_BITS, a)
    a.DelBit(c4d.BIT_ACTIVE)
    doc.AddUndo(c4d.UNDOTYPE_BITS, b)
    b.DelBit(c4d.BIT_ACTIVE)
    booleB.SetBit(c4d.BIT_ACTIVE)

# Main function
def main():
    """
    Main entry point.

    Args:
    """
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if len(selection) is None: return
    #for i, s in enumerate(selection): # Loop through selected objects
    first = selection[0] # Get first selected object
    last = selection[1] # Get last selected object

    if keyMod == "None":
        BooleSplit(last, first, False)
    elif keyMod == "Shift":
        BooleSplit(last, first, True)

    #doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
    #s.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()
