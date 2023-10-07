"""
AR_CameraPlane

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CameraPlane
Version: 1.0.0
Description-US: Creates a camera plane for selected camera(s). Supports Perspective and Parallel projections

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.0.0 (10.01.2023) - Initial realease
"""

# Libraries
import c4d

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
    return 

def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get active objects
    planes = [] # Initialize a list for created camera planes
    cameras = [] # Initialize a list for cameras
    for s in selection: # Iterate through selected objects
        if s.GetType() not in [5103, 1057516]: # If not a camera
             return False # Break the script
         
        else: # Otherwise
            cameras.append(s) # Add camera to camera list
            cam = s # This is a camera
            if s.GetType() == 5103: # If standard camera
                fdist = cam[c4d.CAMERAOBJECT_TARGETDISTANCE] # Get focal distance
            elif s.GetType() == 1057516: # If redshift camera
                fdist = cam[c4d.RSCAMERAOBJECT_FOCUS_DISTANCE] # Get focal distance
    
            plane = c4d.BaseObject(c4d.Oplane) # Initialize a plane object
            plane[c4d.PRIM_PLANE_SUBW] = 1 # Set width segments to 1
            plane[c4d.PRIM_PLANE_SUBH] = 1 # Set height segments to 1
            plane[c4d.PRIM_AXIS] = 5 # Set orientation to "-Z"
            plane.SetName("Camera Plane") # Set plane's name            
            doc.AddUndo(c4d.UNDOTYPE_NEW, plane) # Add undo step for inserting new object
            plane.InsertUnder(cam) # Insert plane under the camera
            plane.SetRelPos(c4d.Vector(0, 0, fdist)) # Set position
            pythonTag = c4d.BaseTag(1022749) # Initialize a Python tag
            plane.InsertTag(pythonTag) # Insert Python tag to the plane
            CreateUserDataLink(pythonTag, "Camera", None)
            pythonTag[c4d.ID_USERDATA,1] = cam
            pythonScript = "# Camera Plane (Python Tag)\n\
# By Arttu Rautio (aturtur)\n\
# https://aturtur.com\n\
# Updated: 10.01.2023\n\
\n\
# Libraries\n\
import c4d\n\
import math\n\
\n\
# Functions\n\
def main():\n\
\n\
    # Get render settings\n\
    renderData = doc.GetActiveRenderData()\n\
    width = float(renderData[c4d.RDATA_XRES])\n\
    height = float(renderData[c4d.RDATA_YRES])\n\
    \n\
    # Object\n\
    obj = op.GetObject()\n\
    \n\
    # Camera\n\
    cam = op[c4d.ID_USERDATA,1]\n\
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
    if cam[c4d.CAMERA_PROJECTION] == 0: # Projection: 'Perspective'\n\
        pass\n\
    elif cam[c4d.CAMERA_PROJECTION] == 1: # Projection: 'Parallel'\n\
        w = 1024 / zoom\n\
        h = w / (width/height)\n\
    else:\n\
        return False\n\
    \n\
    pos_x = w * film_x\n\
    pos_y = h * film_y * -1\n\
    \n\
    # Plane\n\
    plane = op.GetObject()\n\
    plane[c4d.PRIM_PLANE_WIDTH] = w\n\
    plane[c4d.PRIM_PLANE_HEIGHT] = h\n\
    plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = pos_x\n\
    plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = pos_y\n\
    plane[c4d.ID_BASEOBJECT_REL_ROTATION] = c4d.Vector(0,0,0)"
            pythonTag[c4d.TPYTHON_CODE] = pythonScript # Set python script
            planes.append(plane) # Add plane to planes list

    # Deselect old selection
    for c in cameras: # Iterate through cameras
        # Unfold selected objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, c) # Add undo for deselecting
        c.DelBit(c4d.BIT_ACTIVE) # Deselect object
        if c.GetNBit(c4d.NBIT_OM1_FOLD) == 0: # If object is folded
            c.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE) # Unfold

    # Select new objects
    for p in planes: # Iterate through cameras
        p.SetBit(c4d.BIT_ACTIVE) # Select object

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__ == '__main__':
    main()