"""
AR_MatSelectPrev

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MatSelectPrev
Version: 1.0.0
Description-US: Select previous material

Note: Does not support layer filtering!

Written for Maxon Cinema 4D 2024.1.0
Python version 3.11.4

Change log:
1.0.0 (26.11.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def main():
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get all materials
    selectedMaterials = [] # Initialize a list for selected materials
    for material in materials: # Iterate through materials
        if material.GetBit(c4d.BIT_ACTIVE): # If material is selected
            selectedMaterials.append(material) # Add material to selected materials list
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, material) # Record undo
            material.DelBit(c4d.BIT_ACTIVE) # Deselect material

    for material in selectedMaterials: # Iterate through selected materials
        prevMaterial = material.GetPred() # Get previous material
        if prevMaterial != None: # If there's an previous material
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, prevMaterial) # Record undo
            prevMaterial.SetBit(c4d.BIT_ACTIVE) # Select material

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main
if __name__ == '__main__':
    main()