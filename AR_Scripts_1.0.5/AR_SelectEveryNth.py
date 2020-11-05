"""
AR_SelectEveryNth

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectEveryNth
Version: 1.0
Description-US: Selects every odd/even/nth object

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

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo() # Start recording undos
    
    keyMod = GetKeyMod()
    selection = doc.GetSelection()
    
    if (keyMod == "Ctrl") or (keyMod == "Alt"):
        nth = int(c4d.gui.InputDialog("Nth", 3))
    
    if len(selection) != 0:
        for i, s in enumerate(selection):
            
            if keyMod == "None":
                if i % 2 == 1: # Odd
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s)
                    s.DelBit(c4d.BIT_ACTIVE)
            if keyMod == "Shift":
                if i % 2 == 0: # Even
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s)
                    s.DelBit(c4d.BIT_ACTIVE)
            if keyMod == "Ctrl":
                if i % nth != 0: # Nth
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s)
                    s.DelBit(c4d.BIT_ACTIVE)
            if keyMod == "Alt":
                if i % nth == 0: # Nth
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s)
                    s.DelBit(c4d.BIT_ACTIVE)
    else:
        first = doc.GetFirstObject()
        current = first
        i = 0
        while current != None:
            if keyMod == "None":
                if i % 2 == 0: # Odd
                    doc.AddUndo(c4d.UNDOTYPE_BITS, current)
                    current.SetBit(c4d.BIT_ACTIVE)
            if keyMod == "Shift":
                if i % 2 == 1: # Even
                    doc.AddUndo(c4d.UNDOTYPE_BITS, current)
                    current.SetBit(c4d.BIT_ACTIVE)
            if keyMod == "Ctrl":
                if i % nth == 0: # Nth
                    doc.AddUndo(c4d.UNDOTYPE_BITS, current)
                    current.SetBit(c4d.BIT_ACTIVE)
            if keyMod == "Alt":
                if i % nth != 0: # Nth
                    doc.AddUndo(c4d.UNDOTYPE_BITS, current)
                    current.SetBit(c4d.BIT_ACTIVE)
            current = current.GetNext()
            i = i+1
            
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()