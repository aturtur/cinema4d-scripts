"""
AR_CycleCameras

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CycleCameras
Version: 1.1.0
Description-US: Cycles through available cameras

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.1.0 (25.05.2023) - Support for camera selection and Selection object
1.0.0 (03.03.2023) - Initial realease
"""

# Libraries
import c4d

# Global variables
camTypes = [5103, 1057516]

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
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectCameras(op):
    cameras = []
    if op is None:
        return
    while op:
        if op.GetType() in camTypes:
            cameras.append(op)
        op = GetNextObject(op)
    return cameras

def main():
    keymod = GetKeyMod()
    bd = doc.GetActiveBaseDraw() # Get active base draw
    camera = bd.GetSceneCamera(doc) # Get active camera
    cameras = CollectCameras(doc.GetFirstObject())
    editorCamera = bd.GetEditorCamera()
    cameras.insert(0, editorCamera)

    selectedCameras = [] # Initialise a list for selected cameras
    selection = doc.GetActiveObjects(1) # Get active objects (include children, if selected)

    if len(selection) != 0: # If selected objects
        for s in selection: # Iterate through selected objects
            if s.GetType() in camTypes: # If camera object selected
                selectedCameras.append(s) # Add camera to list
            if s.GetType() == 5190: # If Selection object selected
                inexcludedata = s[c4d.SELECTIONOBJECT_LIST]
                cnt = inexcludedata.GetObjectCount() # Get number of items
                for i in range(0, cnt): # Iterate through InExclude data list
                    item = inexcludedata.ObjectFromIndex(doc, i) # Get object
                    if item.GetType() in camTypes: # If camera
                        selectedCameras.append(item) # Add camera to list

    if len(selectedCameras) != 0: # If selected ameras
        try:
            currentIndex = selectedCameras.index(camera)
        except:
            currentIndex = 0
        if keymod in ["Shift", "Alt+Ctrl+Shift", "Ctrl+Shift", "Alt+Shift"]:
            bd.SetSceneCamera(selectedCameras[(currentIndex-1)%len(selectedCameras)])
        else:
            bd.SetSceneCamera(selectedCameras[(currentIndex+1)%len(selectedCameras)])
    else:
        currentIndex = cameras.index(camera)
        if keymod in ["Shift", "Alt+Ctrl+Shift", "Ctrl+Shift", "Alt+Shift"]:
            bd.SetSceneCamera(cameras[(currentIndex-1)%len(cameras)])
        else:
            bd.SetSceneCamera(cameras[(currentIndex+1)%len(cameras)])

    c4d.EventAdd()
    pass

# Execute main
if __name__ == '__main__':
    main()