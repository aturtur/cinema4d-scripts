"""
AR_ImportFspyCamera

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportFspyCamera
Version: 1.0.0
Description-US: Creates a camera from fSpy JSON-file and Background object from Image-file

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

"""
# Libraries
import c4d
import json
import os
from c4d import storage as s
from c4d import utils as u

# Global variables
scale = 100.0 # Set scale

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document

    # Load fSpy data and create the camera object

    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select fspy JSON-file')
    if fn is None: return

    with open(fn) as json_file:
        data = json.load(json_file)

    matrix_rows = [[0, 1, 2, 3],
                   [0, 1, 2, 3],
                   [0, 1, 2, 3],
                   [0, 1, 2, 3]]

    for i, matrix_list in enumerate(data['cameraTransform']['rows']):
        for k in range(0,4):
            matrix_rows[i][k] = matrix_list[k]

    a0 = []
    a1 = []
    a2 = []
    a3 = []

    for i, x in enumerate(matrix_rows):
        a0.append(x[0])
        a1.append(x[1])
        a2.append(x[2])
        a3.append(x[3])

    mat = c4d.Matrix() # Initialize a matrix
    mat.off = c4d.Vector(a3[0], a3[2], a3[1])
    mat.v1 = c4d.Vector(a0[0], a0[2], a0[1])
    mat.v2 = c4d.Vector(a1[0], a1[2], a1[1])
    mat.v3 = c4d.Vector(a2[0], a2[2], a2[1])
    Z = u.MatrixScale(c4d.Vector(1, 1, -1)) # Initialize a scaling matrix
    mat = mat * Z # Flip Z

    # Y-axis up
    glMat = c4d.Matrix()
    R = u.MatrixRotX(u.DegToRad(90))
    glMat = glMat * R
    mat = glMat * mat
    mat.off = mat.off * scale

    doc.StartUndo() # Start recording undos

    cam = c4d.BaseObject(c4d.Ocamera) # Initialize a camera object
    cam.SetMg(mat) # Set matrix
    cam[c4d.CAMERAOBJECT_FOV] = float(data["horizontalFieldOfView"]) # Set field of view
    cam[c4d.CAMERAOBJECT_TARGETDISTANCE] = 20 * scale # Set focus distance
    f = os.path.basename(fn)
    name = f.rpartition(".")[0] # Get name from file path    
    cam.SetName("cam_"+name) # Set camera name
    doc.AddUndo(c4d.UNDOTYPE_NEW, cam) # Record undo step
    doc.InsertObject(cam) # Insert camera to the document

    bd = doc.GetActiveBaseDraw() # Get active base draw
    bd.SetSceneCamera(cam) # Set active camera

    # - - - - - - - - - - - - - - - - - - - -

    # Load background image and generate stuff

    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select background image')
    if fn != None:
        
        mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize a material
        mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
        
        # Color channel
        color = c4d.BaseShader(c4d.Xbitmap)
        color[c4d.BITMAPSHADER_FILENAME] = fn
        mat[c4d.MATERIAL_COLOR_SHADER] = color

        # Luminance channel
        luminance = c4d.BaseShader(c4d.Xbitmap)
        luminance[c4d.BITMAPSHADER_FILENAME] = fn
        mat[c4d.MATERIAL_LUMINANCE_SHADER] = luminance

        # Assign shaders to material
        mat.InsertShader(color) # Insert shader to color channel
        mat.InsertShader(luminance) # Insert shader to luminance channel

        # Other stuff
        mat.Message(c4d.MSG_UPDATE)
        mat.Update(True, True) # Update material

        f = os.path.basename(fn)
        name = f.rpartition(".")[0] # Get name from file path
        mat.SetName(name) # Set material name
        doc.InsertMaterial(mat) # Insert new material to document
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat) # Add undo command for inserting new material

        # Get bitmap size
        irs = c4d.modules.render.InitRenderStruct() # Needed to get shader's bitmap info
        if color.InitRender(irs)==c4d.INITRENDERRESULT_OK:
          bitmap = color.GetBitmap() # Get bitmap
          color.FreeRender() # Frees all resources used by this shader
          if bitmap is not None: # If there is bitmap
            width = bitmap.GetSize()[0] # Get bitmap width in pixels
            height = bitmap.GetSize()[1] # Get bitmap height in pixels

        # Render settings
        renderData = doc.GetActiveRenderData() # Get document render data
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData)
        renderData[c4d.RDATA_XRES] = width
        renderData[c4d.RDATA_YRES] = height
        renderData[c4d.RDATA_FILMASPECT] = float(width) / float(height)
        
        doc.SetActiveRenderData(renderData)

        # Background object
        bgObject = c4d.BaseObject(5122) # Initialize a background object
        doc.InsertObject(bgObject) # Insert object to document
        doc.AddUndo(c4d.UNDOTYPE_NEW, bgObject) # Add undo command for inserting new object

        # Texture tag
        t = c4d.BaseTag(5616) # Initialize texture tag
        bgObject.InsertTag(t) # Insert texture tag to object
        tag = bgObject.GetFirstTag() # Get object's first tag
        tag[c4d.TEXTURETAG_MATERIAL] = mat # Set material to texture tag
        tag[c4d.TEXTURETAG_PROJECTION] = 4 # Set texture projection to Frontal
        doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Add undo command for inserting texture tag to object

    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()