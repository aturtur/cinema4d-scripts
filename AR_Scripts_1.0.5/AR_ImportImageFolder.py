"""
AR_ImportImageFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportImageFolder
Version: 1.0
Description-US: Import image folder to materials. SHIFT: Generates image planes.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d, os
from c4d import storage as s

# Functions
def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select image folder',c4d.FILESELECT_DIRECTORY,'')
    if not folder: return # If no folder, quit the script

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

    try: # Try to execute following script
        files = os.listdir(folder)
        for f in files: # Loop through files
            extension = f.rpartition(".")[-1].lower()
            formats = ["tif", "tiff", "psd", "jpg", "jpeg", "png", "exr", "tga"] # Supported file formats
            if extension in formats: # If file is supported
                mat = c4d.BaseMaterial(c4d.Mmaterial)
                path = os.path.join(folder, f) #path = folder+"\\"+f
                mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
                                
                # Color channel
                color = c4d.BaseShader(c4d.Xbitmap)
                color[c4d.BITMAPSHADER_FILENAME] = path
                mat[c4d.MATERIAL_COLOR_SHADER] = color

                # Get bitmap size
                irs = c4d.modules.render.InitRenderStruct() # Needed to get shader's bitmap info
                if color.InitRender(irs)==c4d.INITRENDERRESULT_OK:
                  bitmap = color.GetBitmap() # Get bitmap
                  color.FreeRender() # Frees all resources used by this shader
                  if bitmap is not None: # If there is bitmap
                    width = bitmap.GetSize()[0] # Get bitmap width in pixels
                    height = bitmap.GetSize()[1] # Get bitmap height in pixels

                # Luminance channel
                luminance = c4d.BaseShader(c4d.Xbitmap)
                luminance[c4d.BITMAPSHADER_FILENAME] = path
                mat[c4d.MATERIAL_LUMINANCE_SHADER] = luminance

                # Alpha channel
                alpha = c4d.BaseShader(c4d.Xbitmap)
                alpha[c4d.BITMAPSHADER_FILENAME] = path
                mat[c4d.MATERIAL_ALPHA_SHADER] = alpha
                
                # Assign shaders to material
                mat.InsertShader(color) # Insert shader to color channel
                mat.InsertShader(luminance) # Insert shader to luminance channel
                mat.InsertShader(alpha) # Insert shader to alpha channel
                
                # Other stuff
                mat.Message(c4d.MSG_UPDATE)
                mat.Update(True, True) # Update material
                matname = f.rpartition(".")[0] # Get material name from file path
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
                    plane[c4d.PRIM_PLANE_WIDTH] = width # Set plane's width
                    plane[c4d.PRIM_PLANE_HEIGHT] = height # Set planes height
                    doc.InsertObject(plane) # Insert plane to document
                    doc.AddUndo(c4d.UNDOTYPE_NEW, plane) # Add undo command for inserting plane to document

                    # Texture tag
                    t = c4d.BaseTag(5616) # Initialize texture tag
                    plane.InsertTag(t) # Insert texture tag to object
                    tag = plane.GetFirstTag() # Get object's first tag
                    tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
                    tag[c4d.TEXTURETAG_PROJECTION] = 6 # Set texture projection to uvw mapping
                    doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Add undo command for inserting texture tag to object

    except: # If something went wrong
        pass # Do nothing

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()