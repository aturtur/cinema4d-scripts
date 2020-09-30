"""
AR_SelectSourceObject

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectSourceObject
Version: 1.0
Description-US: Selects the source object. Supports Instance, Connect, MoInstance, MoSpline, Cloner and Matrix objects

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
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

def Select(obj, source, doc, keyMod):
    doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
    if keyMod == "None":
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect original object
        doc.AddUndo(c4d.UNDOTYPE_BITS, source) # Add undo command for changing bits
        source.SetBit(c4d.BIT_ACTIVE) # Select object
        c4d.CallCommand(100004769) # Scroll to First Active
    elif keyMod == "Shift":
        source.SetBit(c4d.BIT_ACTIVE) # Select object
        c4d.CallCommand(100004769) # Scroll to First Active

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    keyMod = GetKeyMod() # Get keymodifier
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get active selection
    for x in selection: # Loop through selection
        try: # Try to execute following script
            if x.GetType() == 5126: # Instance Object
                source = x[c4d.INSTANCEOBJECT_LINK]
                Select(x, source, doc, keyMod)
            if x.GetType() == 1011010: # Connect Object
                source = x[c4d.CONNECTOBJECT_LINK]
                Select(x, source, doc, keyMod)
            if x.GetType() == 1018957: # MoInstance Object
                source = x[c4d.MGINSTANCER_LINK]
                Select(x, source, doc, keyMod)
            if x.GetType() == 1018544: # Cloner Object
                if x[c4d.ID_MG_MOTIONGENERATOR_MODE] == 0: # Object Mode
                    source = x[c4d.MG_OBJECT_LINK]
                    Select(x, source, doc, keyMod)
            if x.GetType() == 1018545: # Matrix Object
                if x[c4d.ID_MG_MOTIONGENERATOR_MODE] == 0: # Object Mode
                    source = x[c4d.MG_OBJECT_LINK]
                    Select(x, source, doc, keyMod)
            if x.GetType() == 440000054: #MoSpline Object
                if x[c4d.MGMOSPLINEOBJECT_MODE] == 1: #Spline
                    source = x[c4d.MGMOSPLINEOBJECT_SOURCE_SPLINE]
                    Select(x, source, doc, keyMod)
        except: # If something went wrong
            pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()