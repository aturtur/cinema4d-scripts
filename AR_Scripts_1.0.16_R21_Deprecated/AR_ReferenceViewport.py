"""
AR_ReferenceViewport

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ReferenceViewport
Version: 1.0
Description-US: Creates a reference view port for helping to animate stuff. SHIFT: Create reference background CTRL: Delete reference setups
Note 1: You have to enable 'Full Animation Redraw' in Preferences/View
Note 2: If you cant see anything try to change 'View Clipping' settings in 'Project Settings'

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d import storage as s
from c4d import gui as g

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
    keyMod = GetKeyMod() # Get keymodifier
    doc.StartUndo() # Start recording undos
    if keyMod != "Ctrl": # Reference background
        fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,"Select reference file",c4d.FILESELECT_LOAD) # Load file
        if fn == None: return None # If no file, stop the script

        # Material
        mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize material
        mat.SetName("AR_REFERENCE_MATERIAL") # Set material name
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
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    if keyMod == "None": # Reference viewport
        # Camera
        cam = c4d.BaseObject(c4d.Ocamera) # Initialize camera object
        cam.SetName("AR_REFERENCE_CAMERA") # Set camera name
        cam[c4d.CAMERAOBJECT_TARGETDISTANCE] = width # Set camera focus to match bitmap width
        cam[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set camera's visible in rendeerr to off
        doc.InsertObject(cam) # Insert camera to document
        doc.AddUndo(c4d.UNDOTYPE_NEW, cam)
        
        # Plane
        plane = c4d.BaseObject(c4d.Oplane) # Initialize plane object
        plane[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set plane's visible in renderer to off
        plane.SetName("AR_REFERENCE_PLANE") # Set plane name
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
        bd[c4d.BASEDRAW_TITLE] = "AR_REFERENCE_VIEWPORT" # Set base view name
            
        cam[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 5000000 # Move camera far away

    if keyMod == "Shift": # Reference background
        # Plane
        bg = c4d.BaseObject(5122) # Initialize a background object
        bg[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1 # Set bg's visible in renderer to off
        bg.SetName("AR_REFERENCE_BACKGROUND") # Set bg name
        doc.InsertObject(bg) # Insert bg object under camera object
        doc.AddUndo(c4d.UNDOTYPE_NEW, bg)

        # Tags
        t = c4d.BaseTag(5616) # Initialize texture tag
        bg.InsertTag(t) # Insert texture tag to object
        tag = bg.GetFirstTag() # Get object's first tag
        tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
        tag[c4d.TEXTURETAG_PROJECTION] = 6 # Set texture projection to uvw mapping

    if keyMod == "Ctrl": # Reference background
        materials = doc.GetMaterials()
        objects = doc.GetObjects()

        for m in materials:
            if m.GetName().find("AR_REFERENCE_") != -1:
                doc.AddUndo(c4d.UNDOTYPE_DELETE, m)
                m.Remove()
        for o in objects:
            if o.GetName().find("AR_REFERENCE_") != -1:
                doc.AddUndo(c4d.UNDOTYPE_DELETE, o)
                o.Remove()
        pass


    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()