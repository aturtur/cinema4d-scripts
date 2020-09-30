"""
AR_BooleMuch

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_BooleMuch
Version: 1.0
Description-US: Boole many objects at once. First selected is booler. CTRL: Last selected is booler. SHIFT: Create huge cube booler

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Global variables
cube = None

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

def BooleMuch(obj, s, control, boxbox):
    global cube

    if boxbox:
        null = c4d.BaseObject(c4d.Onull) # Initialize a null object
        cube = c4d.BaseObject(c4d.Ocube) # Initialize a cube object
        cubeSize = 10000
        cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_X] = cubeSize
        cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Y] = cubeSize
        cube[c4d.PRIM_CUBE_LEN,c4d.VECTOR_Z] = cubeSize
        cube[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = cubeSize / 2
        null.SetName("Boole Null")
        cube.SetName("Boole Cube")
        doc.AddUndo(c4d.UNDOTYPE_NEW, cube)
        cube.InsertUnder(null)
        doc.AddUndo(c4d.UNDOTYPE_NEW, null)
        doc.InsertObject(null)
        null[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
        null[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

        null.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager

    if obj == None:
        obj = cube

    boole = c4d.BaseObject(1010865) # Initialize a boole object
    boole.SetName("Boole "+s.GetName()) # Set boole's name
    instance = c4d.BaseObject(5126) # Initialize a instance object
    instance.SetName(obj.GetName()+"_Instance") # Set instance's name
    instance[c4d.INSTANCEOBJECT_LINK] = obj # Set instance link

    if control:
        constraintTag = c4d.BaseTag(1019364) # Initialize a constraint tag
        constraintTag[c4d.ID_CA_CONSTRAINT_TAG_PSR] = True # PSR
        constraintTag[10001] = obj # Target
        constraintTag[10005] = True # Position
        constraintTag[10006] = True # Scale
        constraintTag[10007] = True # Rotation
        instance.InsertTag(constraintTag) # Insert tag to instance object
    else:
        instance.SetMg(obj.GetMg()) # Set instance object's matrix

    doc.AddUndo(c4d.UNDOTYPE_NEW, boole)
    boole.InsertBefore(s)

    if cube == None:
        boole.SetBit(c4d.BIT_ACTIVE)

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, instance)
    instance.InsertUnder(boole)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
    s.InsertUnder(boole)
    
# Main function
def main():
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if len(selection) is None: return
    boxbox = True
    for i, s in enumerate(selection): # Loop through selected objects
        first = selection[0] # Get first selected object
        last = selection[-1] # Get last selected object

        if keyMod == "None":
            if s != first:
                BooleMuch(first, s, True, False)

        elif keyMod == "Ctrl":
            if s != last:
                BooleMuch(last, s, True, False)

        elif keyMod == "Shift":
            BooleMuch(None, s, True, boxbox)
            boxbox = False

        doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
        s.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()
