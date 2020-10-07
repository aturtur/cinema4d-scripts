"""
AR_ResizeCanvas

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ResizeCanvas
Version: 1.01
Description-US: Resizes canvas without changing the perspective.
Changes active render settings resolution and selected/active camera's sensor size (film gate) and possibly also film offsets.
NOTE! If you don't have custom camera active or selected, script will modify default viewport camera's settings!
You can reset default viewport camera with "View -> Frame Default"

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
07.10.2020 - Supports now non perspective camera projections (e.g. parallel, isometric etc.)
"""
# Libraries
import c4d
from c4d import gui
from c4d.gui import GeDialog

# Functions
def checkCamera(doc):
    # Check camera selection / active camera
    bd = doc.GetActiveBaseDraw() # Get active base draw
    activeCam = bd.GetSceneCamera(doc) # Get active camera
    if doc.GetActiveObject() == None: # If no active object
        return activeCam
    else:
        activeObject = doc.GetActiveObject() # Get active object
        if activeObject.GetType() == 5103: # If camera
            return activeObject
        else:
            return activeCam

def getSensorSize(old, new, sensor):
    return sensor * (new / old)

def getFilmAnchor(old, new, current):
    return current * (old / new)

def getFilmOffset(old, new, direction):
    filmOffset = ((1.0 - (old / new)) / 2.0)
    if (direction == "Up") or (direction == "Left"):
        filmOffset = filmOffset * -1.0
    return filmOffset

def resizeComposition(anchor, newWidth, newHeight):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    renderData = doc.GetActiveRenderData() # Get document render data

    camera = checkCamera(doc) # Check if camera is selected or active

    focalLength = camera[c4d.CAMERA_FOCUS] # Get camera's focal length
    sensorSize = camera[c4d.CAMERAOBJECT_APERTURE] # Get camera's sensor size
    zoom = camera[c4d.CAMERA_ZOOM] # Get camera's zoom value
    oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution
    oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution

    # Focal length method
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera) # Add undo step for camera changes
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData) # Add undo step for render data changes

    oldFilmOffsetY = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y])
    oldFilmOffsetX = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_X])

    if camera[c4d.CAMERA_PROJECTION] == 0: # If camera projection is perspective
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

    renderData[c4d.RDATA_XRES] = newWidth
    renderData[c4d.RDATA_YRES] = newHeight
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
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        renderData = doc.GetActiveRenderData() # Get document render data
        oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution
        oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution
        # ----------------------------------------------------------------------------------------
        self.SetTitle("Resize composition") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1000, c4d.BFH_CENTER, 2, 1) # Begin 'Mega1' group
        # ----------------------------------------------------------------------------------------
        # Radio checkboxes
        self.GroupBegin(1001, c4d.BFH_LEFT, 1, 2, "Anchor") # Begin 'Anchor' group
        self.GroupBorder(c4d.BORDER_ROUND)
        self.GroupBorderSpace(5, 5, 5, 5)

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
        self.GroupBorder(c4d.BORDER_ROUND)
        self.GroupBorderSpace(5, 5, 5, 5)
        self.AddStaticText(3000, c4d.BFH_LEFT, 0, 0, "Width", 0)
        self.AddEditNumberArrows(3001, c4d.BFH_LEFT, initw=80, inith=0)
        self.AddStaticText(3002, c4d.BFH_LEFT, 0, 0, "Height", 0)
        self.AddEditNumberArrows(3003, c4d.BFH_LEFT, initw=80, inith=0)
        self.SetFloat(3001, oldWidth)
        self.SetFloat(3003, oldHeight)
        self.GroupEnd() # End 'Resolution' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # End 'Mega1' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1005, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        # Buttons
        self.AddButton(3004, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(3005, c4d.BFH_RIGHT, name="Cancel") # Add button

        self.GroupEnd() # End 'Buttons' group
        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        # Actions here
        if paramid == 3005: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == 3004: # If 'Accept' button is pressed
            width =  float(self.GetString(3001)) # Get width input
            height = float(self.GetString(3003)) # Get height input

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

            resizeComposition(anchor, width, height) # Run the main algorithm
            c4d.EventAdd() # Refresh Cinema 4D
            pass

        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2, 5, 5) # Open dialog