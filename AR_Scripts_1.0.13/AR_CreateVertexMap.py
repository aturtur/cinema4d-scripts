"""
AR_CreateVertexMap

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateVertexMap
Version: 1.0
Description-US: Creates a vertex map tag for selected objects

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d.modules import mograph as mo

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

def MakeEditable(op, doc):
    if (not op): return op # Check if object is already editable
    clone = op.GetClone() # Get clone
    doc.AddUndo(c4d.UNDOTYPE_NEW, clone)
    clone.InsertAfter(op) # Insert clone to document
    #clone.SetMg(op.GetMg()) # Copy global matrix
    bc = c4d.BaseContainer() # Initialize Base Container
    op = c4d.utils.SendModelingCommand(c4d.MCOMMAND_MAKEEDITABLE,
                                          [clone],
                                          c4d.MODELINGCOMMANDMODE_ALL,
                                          bc,
                                          doc,
                                          c4d.MODELINGCOMMANDFLAGS_CREATEUNDO) # Make editable
    #op = c4d.utils.SendModelingCommand(makeEditable, [clone], 0, bc, doc) # Make editable
    if op: return op[0] # Return object
    else: return None # Otherwise return nothing

def CreateVertexMap(op, keyMod):
    wtag = op.MakeVariableTag(c4d.Tvertexmap, op.GetPointCount()) # Initialize weight tag
    doc.AddUndo(c4d.UNDOTYPE_NEW, wtag) # Add undo command for inserting new tag
    if keyMod == "Shift":
        wtag[c4d.ID_TAGFIELD_ENABLE] = 1 # Enable fields
        fieldObject = mo.FieldObject(440000266) # Initialize 'Linear Field'
        fieldList = wtag[c4d.ID_TAGFIELDS] # Get field list
        fieldLayer = mo.FieldLayer(440000251) # Initialize linear field layer
        fieldLayer.SetLinkedObject(fieldObject) # Link field object to field layer
        fieldList.InsertLayer(fieldLayer) # Add layer to field list
        wtag[c4d.ID_TAGFIELDS] = fieldList # Update fields
        fieldObject.InsertUnder(op) # Insert field object under the object
        doc.AddUndo(c4d.UNDOTYPE_NEW, fieldObject) # Add undo command for inserting new object
        fieldObject.SetBit(c4d.BIT_ACTIVE) # Select field object
    doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Add undo command for changing bits
    op.DelBit(c4d.BIT_ACTIVE) # Deselect operator
    wtag.SetBit(c4d.BIT_ACTIVE) # Select tag

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    #try: # Try to execute following script
    keyMod = GetKeyMod() # Get keymodifier
    selection = doc.GetActiveObjects(0) # Get active selection
    for s in selection: # Iterate through selected objects
        if s.GetType() != 5100: # If no polygon object
            e = MakeEditable(s, doc)
            doc.AddUndo(c4d.UNDOTYPE_DELETE, s)
            s.Remove()
            CreateVertexMap(e, keyMod)
        else:
            CreateVertexMap(s, keyMod) # Do the thing

    #except: # If something goes wrong
        #pass # Do nothing

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()