"""
AR_CropToIRR

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CropToIRR
Version: 1.0.1
Description-US: Crops canvas to Interactive Render Region

Changes active render settings resolution and selected/active camera's sensor size (film gate) and possibly also film offsets.

NOTE! If you don't have custom camera active or selected, script will modify default viewport camera's settings!
You can reset default viewport camera with "View -> Frame Default"

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (11.01.2022) - Checks if you really want to modify editor camera
1.0.0 (07.12.2021) - First version
"""

# Libraries
import c4d
from c4d import utils as u
from c4d import gui

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
                return activeCam
            else:
                return False
    else:
        activeObject = doc.GetActiveObject() # Get active object
        if activeObject.GetType() == 5103: # If camera
            return activeObject
        else:
            return activeCam

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

def resizeComposition(camera, anchor, newWidth, newHeight):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    renderData = doc.GetActiveRenderData() # Get document render data
    camera = CheckCamera(doc) # Check if camera is selected or active
    focalLength = camera[c4d.CAMERA_FOCUS] # Get camera's focal length
    sensorSize = camera[c4d.CAMERAOBJECT_APERTURE] # Get camera's sensor size
    zoom = camera[c4d.CAMERA_ZOOM] # Get camera's zoom value
    oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution
    oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera) # Add undo step for camera changes
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
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        

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
    renderData[c4d.RDATA_XRES]       = newWidth
    renderData[c4d.RDATA_YRES]       = newHeight
    renderData[c4d.RDATA_FILMASPECT] = float(newWidth) / float(newHeight)

def main():
    global exit

    doc.StartUndo() # Start recording undos
    renderData = doc.GetActiveRenderData() # Get document render data
    bd = doc.GetActiveBaseDraw() # Get base draw
    if bd is None: return
    
    size = bd.GetFrame() # Get viewport size
    vp_width  = size['cr'] # Viewport width
    vp_height = size['cb'] # Viewport height
    
    bc = bd.GetDataInstance() # Get base draw data
    if bc is None: return
    
    subcontainer = bc.GetContainer(430000020) # Get subcontainer (IRR) data
    irr_data = []
    for info in subcontainer:
        irr_data.append(info[1])

    if len(irr_data) == 0:
        gui.MessageDialog("No Interactive Render Region data found.\nRun IRR first!")
        return
    
    a = [irr_data[0], irr_data[1]] # Top left corner position (in %)
    b = [irr_data[2], irr_data[3]] # Bottom right corner position (in %)
    
    # Corners' locations in pixels
    topleft  = [vp_width*a[0], vp_height*a[1]]
    botright = [vp_width*b[0], vp_height*b[1]]

    vp_ar = float(vp_width) / float(vp_height) # Viewport aspect ratio
    rd_ar = renderData[c4d.RDATA_FILMASPECT] # Render data aspect ratio

    rd_width  = renderData[c4d.RDATA_XRES]
    rd_height = renderData[c4d.RDATA_YRES]

    # 1. Crop new render data resolution to viewport aspect ratio
    if rd_ar > vp_ar:
        new_w = rd_width
        new_h = (rd_width / vp_ar)

    elif rd_ar < vp_ar:
        new_w = (rd_height * vp_ar)
        new_h = rd_height

    else:
        new_w = rd_width
        new_h = rd_height

    cam = CheckCamera(doc)
    if cam == False: return

    # 1. First set resolution to match viewport
    resizeComposition(cam, "Mid Center", new_w, new_h)

    # 2. Second crop bottom and right
    x2 = u.RangeMap(botright[0], 0, vp_width, 0, new_w, True)
    y2 = u.RangeMap(botright[1], 0, vp_height, 0, new_h, True)
    trim_w = new_w - x2
    trim_h = new_h - y2
    resizeComposition(cam, "Top Left", new_w-trim_w, new_h-trim_h)

    # 3. Finally crop top and left
    x1 = u.RangeMap(topleft[0], 0, vp_width, 0, new_w, True)
    y1 = u.RangeMap(topleft[1], 0, vp_height, 0, new_h, True)
    trim_w = new_w - trim_w - x1
    trim_h = new_h - trim_h - y1
    resizeComposition(cam, "Bot Right", trim_w, trim_h) # Second trim top left
    
    c4d.CallCommand(430000021) # Toggle interactive render region

    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()