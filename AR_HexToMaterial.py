"""
AR_HexToMaterial

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_HexToMaterial
Description-US: Create material from hex color value
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import gui

# Functions
def HexToRgb(value):
    value = value.lstrip('#') # Strip '#' symbol from value
    lv = len(value) # Length of the input
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        hexcolor = c4d.gui.InputDialog("Hex Color") # Get user input hex color value
        rgb = HexToRgb(hexcolor) # Convert hex to rgb values
        color = c4d.Vector(float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255) # Convert rgb to c4d form
        mat = c4d.BaseMaterial(c4d.Mmaterial) # Initialize material
        mat[c4d.MATERIAL_COLOR_COLOR] = color # Set color channel color
        mat[c4d.MATERIAL_LUMINANCE_COLOR] = color # Set luminance channel color
        mat.SetName(str(hexcolor)) # Set material name
        doc.InsertMaterial(mat) # Insert material to active document
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat) # Add undo command for adding new material
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()