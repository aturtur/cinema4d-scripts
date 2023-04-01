"""
AR_ObjectReplace

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ObjectReplace
Version: 1.0.1
Description-US: Replace objects with instance/copies of the first/last selected object.

Default:    Replace objects with instances of the first selected object
Shift:      Replace objects with instances of the last selected object
Ctrl:       Replace objects with copies of the first selected object
Ctrl+Shift: Replace objects with copies of the last selected object

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (28.03.2022) - Updated to R25
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

def deleteWithoutChildren(s):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    children = s.GetChildren() # Get selected object's children
    for child in reversed(children): # Loop through children
        globalMatrix = child.GetMg() # Get current global matrix
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child) # Add undo command for moving item
        child.InsertAfter(s) # Move child
        child.SetMg(globalMatrix) # Set old global matrix
    doc.AddUndo(c4d.UNDOTYPE_DELETE, s) # Add undo command for deleting selected object
    s.Remove() # Remove selected object

def replaceObjects(keyMod, inherit = False):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get selection
    objList = [] # Initialize list for objects
    childrenList = [] # Initialize list for list of children

    # Create instance objects and place those
    for i, s in enumerate(selection): # Loop through selected objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
        s.DelBit(c4d.BIT_ACTIVE) # Deselect first selected object
        if keyMod == "None": # Replace with instance of the first selected
            if i != 0: # If not first loop round
                childrenList.append(selection[i].GetChildren()) # Get children objects
                instObj = c4d.BaseObject(5126) # Initialize intance object
                instObj[c4d.INSTANCEOBJECT_LINK] = selection[0] # Link first selected object to instance
                instObj[c4d.ID_BASELIST_NAME] = selection[0].GetName()+"_Instance_"+str(i) # Change name
                instObj.InsertUnder(s) # Put instance under the selected object
                doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
                s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                doc.AddUndo(c4d.UNDOTYPE_NEW, instObj) # Add undo command for inserting a new object
                objList.append(instObj) # Add current instance to list
        elif keyMod == "Shift": # Replace with instance of the last selected
            if i != (len(selection)-1): # If not last selected element
                childrenList.append(selection[i].GetChildren()) # Get children objects
                instObj = c4d.BaseObject(5126) # Initialize intance object
                instObj[c4d.INSTANCEOBJECT_LINK] = selection[-1] # Link first selected object to instance
                instObj[c4d.ID_BASELIST_NAME] = selection[-1].GetName()+"_Instance_"+str(i) # Change name
                instObj.InsertUnder(s) # Put instance under the selected object
                doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
                s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                doc.AddUndo(c4d.UNDOTYPE_NEW, instObj) # Add undo command for inserting a new object
                objList.append(instObj) # Add current instance to list
        elif keyMod == "Ctrl": # Replace with copy of the first selected
            if i != 0: # If not first loop round
                childrenList.append(selection[i].GetChildren()) # Get children objects
                copyObj = selection[0].GetClone() # Get clone object
                copyObj[c4d.ID_BASELIST_NAME] = selection[0].GetName()+"_Copy_"+str(i) # Change name
                copyObj.InsertUnder(s) # Put instance under the selected object
                doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
                s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                doc.AddUndo(c4d.UNDOTYPE_NEW, copyObj) # Add undo command for inserting a new object
                objList.append(copyObj) # Add current instance to list
        elif keyMod == "Ctrl+Shift": # Replace with copy of the last selected
            if i != (len(selection)-1): # If not last selected element
                childrenList.append(selection[i].GetChildren()) # Get children objects
                copyObj = selection[-1].GetClone() # Get clone object
                copyObj[c4d.ID_BASELIST_NAME] = selection[-1].GetName()+"_Copy_"+str(i) # Change name
                copyObj.InsertUnder(s) # Put instance under the selected object
                doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
                s.DelBit(c4d.BIT_ACTIVE) # Deselect object
                doc.AddUndo(c4d.UNDOTYPE_NEW, copyObj) # Add undo command for inserting a new object
                objList.append(copyObj) # Add current instance to list


    # Reset PSR and remove original object
    for i, s in enumerate(objList): # Loop through instances
        doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
        s.SetBit(c4d.BIT_ACTIVE) # Select object
        # Reset position
        s[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 0
        s[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = 0
        s[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = 0
        # Reset scale
        s[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_X] = 1
        s[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_Y] = 1
        s[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_Z] = 1
        # Reset rotation
        s[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = 0
        s[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = 0
        s[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z] = 0
        deleteWithoutChildren(s.GetUp()) # Delete Without Children
        # Move old children (inherit)
        if inherit == True:
            for child in childrenList[i]:
                childMg = child.GetMg()
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
                child.InsertUnderLast(s)
                child.SetMg(childMg)
    # Select objects again
    doc.AddUndo(c4d.UNDOTYPE_BITS, selection[-1]) # Add undo command for changing bits
    selection[-1].SetBit(c4d.BIT_ACTIVE) # Select first object
    for i in objList: # Loop through instances
            doc.AddUndo(c4d.UNDOTYPE_BITS, i) # Add undo command for changing bits
            i.SetBit(c4d.BIT_ACTIVE) # Select object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() #Get selection
    keyMod = GetKeyMod()
    replaceObjects(keyMod, True) # Run the script
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()