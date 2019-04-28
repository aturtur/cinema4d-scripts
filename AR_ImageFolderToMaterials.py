"""
AR_ImageFolderToMaterials

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImageFolderToMaterials
Description-US: Import image folder to materials
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d, os
from c4d import storage as s

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select image folder',c4d.FILESELECT_DIRECTORY,'')
    if not folder: return
    try: # Try to execute following script
        files = os.listdir(folder)
        for f in files: # Loop through files
            mat = c4d.BaseMaterial(c4d.Mmaterial)
            path = folder+"\\"+f
            mat[c4d.MATERIAL_USE_REFLECTION] = 0 # Disable reflection channel
            
            # Color channel
            color = c4d.BaseShader(c4d.Xbitmap)
            color[c4d.BITMAPSHADER_FILENAME] = path
            mat[c4d.MATERIAL_COLOR_SHADER] = color

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
            matname = f.split(".")[0] # Get material name from file path
            mat.SetName(matname) # Set material name
            doc.InsertMaterial(mat) # Insert new material to document
            doc.AddUndo(c4d.UNDOTYPE_NEW, mat) # Add undo command for inserting new material            
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()