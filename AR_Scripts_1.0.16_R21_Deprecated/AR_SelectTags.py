"""
AR_SelectTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectTags
Version: 1.0
Description-US: Select object(s) tag(s)

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

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def IterateHierarchy(tagTypes, op):
    collectedTags = []
    if op is None:
        return
    while op:
        for tagType in tagTypes:
            foundTags = SearchTags(tagType, op)
            collectedTags = collectedTags + foundTags
        op = GetNextObject(op) # Get next object
    return collectedTags

def Select(lst):
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.SetBit(c4d.BIT_ACTIVE) # Select object

def Deselect(lst):
    if len(lst) > 0: # If list is not empty
        for l in lst:
            doc.AddUndo(c4d.UNDOTYPE_BITS, l) # Record undo for changing bits
            l.DelBit(c4d.BIT_ACTIVE) # Deselect object

def GetTags(op):
    op = op.GetTags() # Get tags
    if op == None: # If object is none
        return pred # Return old object
    else: # Otherwise
        return op # Return the object

def SearchTags(tagType, op):
    collectedTags = []
    tags = op.GetTags()
    for t in tags:
        if t.GetType() == tagType:
            collectedTags.append(t)
    return collectedTags

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag,
                  c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag,
                  c4d.modules.character.CAWeightTag, c4d.VariableTag,
                  c4d.modules.graphview.XPressoTag, c4d.VertexColorTag,
                  c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags

    collectedTagTypes = [] # Init an array for tag types

    selection = doc.GetSelection() # Get selection (includes objs, mats, tags...)
    for t in selection: # Iterate through selection
        if type(t) in commonTags: # If selected item is a tag
            collectedTagTypes.append(t.GetType()) # Add tag type to the list

    selectedObjs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
    keyMod = GetKeyMod() # Get keymodifier


    if len(collectedTagTypes) == 0: # If no tags selection
        if keyMod == "None":
            for s in selectedObjs: # Loop through selection
                Select(GetTags(s)) # Select the object
                Deselect([s]) # Deselect original item
        elif keyMod == "Shift":
            for s in selectedObjs:
                Select(GetTags(s))
    else:
        if len(selectedObjs) == 0: # If no selected objects
            tags = IterateHierarchy(collectedTagTypes, doc.GetFirstObject()) # Iterate through all objects in the document
            Select(tags)
        else:
            for o in selectedObjs:
                for tagType in collectedTagTypes:
                    tags = SearchTags(tagType, o)
                    Select(tags)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()