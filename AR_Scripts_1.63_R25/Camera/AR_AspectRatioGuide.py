"""
AR_AspectRatioGuide

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AspectRatioGuide
Version: 1.0.1
Description-US: Creates an aspect ratio guide for selected camera(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (02.05.2022) - Added scale parameter
1.0.0 (05.04.2022) - First version
"""

# Libraries
import c4d
from c4d import utils as u

# Functions
def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_DEFAULT] = link
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
  
    element = obj.AddUserData(bc)
    obj[element] = link
    return element

def CreateUserDataCycle(obj, name, val, parentGroup=None, unit=c4d.DESC_UNIT_LONG):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLEBUTTON
    
    cycleBC = c4d.BaseContainer()
    items = val.split(',')
    for i, item in enumerate(items):
        cycleBC.SetString(i, item)

    bc[c4d.DESC_CYCLE] = cycleBC

    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
  
    element = obj.AddUserData(bc)
    #obj[element] = val
    return element

def CreateUserDataFloat(obj, name, val=1.778, parentGroup=None, unit=c4d.DESC_UNIT_FLOAT):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REAL
    bc[c4d.DESC_MIN] = 0
    bc[c4d.DESC_MAX] = 1000
    bc[c4d.DESC_MINSLIDER] = 0
    bc[c4d.DESC_MAXSLIDER] = 1000
    bc[c4d.DESC_STEP] = 0.001
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup  
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataStaticText(obj, name, val="", parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_STATICTEXT
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataButton(obj, name, parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BUTTON)
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_BUTTON
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    return element

def CreateUserDataGroup(obj, name, parentGroup=None, columns=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_GROUP)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_TITLEBAR] = False
    bc[c4d.DESC_GUIOPEN] = False
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    if columns is not None:
        bc[c4d.DESC_COLUMNS] = columns
    return obj.AddUserData(bc)

def CreateAspectRatioGuide(cam):
    rectangle = c4d.BaseObject(c4d.Osplinerectangle)
    rectangle.SetName("Aspect Ratio Guide")
    pyTag = c4d.BaseTag(1022749)
    pyTag.SetName("Aspect Ratio Guide Python Tag")

    CreateUserDataLink(pyTag, "Camera", None)
    CreateUserDataCycle(pyTag, "Presets", "9:16,3:5,2:3,4:5,1:1,5:4,4:3,5:3,16:9,1.85,21:9,2.35,2.39")
    CreateUserDataFloat(pyTag, "Aspect Ratio", 1.778)
    CreateUserDataFloat(pyTag, "Scale", 1.0)
    CreateUserDataStaticText(pyTag, "Width")
    CreateUserDataStaticText(pyTag, "Height")
    btnGroup = CreateUserDataGroup(pyTag, "Buttons", None, 2) #c4d.DescID(0)
    CreateUserDataButton(pyTag, "Get Current", btnGroup)
    CreateUserDataButton(pyTag, "Crop", btnGroup)

    pyTag[c4d.ID_USERDATA,1] = cam
    
    rectangle.InsertTag(pyTag)
    rectangle.InsertUnder(cam)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, rectangle)

    m = cam.GetMg()
    m.off = m * c4d.Vector(0,0,100)
    rectangle.SetMg(m)

    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# Aspect Ratio Guide (Python Tag)\n\
# By Arttu Rautio (aturtur)\n\
# https://aturtur.com\n\
# Updated: 06.11.2021\n\
\n\
# Libraries\n\
import c4d\n\
import math\n\
\n\
# Functions\n\
def getFocalLength(old, new, focalLength):\n\
    return (old / new) * focalLength\n\
\n\
def getSensorSize(old, new, sensor):\n\
    return sensor * (new / old)\n\
\n\
def getFilmAnchor(old, new, current):\n\
    return current * (old / new)\n\
\n\
def getFilmOffset(old, new):\n\
    filmOffset = ((1.0 - (old / new)) / 2.0)\n\
    return filmOffset\n\
\n\
def resizeComposition(camera, newWidth, newHeight):\n\
\n\
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document\n\
    doc.StartUndo() # Start recording undos\n\
    renderData = doc.GetActiveRenderData() # Get document render data\n\
    focalLength = camera[c4d.CAMERA_FOCUS] # Get camera's focal length\n\
    sensorSize = camera[c4d.CAMERAOBJECT_APERTURE] # Get camera's sensor size\n\
    zoom = camera[c4d.CAMERA_ZOOM] # Get camera's zoom value\n\
    oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution\n\
    oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution\n\
    # Focal length method\n\
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera) # Add undo step for camera changes\n\
    oldFilmOffsetY = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y])\n\
    oldFilmOffsetX = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_X])\n\
    camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(float(oldWidth), float(newWidth), sensorSize)\n\
    camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(float(oldHeight), float(newHeight), oldFilmOffsetY)\n\
    camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(float(oldWidth), float(newWidth), oldFilmOffsetX)\n\
    # Set render data stuff\n\
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData) # Add undo step for render data changes\n\
    renderData[c4d.RDATA_XRES]       = float(newWidth)\n\
    renderData[c4d.RDATA_YRES]       = float(newHeight)\n\
    renderData[c4d.RDATA_FILMASPECT] = float(newWidth) / float(newHeight)\n\
    doc.SetActiveRenderData(renderData)\n\
    doc.EndUndo() # Stop recording undos\n\
    return True\n\
\n\
def message(id, data):\n\
    doc = c4d.documents.GetActiveDocument()\n\
    renderData = doc.GetActiveRenderData()\n\
    if id == c4d.MSG_DESCRIPTION_COMMAND:\n\
        id2 = data['id'][0].id\n\
        if id2 == c4d.ID_USERDATA:\n\
            userDataId = data['id'][1].id\n\
            if userDataId == 2:\n\
                preset = op[c4d.ID_USERDATA,2]\n\
                if preset == 0:\n\
                    op[c4d.ID_USERDATA,3] = 0.5625\n\
                elif preset == 1:\n\
                     op[c4d.ID_USERDATA,3] = 0.6\n\
                elif preset == 2:\n\
                     op[c4d.ID_USERDATA,3] = 0.6666666666666666\n\
                elif preset == 3:\n\
                     op[c4d.ID_USERDATA,3] = 0.8\n\
                elif preset == 4:\n\
                     op[c4d.ID_USERDATA,3] = 1\n\
                elif preset == 5:\n\
                     op[c4d.ID_USERDATA,3] = 1.25\n\
                elif preset == 6:\n\
                     op[c4d.ID_USERDATA,3] = 1.3333333333333333\n\
                elif preset == 7:\n\
                     op[c4d.ID_USERDATA,3] = 1.6666666666666667\n\
                elif preset == 8:\n\
                     op[c4d.ID_USERDATA,3] = 1.7777777777777777\n\
                elif preset == 9:\n\
                     op[c4d.ID_USERDATA,3] = 1.85\n\
                elif preset == 10:\n\
                     op[c4d.ID_USERDATA,3] = 2.3333333333333335\n\
                elif preset == 11:\n\
                     op[c4d.ID_USERDATA,3] = 2.35\n\
                elif preset == 12:\n\
                     op[c4d.ID_USERDATA,3] = 2.39\n\
\n\
            if userDataId == 8: # Get current aspect ratio\n\
                doc.StartUndo()\n\
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, op)\n\
                op[c4d.ID_USERDATA,3] = renderData[c4d.RDATA_FILMASPECT]\n\
                doc.EndUndo()\n\
                c4d.EventAdd()\n\
\n\
            if userDataId == 9: # Crop\n\
                resizeComposition(op[c4d.ID_USERDATA,1], op[c4d.ID_USERDATA,4], op[c4d.ID_USERDATA,5])\n\
                c4d.EventAdd()\n\
\n\
def main():\n\
    doc = c4d.documents.GetActiveDocument()\n\
    renderData = doc.GetActiveRenderData()\n\
    width = float(renderData[c4d.RDATA_XRES])\n\
    height = float(renderData[c4d.RDATA_YRES])\n\
    obj     = op.GetObject()\n\
    presets = op[c4d.ID_USERDATA,2]\n\
    cam     = op[c4d.ID_USERDATA,1]\n\
    if cam == None: return False\n\
    new_ar  = op[c4d.ID_USERDATA,3]\n\
    scale   = op[c4d.ID_USERDATA,4]\n\
    fov_ver = cam[c4d.CAMERAOBJECT_FOV_VERTICAL]\n\
    fov_hor = cam[c4d.CAMERAOBJECT_FOV]\n\
    zoom    = cam[c4d.CAMERA_ZOOM]\n\
    film_x  = cam[c4d.CAMERAOBJECT_FILM_OFFSET_X]\n\
    film_y  = cam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]\n\
    d       = obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]\n\
\n\
    fv = math.tan((fov_ver * 0.5)) * 2.0\n\
    fh = math.tan((fov_hor * 0.5)) * 2.0\n\
    h  = d * fv\n\
    w  = d * fh\n\
\n\
    pos_x = w * film_x\n\
    pos_y = h * film_y * -1\n\
\n\
    old_ar = width / height\n\
    if old_ar > new_ar:\n\
        w2 = h * new_ar\n\
        h2 = h\n\
        new_w = round((height * new_ar * scale),2)\n\
        new_h = round(height * 1 * scale, 2)\n\
\n\
    elif old_ar < new_ar:\n\
        w2 = w\n\
        h2 = w / new_ar\n\
        new_w = round(width * 1, 2)\n\
        new_h = round((width / new_ar),2)\n\
\n\
    else:\n\
        w2 = w\n\
        h2 = h\n\
        new_w = round(width * 1 * scale, 2)\n\
        new_h = round(height * 1 * scale, 2)\n\
\n\
    op[c4d.ID_USERDATA,5] = str(round(new_w * scale, 2))\n\
    op[c4d.ID_USERDATA,6] = str(round(new_h * scale, 2))\n\
\n\
    obj[c4d.PRIM_RECTANGLE_HEIGHT] = h2 * scale\n\
    obj[c4d.PRIM_RECTANGLE_WIDTH]  = w2 * scale\n\
\n\
    obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = pos_x\n\
    obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = pos_y\n\
\n\
    pass"

    # -------------------------------------------------------

    pyTag.SetBit(c4d.BIT_ACTIVE)

    return True # All good

def main():
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(1)
    if len(selection) != 0:
        for s in selection:
            if s.GetType() == 5103:
                CreateAspectRatioGuide(s) # Run the function
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                if s.GetNBit(c4d.NBIT_OM1_FOLD) == 0: # If object is folded
                    s.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE) # Unfold
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                s.DelBit(c4d.BIT_ACTIVE)

    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()