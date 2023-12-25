"""
AR_RemoveMissingTextureTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveMissingTextureTags
Version: 1.0.2
Description-US: Removes texture tags that does not have assigned material. SHIFT: Remove texture tags with missing selection tags.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.2 (18.08.2022) - Support for R25

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
 
def RemoveMissingTextureTags(op, selection):
    if op is None:
        return
    while op:
        tags = op.GetTags() # Get tags of object
        if selection == True:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                for t in tags: # Loop Through tags
                    if t.GetType() == 5616: # If tag is texture tag
                        if t[c4d.TEXTURETAG_MATERIAL] == None: # If tag doesn't have material
                            doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                            t.Remove() # Remove tag
        else:
            for t in tags: # Loop Through tags
                if t.GetType() == 5616: # If tag is texture tag
                    if t[c4d.TEXTURETAG_MATERIAL] == None: # If tag doesn't have material
                        doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                        t.Remove() # Remove tag
        op = GetNextObject(op)
    return True

def RemoveTagsWithMissingSelection(op, selection):
    if op is None:
        return
    while op:
        materialTags = [] # Init an array
        selectionTags = [] # Init an array
        tags = op.GetTags() # Get object's tags
        
        for t in tags: # Collect tags
            if t.GetType() == 5616: # If material tag
                materialTags.append(t)
            if t.GetType() == 5673: # Polygon selection tag
                selectionTags.append(t.GetName())
        
        if selection == True:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                for m in materialTags: # Iterate through material tags
                    restriction = m[c4d.TEXTURETAG_RESTRICTION] # Get polygon restriction
                    if restriction not in selectionTags: # If not found in polygon selection tags
                        if restriction != "":
                            doc.AddUndo(c4d.UNDO_DELETE, m)
                            m.Remove() # Remove tag
        else:
            for m in materialTags: # Iterate through material tags
                restriction = m[c4d.TEXTURETAG_RESTRICTION] # Get polygon restriction
                if restriction not in selectionTags: # If not found in polygon selection tags
                    if restriction != "":
                        doc.AddUndo(c4d.UNDO_DELETE, m)
                        m.Remove() # Remove tag
        
        op = GetNextObject(op)
    return True

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
    keyMod = GetKeyMod() # Get keymodifier
    try: # Try to execute following script
        start_object = doc.GetFirstObject() # Get first object
        if keyMod == "None":
            if len(selection) != 0:
                RemoveMissingTextureTags(start_object, True) # Do the thing
            else:
                RemoveMissingTextureTags(start_object, False) # Do the thing
        elif keyMod == "Shift":
            if len(selection) != 0:
                RemoveTagsWithMissingSelection(start_object, True) # Do the other thing
            else:
                RemoveTagsWithMissingSelection(start_object, False) # Do the other thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
  
# Execute main()
if __name__=='__main__':
    main()