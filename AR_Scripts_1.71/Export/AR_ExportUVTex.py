"""
AR_ExportUVTex

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ExportUVTex
Version: 1.0.0
Description-US: Exports UV texture for selected object. Remember to select polygons of the object!

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.0.0 (10.01.2023) - Initial realease
"""

# Libraries
import os
import c4d
from c4d.modules import bodypaint as bp
from c4d import storage as s

# Functions
def main():

    resolution   = 4096 # Set resolution
    openLocation = True # If true opens containing folder of the texture
    
    obj = op # Object
    name = obj.GetName() # Get name of the object
    path = doc.GetDocumentPath() # Get file path of project
    
    # Texture creation
    texPath = os.path.join(path, name+"_UV.tif")
    bc = c4d.BaseContainer() # Init a base container
    bc[c4d.TEXTURE_FILEFORMAT]      = c4d.FILTER_TIF # File format
    bc[c4d.TEXTURE_WIDTH]           = resolution # Width resolution
    bc[c4d.TEXTURE_HEIGHT]          = resolution # Height resolution
    bc[c4d.TEXTURE_MODE]            = c4d.COLORMODE_ARGB # Color mode (8-bit RGB channels with 8-bit alpha)
    bc[c4d.TEXTURE_COLOR]           = c4d.Vector(0, 0, 0) # Color
    bc[c4d.TEXTURE_SAVE_IMMEDIATLY] = True # Save immediately, otherwise texture is only created in memory
    tex = bp.PaintTexture.CreateNewTexture(texPath, bc) # Create a new texture

    # Shader creation
    shader = c4d.BaseShader(c4d.Xbitmap) # Initialize bitmap shader
    shader[c4d.BITMAPSHADER_FILENAME] = texPath # Set bitmap file

    # Material creation
    mat = c4d.BaseMaterial(c4d.Mmaterial) # Init a material
    mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
    mat[c4d.MATERIAL_ANIMATEPREVIEW] = 1 # Enable 'Animate Preview'
    mat[c4d.MATERIAL_PREVIEWSIZE] = 1 # Set 'Texture Preview Size' to 'No Scaling'
    mat[c4d.MATERIAL_COLOR_SHADER] = shader # Set shader to material's color channel
    mat.InsertShader(shader) # Insert shader to color channel
    mat.Message(c4d.MSG_UPDATE) # Update material
    mat.Update(True, True) # Update material
    doc.InsertMaterial(mat) # Insert material to the project

    # Texture editing
    bp.PaintTexture.SetSelected_Texture(tex, None) # Select texture
    c4d.CallCommand(170723) # Create UV Mesh Layer
    #c4d.CallCommand(170152) # Outline Polygons
    #c4d.CallCommand(170151) # Fill Polygons
    c4d.CallCommand(170004) # Save Texture
    
    # 
    t = c4d.BaseTag(5616) # Initialize texture tag
    obj.InsertTag(t) # Insert texture tag to object
    tag = obj.GetFirstTag() # Get object's first tag
    tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
    tag[c4d.TEXTURETAG_PROJECTION] = 6 # Set texture projection to uvw mapping
    
    c4d.EventAdd() # Refresh Cinema 4D

    if openLocation == True:
        s.ShowInFinder(texPath, False) # Show the file in the Finder / Explorer
    pass

# Execute main
if __name__ == '__main__':
    main()