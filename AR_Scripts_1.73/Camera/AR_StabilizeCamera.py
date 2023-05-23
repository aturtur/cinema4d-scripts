"""
AR_StabilizeCamera

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_StabilizeCamera
Version: 1.0.0
Description-US: Stabilizes active camera view to selected object

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.0.0 (03.03.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None): # Create User Data Link
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

def CreateStabilizedCamera(camera, obj):
    cam = camera.GetClone()
    cam.SetName(camera.GetName()+"_Stabilized")
    helper = c4d.BaseObject(c4d.Onull)
    helper.SetName("Helper")
    helper.InsertUnder(cam)
    cam.InsertAfter(camera)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, cam)

    # Priority data setup
    prioritydata = c4d.PriorityData() # Initialize a priority data
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 499) # Set priority value to last possible value
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false

    pythonScript = "import math\n\
import c4d\n\
from c4d import utils as u\
\n\
# Functions\n\
def main():\n\
    obj = op[c4d.ID_USERDATA,1]\n\
    cam = op.GetObject()\n\
    dummy = op.GetObject().GetDown()\n\
\n\
    dummy.SetMg(obj.GetMg())\n\
\n\
    fov_ver = cam[c4d.CAMERAOBJECT_FOV_VERTICAL]\n\
    fov_hor = cam[c4d.CAMERAOBJECT_FOV]\n\
    zoom    = cam[c4d.CAMERA_ZOOM]\n\
    d       = dummy[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]\n\
    x       = dummy[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X]\n\
    y       = dummy[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y]\n\
\n\
    fv = math.tan((fov_ver * 0.5)) * 2.0\n\
    fh = math.tan((fov_hor * 0.5)) * 2.0\n\
    h  = d * fv\n\
    w  = d * fh\n\
\n\
    fx = u.RangeMap(x, -w, w, -1, 1, True)\n\
    fy = u.RangeMap(y, -h, h, -1, 1, True)*-1\n\
\n\
    cam[c4d.CAMERAOBJECT_FILM_OFFSET_X] = fx\n\
    cam[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = fy\n\
    cam[c4d.CAMERAOBJECT_TARGETDISTANCE] = d\n\
    pass"

    pythonTag = c4d.BaseTag(1022749) # Initialize a Python tag
    pythonTag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set prioritydata
    cam.InsertTag(pythonTag)
    CreateUserDataLink(pythonTag, "Link", obj)
    pythonTag[c4d.TPYTHON_CODE] = pythonScript

    return cam

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    bd = doc.GetActiveBaseDraw() # Get active base draw
    camera = bd.GetSceneCamera(doc) # Get active camera
    selected = doc.GetActiveObject() # Get active object
    stabilizedCamera = CreateStabilizedCamera(camera, selected)
    bd.SetSceneCamera(stabilizedCamera) # Set new active camera
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    pass

# Execute main
if __name__ == '__main__':
    main()