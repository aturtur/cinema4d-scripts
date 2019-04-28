"""
AR_CreateReferenceViewport

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateReferenceViewport
Description-US: Creates reference view port for helping to animate stuff
Note 1: You have to enable 'Full Animation Redraw' in Preferences/View
Note 2: If you cant see anything try to change 'View Clipping' settings in 'Project Settings'
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import storage as s
from c4d import gui as g

# Functions
def main():
    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,"Select reference file",c4d.FILESELECT_LOAD) # Load file
    if fn == None: return None # If no file, stop the script
    
    # Material
    mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize material
    mat.SetName("REFERENCE_MATERIAL") # Set material name
    mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
    mat[c4d.MATERIAL_ANIMATEPREVIEW] = 1 # Enable 'Animate Preview'
    mat[c4d.MATERIAL_PREVIEWSIZE] = 1 # Set 'Texture Preview Size' to 'No Scaling'
    shader = c4d.BaseShader(c4d.Xbitmap) # Initialize bitmap shader
    shader[c4d.BITMAPSHADER_FILENAME] = fn # Set bitmap file
    doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
    c4d.CallButton(shader, c4d.BITMAPSHADER_CALCULATE) # Press 'Animation>Calculate' button
    mat[c4d.MATERIAL_COLOR_SHADER] = shader # Set shader to material's color channel
    mat.InsertShader(shader) # Insert shader to color channel
    mat.Message(c4d.MSG_UPDATE) # Update material
    mat.Update(True, True) # Update material
    irs = c4d.modules.render.InitRenderStruct() # Needed to get shader's bitmap info
    if shader.InitRender(irs)==c4d.INITRENDERRESULT_OK:
      bitmap = shader.GetBitmap() # Get bitmap
      shader.FreeRender() # Frees all resources used by this shader
      if bitmap is not None: # If there is bitmap
        width = bitmap.GetSize()[0] # Get bitmap width in pixels
        height = bitmap.GetSize()[1] # Get bitmap height in pixels
    doc.InsertMaterial(mat) # Insert material to document
    
    # Camera
    cam = c4d.BaseObject(c4d.Ocamera) # Initialize camera object
    cam.SetName("REFERENCE_CAMERA") # Set camera name
    cam[c4d.CAMERAOBJECT_TARGETDISTANCE] = width # Set camera focus to match bitmap width
    cam[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set camera's visible in rendeerr to off
    doc.InsertObject(cam) # Insert camera to document
    
    # Plane
    plane = c4d.BaseObject(c4d.Oplane) # Initialize plane object
    plane[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set plane's visible in renderer to off
    plane.SetName("REFERENCE_PLANE") # Set plane name
    plane[c4d.PRIM_AXIS] = 5 # Set plane's orientation to -z
    plane[c4d.PRIM_PLANE_SUBW] = 1 # Set plane's width segments
    plane[c4d.PRIM_PLANE_SUBH] = 1 # Set plane's height segments
    plane[c4d.PRIM_PLANE_WIDTH] = width # Set plane's width
    plane[c4d.PRIM_PLANE_HEIGHT] = height # Set planes height
    plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = width # Set plane's z position
    plane.InsertUnder(cam) # Insert plane object under camera object

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
    bd[c4d.BASEDRAW_TITLE] = "REFERENCE_VIEWPORT" # Set base view name
        
    cam[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 5000000 # Move camera far away
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()