"""
AR_SelectObject

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectObject
Version: 1.0
Description-US: DEFAULT: Select tag(s) object(s). SHIFT: Keeps the old selection.

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

def Select(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.SetBit(c4d.BIT_ACTIVE) # Select item

def Deselect(op):
    if op != None:
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Record undo for changing bits
        op.DelBit(c4d.BIT_ACTIVE) # Deselect item

def GetObject(op):
    op = op.GetObject() # Get the object
    if op == None: # If object is none
        return pred # Return old object
    else: # Otherwise
        return op # Return the object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    selection = doc.GetSelection() # Get active selection
    keyMod = GetKeyMod() # Get keymodifier

    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag, c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag, c4d.modules.character.CAWeightTag,
    c4d.VariableTag, c4d.modules.graphview.XPressoTag, c4d.VertexColorTag, c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag]
    
    if keyMod == "None":
        for s in selection: # Loop through selection
            if type(s) in commonTags: # If item is a tag
                Select(GetObject(s)) # Select the object
            Deselect(s) # Deselect original item
    elif keyMod == "Shift":
        for s in selection:
            if type(s) in commonTags:
                Select(GetObject(s))

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()