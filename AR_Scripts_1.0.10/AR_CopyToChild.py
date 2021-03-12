"""
AR_CopyToChild

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CopyToChild
Version: 1.0
Description-US: Creates a copy from first/last selected object to the rest of the selected objects

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

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

    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get selection

        if keyMod == "None":
            doc.AddUndo(c4d.UNDOTYPE_BITS, selection[0]) # Record undo
            selection[0].DelBit(c4d.BIT_ACTIVE) # Deselect object
            for i, s in enumerate(selection): # Loop through selected objects
                if i != 0: # If not first loop round
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Record undo
                    s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                    clone = selection[0].GetClone() # Clone first object
                    clone.InsertUnder(s) # Insert clone under the object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, clone) # Add undo command for inserting a new object
                    clone.SetBit(c4d.BIT_ACTIVE) # Select clone
        elif keyMod == "Shift":
            doc.AddUndo(c4d.UNDOTYPE_BITS, selection[-1]) # Record undo
            selection[-1].DelBit(c4d.BIT_ACTIVE) # Deselect object
            for i, s in enumerate(selection): # Loop through selected objects
                if i != len(selection)-1: # If not last loop round
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Record undo
                    s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                    clone = selection[-1].GetClone() # Clone last object
                    clone.InsertUnder(s) # Insert clone under the object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, clone) # Add undo command for inserting a new object
                    clone.SetBit(c4d.BIT_ACTIVE) # Select clone
        elif keyMod == "Ctrl":
            doc.AddUndo(c4d.UNDOTYPE_BITS, selection[0]) # Record undo
            selection[0].DelBit(c4d.BIT_ACTIVE) # Deselect object
            for i, s in enumerate(selection): # Loop through selected objects
                if i != 0: # If not first loop round
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Record undo
                    s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                    instance = c4d.BaseObject(c4d.Oinstance) # Initialize an instance object
                    instance.SetName(selection[0].GetName() + " Instance")
                    instance[c4d.INSTANCEOBJECT_LINK] = selection[0] # Set reference object
                    instance.InsertUnder(s) # Insert instance under the object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, instance) # Add undo command for inserting a new object
                    instance.SetBit(c4d.BIT_ACTIVE) # Select instance
        elif keyMod == "Ctrl+Shift":
            doc.AddUndo(c4d.UNDOTYPE_BITS, selection[-1]) # Record undo
            selection[-1].DelBit(c4d.BIT_ACTIVE) # Deselect object
            for i, s in enumerate(selection): # Loop through selected objects
                if i != len(selection)-1: # If not last loop round
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Record undo
                    s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                    instance = c4d.BaseObject(c4d.Oinstance) # Initialize an instance object
                    instance.SetName(selection[0].GetName() + " Instance")
                    instance[c4d.INSTANCEOBJECT_LINK] = selection[0] # Set reference object
                    instance.InsertUnder(s) # Insert instance under the object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, instance) # Add undo command for inserting a new object
                    instance.SetBit(c4d.BIT_ACTIVE) # Select instance

    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()
