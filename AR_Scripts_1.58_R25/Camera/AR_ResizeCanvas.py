"""
AR_ResizeCanvas

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ResizeCanvas
Version: 1.0.6
Description-US: Resizes the canvas without changing the perspective

Changes active render settings resolution and selected/active camera's sensor size (film gate) and possibly also film offsets.

NOTE! If you don't have custom camera active or selected, script will modify default viewport camera's settings!
You can reset default viewport camera with "View -> Frame Default"

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.6 (11.01.2022) - Checks if you really want to modify editor camera
1.0.5 (06.11.2021) - Added option to change 'Focal Length' or 'Sensor Size', added option to get copy of camera and render settings
1.0.4 (07.10.2021) - Updated for R25, added 'Get' button to get the current resolution
1.0.3 (09.09.2021) - Added 'Add' button, instead of setting the exact resolution you can add or substract from the current values
1.0.2 (28.08.2021) - Bug fix (Film aspect ratio value in render settings)
1.0.1 (07.10.2020) - Supports now non perspective camera projections (e.g. parallel, isometric etc.)
"""

# Libraries
import c4d
import re
from c4d import gui
from c4d.gui import GeDialog

# Functions
def CheckCamera(doc):
    # Check camera selection / active camera
    bd = doc.GetActiveBaseDraw() # Get active base draw
    activeCam = bd.GetSceneCamera(doc) # Get active camera
    editorCam = bd.GetEditorCamera() # Get editor camera

    if doc.GetActiveObject() == None: # If no active object
        if activeCam == editorCam: # If camera is default camera
            question = gui.QuestionDialog("Do you really want to modify\ndefault viewport camera?")
            if question == True:
                return editorCam
            else:
                return None
        elif activeCam != editorCam:
            return activeCam
    else:
        activeObject = doc.GetActiveObject() # Get active object
        if activeObject.GetType() == 5103: # If camera
            return activeObject
        else:
            return activeCam

def checkName(name):
    n = name.split("[Resized ")
    if len(n) > 1:
        n = n[1].split("]")
        num = int(n[0])+1
        name = name.replace("[Resized "+n[0]+"]", "[Resized "+str(num)+"]")
        return name
    else:
        return name+" [Resized 1]"

def getFocalLength(old, new, focalLength):
    return (old / new) * focalLength

def getSensorSize(old, new, sensor):
    return sensor * (new / old)

def getFilmAnchor(old, new, current):
    return current * (old / new)

def getFilmOffset(old, new, direction):
    filmOffset = ((1.0 - (old / new)) / 2.0)
    if (direction == "Up") or (direction == "Left"):
        filmOffset = filmOffset * -1.0
    return filmOffset

def resizeComposition(anchor, newWidth, newHeight, method, copyCam, copyRS):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    renderData = doc.GetActiveRenderData() # Get document render data

    camera = CheckCamera(doc) # Check if camera is selected or active
    if camera == False: return

    if copyCam == True: # If "copy camera" checkbox is ticked
        duplicateCamera = camera.GetClone() # Get copy of the camera
        doc.InsertObject(duplicateCamera, None, camera, False) # Insert duplicated camera to document
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, duplicateCamera) # Add undo step for camera changes
        bd = doc.GetActiveBaseDraw() # Get active base draw
        bd.SetSceneCamera(duplicateCamera) # Set active camera
        doc.AddUndo(c4d.UNDOTYPE_BITS, camera) # Add undo
        camera.DelBit(c4d.BIT_ACTIVE) # Deselect old render data
        camera = duplicateCamera # Camera is now the new copy
        camera.SetBit(c4d.BIT_ACTIVE) # Select
        cameraName = checkName(camera.GetName()) # Check name
        camera.SetName(cameraName) # Set new name for the camera


    focalLength = camera[c4d.CAMERA_FOCUS] # Get camera's focal length
    sensorSize = camera[c4d.CAMERAOBJECT_APERTURE] # Get camera's sensor size
    zoom = camera[c4d.CAMERA_ZOOM] # Get camera's zoom value
    oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution
    oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution

    # Focal length method
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera) # Add undo step for camera changes

    oldFilmOffsetY = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y])
    oldFilmOffsetX = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_X])

    if camera[c4d.CAMERA_PROJECTION] == 0: # If camera projection is perspective
        if method == 0: # If method is set to: "Change Camera's Focal Length"
            camera[c4d.CAMERA_FOCUS] = getFocalLength(oldWidth, newWidth, focalLength)
        elif method == 1: # If method is set to: "Change Camera's Sensor Size"
            camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        
    else: # If camera projection is something else than perspective (parallel etc.)
        camera[c4d.CAMERA_ZOOM] = getFilmAnchor(oldWidth, newWidth, zoom)

    if anchor == "Mid Center":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX)

    elif anchor == "Top Center":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Down")
    elif anchor == "Bot Center":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Up")
    elif anchor == "Mid Left":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Right")
    elif anchor == "Mid Right":
        filmOffsetX = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = filmOffsetX

    # Corners
    elif anchor == "Top Left":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Right")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Down")
    elif anchor == "Top Right":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Down")
    elif anchor == "Bot Left":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Right")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Up")
    elif anchor == "Bot Right":
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Up")

    # Set render data stuff
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData) # Add undo step for render data changes
    if copyRS == True: # If "copy render settings" checkbox is ticked
        copyRenderData = renderData.GetClone() # Get copy of the current render data
        renderdataName = checkName(renderData.GetName()) # Check name
        copyRenderData.SetName(renderdataName)
        doc.InsertRenderData(copyRenderData, None, renderData) # Insert new render data to document
        doc.SetActiveRenderData(copyRenderData) # Set new render data to active
        renderData = copyRenderData
    renderData[c4d.RDATA_XRES]       = newWidth
    renderData[c4d.RDATA_YRES]       = newHeight
    renderData[c4d.RDATA_FILMASPECT] = float(newWidth) / float(newHeight)

    doc.SetActiveRenderData(renderData)
    doc.EndUndo() # Stop recording undos
    return True

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()

    # Create Dialog
    def CreateLayout(self):
        # ----------------------------------------------------------------------------------------
        self.SetTitle("Resize composition") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(999, c4d.BFH_CENTER, 1, 1) # Begin 'Main' group
        self.GroupBorderSpace(9, 0, 9, 9)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1000, c4d.BFH_CENTER, 2, 1) # Begin 'Mega1' group
        # ----------------------------------------------------------------------------------------
        # Radio checkboxes
        self.GroupBegin(1001, c4d.BFH_LEFT, 1, 2, "Anchor") # Begin 'Anchor' group
        self.GroupBorderSpace(5, 5, 5, 0)

        self.AddRadioGroup(2000, c4d.BFH_CENTER, 3, 3)
        self.AddChild(2000, 2001, " ")
        self.AddChild(2000, 2002, " ")
        self.AddChild(2000, 2003, " ")
        self.AddChild(2000, 2004, " ")
        self.AddChild(2000, 2005, " ")
        self.AddChild(2000, 2006, " ")
        self.AddChild(2000, 2007, " ")
        self.AddChild(2000, 2008, " ")
        self.AddChild(2000, 2009, " ")
        self.SetBool(2005, 1) # Set default selection
        self.GroupEnd() # End 'Anchor' group
        # ----------------------------------------------------------------------------------------
        # Inputs
        self.GroupBegin(1002, c4d.BFH_RIGHT, 2, 2, "Resolution") # Begin 'Resolution' group
        self.GroupBorderSpace(5, 5, 5, 5)
        self.AddStaticText(3000, c4d.BFH_LEFT, 0, 0, "Width", 0)
        self.AddEditNumberArrows(3001, c4d.BFH_LEFT, initw=80, inith=0)
        self.AddStaticText(3002, c4d.BFH_LEFT, 0, 0, "Height", 0)
        self.AddEditNumberArrows(3003, c4d.BFH_LEFT, initw=80, inith=0)
        self.SetFloat(3001, 0)
        self.SetFloat(3003, 0)
        self.GroupEnd() # End 'Resolution' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # End 'Mega1' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(4000, c4d.BFH_CENTER, 2, 1, "Method") # Begin 'Method' group
        self.GroupBorderSpace(5, 0, 5, 5)
        self.AddStaticText(3000, c4d.BFH_LEFT, 0, 0, "Change Camera's", 0)
        self.AddComboBox(4001, c4d.BFH_LEFT, 150, 13)
        self.AddChild(4001, 0, "Focal Length")
        self.AddChild(4001, 1, "Sensor Size")
        self.SetInt32(4001, 1) # Set default

        self.GroupEnd() # End 'Method' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(5000, c4d.BFH_CENTER, 2, 1, "Copy") # Begin 'Copy' group
        self.GroupBorderSpace(5, 0, 5, 5)

        self.AddCheckbox(5001, c4d.BFH_LEFT, 0, 0, "Copy Camera")
        self.AddCheckbox(5002, c4d.BFH_LEFT, 0, 0, "Copy Render Settings")

        self.GroupEnd() # End 'Method' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1005, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        # Buttons
        self.AddButton(3007, c4d.BFH_LEFT, name="Get") # Add button
        self.AddButton(3004, c4d.BFH_LEFT, name="Set") # Add button
        self.AddButton(3006, c4d.BFH_LEFT, name="Add") # Add button
        self.AddButton(3005, c4d.BFH_LEFT, name="Cancel") # Add button

        self.GroupEnd() # End 'Buttons' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # Begin 'Main' group
        # ----------------------------------------------------------------------------------------
        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        renderData = doc.GetActiveRenderData() # Get document render data

        # Actions here
        if paramid == 3005: # If 'Cancel' button is pressed
            self.Close() # Close dialog

        if paramid in [3004, 3006, 3007]: # If 'Set', 'Add' or 'Get' buttons are pressed
            width   = float(self.GetString(3001)) # Get width input
            height  = float(self.GetString(3003)) # Get height input
            method  = self.GetInt32(4001) # Get method input
            copyCam = self.GetBool(5001) # Get copy camera input
            copyRS  = self.GetBool(5002) # Get copy render settings input

            atl = self.GetBool(2001)      # Get 'Anchor' checkboxes
            atc = self.GetBool(2002)
            atr = self.GetBool(2003)
            aml = self.GetBool(2004)
            amc = self.GetBool(2005)
            amr = self.GetBool(2006)
            abl = self.GetBool(2007)
            abc = self.GetBool(2008)
            abr = self.GetBool(2009)

            if atl == True:
                anchor = "Top Left"
            elif atc == True:
                anchor = "Top Center"
            elif atr == True:
                anchor = "Top Right"
            elif aml == True:
                anchor = "Mid Left"
            elif amc == True:
                anchor = "Mid Center"
            elif amr == True:
                anchor = "Mid Right"
            elif abl == True:
                anchor = "Bot Left"
            elif abc == True:
                anchor = "Bot Center"
            else:
                anchor = "Bot Right"

            if paramid == 3007: # If 'Get'
                self.SetFloat(3001, float(renderData[c4d.RDATA_XRES]))
                self.SetFloat(3003, float(renderData[c4d.RDATA_YRES]))
                
            elif paramid == 3004: # If 'Set'
                resizeComposition(anchor, width, height, method, copyCam, copyRS) # Run the main algorithm

            elif paramid == 3006: # If 'Add'
                oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution
                oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution
                resizeComposition(anchor, oldWidth+width, oldHeight+height, method, copyCam, copyRS) # Run the main algorithm

            c4d.EventAdd() # Refresh Cinema 4D
            pass

        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2, 5, 5) # Open dialog