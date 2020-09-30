"""
AR_PixeurToMaterials

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PixeurToMaterials
Version: 1.0
Description-US: Create materials from Pixeur color palette file

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d import storage as s

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select pixeur palette',c4d.FILESELECT_LOAD,'') # File dialog
    if fn is None: return # If no file, exit
    f = open(fn.decode("utf-8")) # Open file and read it in UTF-8
    try: # Try to execute following script
        for line in f: # Loop trhough lines in Pixeur color palette file
            if line.startswith("R"): # If line starts with letter R
                line = line.split(" ") # Split line to list
                r = line[0][2:] # Red channel value
                g = line[1][2:] # Green channel value
                line = line[2].split(",") # Split line new list
                b = line[0][2:] # Blue channel value
                mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize new material
                color = c4d.Vector(float(r)/255,float(g)/255,float(b)/255) # Convert rgb colors to c4d format
                mat[c4d.MATERIAL_COLOR_COLOR] = color # Set color channel color
                mat[c4d.MATERIAL_LUMINANCE_COLOR] = color # Set luminance channel color
                doc.InsertMaterial(mat) # Insert material to document
                doc.AddUndo(c4d.UNDOTYPE_NEW, mat) # Add undo command for inserting new material
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()