"""
AR_CameraFocusToNull

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CameraFocusToNull
Version: 1.0.0
Description-US: Creates Focus Distance object for selected camera(s). SHIFT: Assigns also target tag to camera

Written for Maxon Cinema 4D 2023.2.0
Python version 3.10.8

Change log:
1.0.0 (25.05.2023) - Initial realease
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

def main():
    keyMod = GetKeyMod() # Get keymod
    doc.StartUndo() # Start recording undos
    cameraTypes = [5103, 1057516] # Camera types
    selection = doc.GetSelection() # Get selected items
    for s in selection: # Iterate through selection
        if s.GetType() in cameraTypes: # If item is a camera
            null = c4d.BaseObject(c4d.Onull) # Initialize a null object
            null.SetName(s.GetName()+"_CameraTarget") # Set name
            #null.InsertUnder(s) # Insert null under camera object
            firstObject = doc.GetFirstObject() # Get first object of the document
            null.InsertBefore(firstObject) # Move null to top of the object hierarchy
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Add undo for inserting object
            null[c4d.NULLOBJECT_DISPLAY] = 1 # Set shape to locator
            
            if s.GetType() == 5103: # If standard camera
                #null[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = s[c4d.CAMERAOBJECT_TARGETDISTANCE] # Move in Z
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo for changing camera settings
                offset = c4d.Vector(0,0,s[c4d.CAMERAOBJECT_TARGETDISTANCE]) # Z position
                s[c4d.CAMERAOBJECT_TARGETOBJECT] = null # Set camera's focus object
                
            if s.GetType() == 1057516: # If Redshift camera
                #null[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = s[c4d.RSCAMERAOBJECT_FOCUS_DISTANCE] # Move in Z
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo for changing camera settings
                offset = c4d.Vector(0,0,s[c4d.CAMERAOBJECT_TARGETDISTANCE]) # Z position
                s[c4d.RSCAMERAOBJECT_TARGETOBJECT] = null # Set camera's focus object

            if keyMod == "Shift" or keyMod == "Ctrl+Shift" or keyMod == "Alt+Shift" or keyMod == "Alt+Ctrl+Shift":
                targetTag = c4d.BaseTag(5676) # Initialize a target tag
                s.InsertTag(targetTag) # Insert target tag to object
                targetTag[c4d.TARGETEXPRESSIONTAG_LINK] = null # Set target link
                targetTag[c4d.TARGETEXPRESSIONTAG_PITCH] = True # Pitch
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, targetTag) # Add undo for inserting tag

            offset = s.GetMg().Mul(offset) # Multiply matrix with vector
            matrix = s.GetMg() # Initialize a matrix
            matrix.off = offset # Set offset position
            null.SetMg(matrix) # Set global matrix


            s.DelBit(c4d.BIT_ACTIVE) # Deselect camera
            null.SetBit(c4d.BIT_ACTIVE) # Select null
                
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

if __name__ == '__main__':
    main()