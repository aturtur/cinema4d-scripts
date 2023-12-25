"""
AR_Reference

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Reference
Version: 1.1.0
Description-US: Creates reference

Notice: Script requires and will enable 'Full Animation Redraw' in Preferences/View

Current time declares the starting point of the reference animation!

If you cant see reference  try to change 'View Clipping' settings in 'Project Settings'

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.1.0 (09.12.2023) - Dialog with options
1.0.1 (29.03.2022) - Updated for R25
"""
# Libraries
import c4d
from c4d import storage as s
from c4d import gui as g
from c4d.gui import GeDialog

# Global variables
GROUP_MAIN       = 1000
GROUP_OPTIONS    = 1001
GROUP_BUTTONS    = 1002
GROUP_FILEPATH   = 1003

COMBO_REFERENCE  = 2000
TEXT_REFERENCE   = 2001
EDIT_FILEPATH    = 2002
TEXT_FILEPATH    = 2003

MTHD_VIEWPORT    = 4001
MTHD_BACKGROUND  = 4002
MTHD_CAMERAPLANE = 4003

BUTTON_OK        = 3000
BUTTON_CANCEL    = 3001
BUTTON_FILEPATH  = 3002

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()

    # Create Dialog
    def CreateLayout(self):
        # ----------------------------------------------------------------------------------------
        self.SetTitle("Reference") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GROUP_MAIN, c4d.BFH_LEFT, 1, 1) # Begin 'Main' group
        self.GroupBorderSpace(9, 0, 9, 9)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GROUP_FILEPATH, c4d.BFH_LEFT, 3, 1, "Filepath") # Begin 'Options' group
        self.GroupBorderSpace(5, 0, 5, 5)

        self.AddStaticText(TEXT_FILEPATH, c4d.BFH_LEFT, 0, 0, "File Path", 0)
        self.AddEditText(EDIT_FILEPATH, c4d.BFH_LEFT, 250, 0)
        self.AddButton(BUTTON_FILEPATH, c4d.BFH_LEFT, name="...") # File path button

        self.GroupEnd() # End 'Options' group

        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_LEFT, 2, 1, "Options") # Begin 'Options' group
        self.GroupBorderSpace(5, 0, 5, 5)

        self.AddStaticText(TEXT_REFERENCE, c4d.BFH_LEFT, 0, 0, "Reference", 0)
        self.AddComboBox(COMBO_REFERENCE, c4d.BFH_LEFT, 150, 13)
        self.AddChild(COMBO_REFERENCE, MTHD_BACKGROUND, "Background")
        self.AddChild(COMBO_REFERENCE, MTHD_CAMERAPLANE, "Camera Plane")
        self.AddChild(COMBO_REFERENCE, MTHD_VIEWPORT, "Viewport")
        self.SetInt32(COMBO_REFERENCE, MTHD_BACKGROUND) # Set default

        self.GroupEnd() # End 'Options' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GROUP_BUTTONS, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group

        # Buttons
        self.AddButton(BUTTON_OK, c4d.BFH_LEFT, name="Ok") # Add button
        self.AddButton(BUTTON_CANCEL, c4d.BFH_LEFT, name="Cancel") # Add button

        self.GroupEnd() # End 'Buttons' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # Begin 'Main' group
        # ----------------------------------------------------------------------------------------
        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        # Actions here

        if paramid == BUTTON_FILEPATH: # If '...' button is pressed
            fn = LoadFile()
            if fn != None:
                self.SetString(EDIT_FILEPATH, fn)
            else:
                pass

        if paramid == BUTTON_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog

        if paramid == BUTTON_OK: # If 'Ok' button is pressed
            filePath = self.GetString(EDIT_FILEPATH) # Get file path input
            mode = self.GetInt32(COMBO_REFERENCE) # Get reference mode input

            if mode == MTHD_VIEWPORT: # If viewport mode
                self.Close() # Close dialog
                mat, width, height = CreateMaterial(filePath) # Create material
                CreateReferenceViewport(mat, width, height) # Create reference viewport

            elif mode == MTHD_BACKGROUND: # If background mode
                self.Close() # Close dialog
                mat, width, height = CreateMaterial(filePath) # Create material
                CreateReferenceBackground(mat) # Create reference background

            elif mode == MTHD_CAMERAPLANE: # If camera plane mode
                self.Close() # Close dialog
                mat, width, height = CreateMaterial(filePath) # Create material
                cam = doc.GetActiveObject() # Get selected object
                CreateReferenceCameraPlane(mat, cam) # Create reference camera plane

                
            c4d.EventAdd() # Refresh Cinema 4D
            pass

        return True # Everything is fine

# Functions
def Prefs(id):
    return c4d.plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

def LoadFile():
    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,"Select reference file",c4d.FILESELECT_LOAD) # Load file
    if fn == None:
        return None
    else:
        return fn

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

def CreateMaterial(fn):
    # Material
    mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize material
    mat.SetName("AR_REF_MATERIAL") # Set material name
    mat[c4d.MATERIAL_USE_COLOR] = 0 # Disable color channel
    mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
    mat[c4d.MATERIAL_USE_LUMINANCE] = 1 # Enable luminance channel
    mat[c4d.MATERIAL_ANIMATEPREVIEW] = 1 # Enable 'Animate Preview'
    mat[c4d.MATERIAL_PREVIEWSIZE] = 1 # Set 'Texture Preview Size' to 'No Scaling'
    shader = c4d.BaseShader(c4d.Xbitmap) # Initialize bitmap shader
    shader[c4d.BITMAPSHADER_FILENAME] = fn # Set bitmap file
    doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
    c4d.CallButton(shader, c4d.BITMAPSHADER_CALCULATE) # Press 'Animation>Calculate' button
    shader[c4d.BITMAPSHADER_TIMING_TIMING] = 2 # Set 'Timing' to 'Range'
    rangeInFrames = shader[c4d.BITMAPSHADER_TIMING_TO] - shader[c4d.BITMAPSHADER_TIMING_FROM]
    currentFrame = doc.GetTime().GetFrame(doc.GetFps()) # Get current frame
    shader[c4d.BITMAPSHADER_TIMING_RANGEFROM] = c4d.BaseTime((currentFrame) / doc.GetFps())
    shader[c4d.BITMAPSHADER_TIMING_RANGETO] = c4d.BaseTime((currentFrame + rangeInFrames) / doc.GetFps())
    mat[c4d.MATERIAL_COLOR_SHADER] = shader # Set shader to material's color channel
    mat[c4d.MATERIAL_LUMINANCE_SHADER] = shader # Set shader to material's luminance channel
    mat.InsertShader(shader) # Insert shader to material
    mat.Message(c4d.MSG_UPDATE) # Update material
    mat.Update(True, True) # Update material
    irs = c4d.modules.render.InitRenderStruct() # Needed to get shader's bitmap info
    if shader.InitRender(irs)==c4d.INITRENDERRESULT_OK:
      bitmap = shader.GetBitmap() # Get bitmap
      shader.FreeRender() # Frees all resources used by this shader
      if bitmap is not None: # If there is bitmap
        width = bitmap.GetSize()[0] # Get bitmap width in pixels
        height = bitmap.GetSize()[1] # Get bitmap height in pixels

    return mat, width, height # Return material and some data

def CreateReferenceViewport(mat, width, height):
    # Reference viewport

    # Put 'Full Animation Redraw' on, if it's not
    if Prefs(465001625)[c4d.PREF_VIEW_FULLANIMREDRAW] == False:
        Prefs(465001625)[c4d.PREF_VIEW_FULLANIMREDRAW] = True

    # Add material
    doc.InsertMaterial(mat) # Insert material to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    # Camera
    cam = c4d.BaseObject(c4d.Ocamera) # Initialize camera object
    cam.SetName("AR_REF_CAM") # Set camera name
    cam[c4d.CAMERAOBJECT_TARGETDISTANCE] = width # Set camera focus to match bitmap width
    cam[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set camera's visible in rendeerr to off
    doc.InsertObject(cam) # Insert camera to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, cam)

    # Plane
    plane = c4d.BaseObject(c4d.Oplane) # Initialize plane object
    plane[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set plane's visible in renderer to off
    plane.SetName("AR_REF_PLANE") # Set plane name
    plane[c4d.PRIM_AXIS] = 5 # Set plane's orientation to -z
    plane[c4d.PRIM_PLANE_SUBW] = 1 # Set plane's width segments
    plane[c4d.PRIM_PLANE_SUBH] = 1 # Set plane's height segments
    plane[c4d.PRIM_PLANE_WIDTH] = width # Set plane's width
    plane[c4d.PRIM_PLANE_HEIGHT] = height # Set planes height
    plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = width # Set plane's z position
    plane.InsertUnder(cam) # Insert plane object under camera object
    doc.AddUndo(c4d.UNDOTYPE_NEW, plane)

    # Tags
    t = c4d.BaseTag(5616) # Initialize texture tag
    plane.InsertTag(t) # Insert texture tag to object
    tag = plane.GetFirstTag() # Get object's first tag
    tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
    tag[c4d.TEXTURETAG_PROJECTION] = 6 # Set texture projection to uvw mapping
    d = c4d.BaseTag(5613) # Initialize display tag
    d[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = True # Use custom shading mode
    d[c4d.DISPLAYTAG_SDISPLAYMODE] = 7 # Use 'Constant Shading'
    d[c4d.DISPLAYTAG_AFFECT_TEXTURES] = True # Use textures
    plane.InsertTag(d) # Insert display tag to object

    # Base view
    c4d.CallCommand(12544) # Create new viewport
    bd = doc.GetActiveBaseDraw() # Get active base draw
    bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 1 # Set tinted borders for base view
    bd[c4d.BASEDRAW_DATA_CAMERA] = cam # Set base view's camera
    bd[c4d.BASEDRAW_TITLE] = "AR_REF_VIEW" # Set base view name
        
    cam[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 5000000 # Move camera far away

def CreateReferenceBackground(mat):
    # Reference background

    # Add material
    doc.InsertMaterial(mat) # Insert material to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    # Plane
    bg = c4d.BaseObject(5122) # Initialize a background object
    bg[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set bg's visible in renderer to off
    bg.SetName("AR_REF_BG") # Set bg name
    doc.InsertObject(bg) # Insert bg object under camera object
    doc.AddUndo(c4d.UNDOTYPE_NEW, bg)

    # Tags
    t = c4d.BaseTag(5616) # Initialize texture tag
    bg.InsertTag(t) # Insert texture tag to object
    tag = bg.GetFirstTag() # Get object's first tag
    tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
    tag[c4d.TEXTURETAG_PROJECTION] = 4 # Set texture projection to frontal mapping

def CreateReferenceCameraPlane(mat, cam):
    # Reference camera pLane
    if cam == None:
        return False

    # Add material
    doc.InsertMaterial(mat) # Insert material to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    if cam.GetType() == 5103: # If standard camera
        fdist = cam[c4d.CAMERAOBJECT_TARGETDISTANCE] # Get focal distance
    elif cam.GetType() == 1057516: # If redshift camera
        fdist = cam[c4d.RSCAMERAOBJECT_FOCUS_DISTANCE] # Get focal distance

    plane = c4d.BaseObject(c4d.Oplane) # Initialize a plane object
    plane[c4d.PRIM_PLANE_SUBW] = 1 # Set width segments to 1
    plane[c4d.PRIM_PLANE_SUBH] = 1 # Set height segments to 1
    plane[c4d.PRIM_AXIS] = 5 # Set orientation to "-Z"
    plane.SetName("Reference Plane") # Set plane's name            
    doc.AddUndo(c4d.UNDOTYPE_NEW, plane) # Add undo step for inserting new object
    plane.InsertUnder(cam) # Insert plane under the camera
    plane.SetRelPos(c4d.Vector(0, 0, fdist)) # Set position
    pythonTag = c4d.BaseTag(1022749) # Initialize a Python tag
    plane.InsertTag(pythonTag) # Insert Python tag to the plane
    CreateUserDataLink(pythonTag, "Camera", None)
    pythonTag[c4d.ID_USERDATA,1] = cam
    pythonScript = "# Reference Camera Plane (Python Tag)\n\
# By Arttu Rautio (aturtur)\n\
# https://aturtur.com\n\
# Updated: 09.12.2023\n\
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

    t = c4d.BaseTag(5616) # Initialize texture tag
    plane.InsertTag(t) # Insert texture tag to object
    tag = plane.GetFirstTag() # Get object's first tag
    tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
    tag[c4d.TEXTURETAG_PROJECTION] = 6 # Set texture projection to UVW mapping

    pass    


def main():
    keyMod = GetKeyMod() # Get keymodifier
    doc.StartUndo() # Start recording undos
    dlg = Dialog() # Create dialog object
    dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()