"""
AR_RandomlyPutSelectedMaterialsToSelectedObjects

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RandomlyPutSelectedMaterialsToSelectedObjects
Description-US: Script randomly assigns selected materials to selected objects
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
import random as rnd

# Functions
def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get selected objects
    materials = doc.GetActiveMaterials() # Get selected materials
    for s in selection: # Loop through selected objects
        texTag = c4d.BaseTag(5616) # Initialize texture tag
        texTag[c4d.TEXTURETAG_MATERIAL] = materials[rnd.randint(0,len(materials))-1] # Set random material to texture tag
        s.InsertTag(texTag) # Insert tag to objects
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag) # Add undo command for inserting a new tag
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()
