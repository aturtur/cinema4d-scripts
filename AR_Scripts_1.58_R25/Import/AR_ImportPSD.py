"""
AR_ImportPSD

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportPSD
Version: 1.0.0
Description-US: Import PSD-file's layers to separate materials. Shift: Generates also image planes.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

http://www.plugincafe.com/forum/forum_posts.asp?TID=13697

Change log:
1.0.0 (11.04.2022) - Initial version
"""

# Libraries
import c4d, os
from c4d.modules import bodypaint as bp
from c4d import storage as s

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
    #if op.GetDown():
    #    return op.GetDown()
    #while not op.GetNext() and op.GetUp():
    #    op = op.GetUp()
    return op.GetNext()

def CollectLayers(op):
    layers = []
    if op is None:
        return
    while op:
        layers.append(op)
        op = GetNextObject(op)
    return layers

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    file = s.LoadDialog(c4d.FILESELECTTYPE_IMAGES, 'Select PSD-file', c4d.FILESELECT_LOAD, '')
    if not file: return # If no folder, quit the script

    keyMod = GetKeyMod() # Get keyboard modifier

    extension = file.rpartition(".")[-1].lower()
    if extension != "psd": return None # Break if not PSD file

    # Preparing texture and layers
    bc = c4d.BaseContainer()
    bc.SetFilename(c4d.LOADTEXTURE_FILENAME, file)
    tex = bp.SendPainterCommand(c4d.PAINTER_LOADTEXTURE, doc, tex=None, bc=bc)
    layers = CollectLayers(tex.GetFirstLayer())

    for i, l in enumerate(layers): #  Iterate through layers

        layerName     = l.GetName()

        layerSet      = c4d.LayerSet()
        layerSetAlpha = c4d.LayerSet()

        layerSet.AddLayer(layerName)
        layerSetAlpha.SetMode(c4d.LAYERSETMODE_LAYERALPHA)
        layerSetAlpha.AddLayer(layerName)

        mat  = c4d.BaseMaterial(c4d.Mmaterial)
        mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
        mat[c4d.MATERIAL_USE_ALPHA] = 1 # Enable alpha channel

        # Color channel
        color = c4d.BaseShader(c4d.Xbitmap)
        color[c4d.BITMAPSHADER_FILENAME] = file
        color[c4d.BITMAPSHADER_LAYERSET] = layerSet
        mat[c4d.MATERIAL_COLOR_SHADER]   = color
        # Get bitmap size
        irs = c4d.modules.render.InitRenderStruct() # Needed to get shader's bitmap info
        if color.InitRender(irs)==c4d.INITRENDERRESULT_OK:
          bitmap = color.GetBitmap() # Get bitmap
          color.FreeRender() # Frees all resources used by this shader
          if bitmap is not None: # If there is bitmap
            width  = bitmap.GetSize()[0] # Get bitmap width in pixels
            height = bitmap.GetSize()[1] # Get bitmap height in pixels

        # Luminance channel
        luminance = c4d.BaseShader(c4d.Xbitmap)
        luminance[c4d.BITMAPSHADER_FILENAME] = file
        luminance[c4d.BITMAPSHADER_LAYERSET] = layerSet
        mat[c4d.MATERIAL_LUMINANCE_SHADER]   = luminance

        # Alpha channel
        alpha = c4d.BaseShader(c4d.Xbitmap)
        alpha[c4d.BITMAPSHADER_FILENAME] = file
        alpha[c4d.BITMAPSHADER_LAYERSET] = layerSetAlpha
        mat[c4d.MATERIAL_ALPHA_SHADER]   = alpha
        
        # Assign shaders to material
        mat.InsertShader(color) # Insert shader to color channel
        mat.InsertShader(luminance) # Insert shader to luminance channel
        mat.InsertShader(alpha) # Insert shader to alpha channel
        
        # Other stuff
        mat.Message(c4d.MSG_UPDATE)
        mat.Update(True, True) # Update material
        #matname = os.path.basename(file).rpartition(".")[0]+"_"+layerName
        matname = layerName
        mat.SetName(matname) # Set material name
        doc.InsertMaterial(mat) # Insert new material to document
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat) # Add undo command for inserting new material

        if keyMod == "Shift": # If Shift key pressed - Generate planes and assign materials to them
            # Create plane
            plane = c4d.BaseObject(c4d.Oplane) # Initialize plane object
            plane.SetName(matname) # Set plane's name same as the material name
            plane[c4d.PRIM_AXIS] = 5 # Set plane's orientation to -z
            plane[c4d.PRIM_PLANE_SUBW] = 1 # Set plane's width segments
            plane[c4d.PRIM_PLANE_SUBH] = 1 # Set plane's height segments
            plane[c4d.PRIM_PLANE_WIDTH]  = width # Set plane's width
            plane[c4d.PRIM_PLANE_HEIGHT] = height # Set planes height
            plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = i*100
            doc.InsertObject(plane) # Insert plane to document
            doc.AddUndo(c4d.UNDOTYPE_NEW, plane) # Add undo command for inserting plane to document

            # Texture tag
            t = c4d.BaseTag(5616) # Initialize texture tag
            plane.InsertTag(t) # Insert texture tag to object
            tag = plane.GetFirstTag() # Get object's first tag
            tag[c4d.TEXTURETAG_MATERIAL]   = mat # Set material to texture tag
            tag[c4d.TEXTURETAG_PROJECTION] = 6 # Set texture projection to uvw mapping
            doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Add undo command for inserting texture tag to object

    bp.SendPainterCommand(c4d.PAINTER_FORCECLOSETEXTURE, doc, tex=tex, bc=c4d.BaseContainer())

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()