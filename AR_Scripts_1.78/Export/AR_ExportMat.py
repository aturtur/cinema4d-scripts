"""
AR_ExportMat

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ExportMat
Version: 1.2.0
Description-US: Exports selected material(s) to own c4d-file(s)

Note: Material names should NOT end with dot and number! Eg. "MyMaterial.1" rename that to "MyMaterial_1"
      or something different. Currently the script does not copy textures to the export location, use global paths!

Written for Maxon Cinema 4D 2023.0.1
Python version 3.9.1

Change log:
1.2.0 (14.12.2023) - Exports with current render settings
1.1.0 (20.11.2022) - Progress bar
1.0.0 (01.11.2022) - Initial realease
"""

# Libraries
import c4d
import os
from c4d import documents
from c4d import storage
from c4d import utils as u

# Functions
def ExportMaterial(material, fn):
    tempDoc = documents.BaseDocument() # Initialize a temporary document
    
    renderData = doc.GetActiveRenderData() # Get document render data
    copyRenderData = renderData.GetClone() # Get clone of render data
    tempDoc.InsertRenderData(renderData.GetClone(), None, None) # Insert new render data to document
    tempDoc.SetActiveRenderData(copyRenderData) # Set new render data to active

    tempDoc.InsertMaterial(material, pred = None, checknames = True) # Insert material to temporary document
    matName = material.GetName() # Get material's name
    path = fn+os.sep+matName+".c4d" # File path
    documents.SaveDocument(tempDoc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT) # Export C4D-file    
    documents.KillDocument(tempDoc) # Kill the temporary document

def main():
    materials = doc.GetMaterials() # Get materials
    if len(materials) == 0: return false # If no any materials, stop the script

    selectedMaterials = [] # Init an array for selected materials3
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
            selectedMaterials.append(m) # Add material to selectedMaterials list

    if len(selectedMaterials) == 0: return False # If no selected materials, stop the script

    fn = storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Folder to export", c4d.FILESELECT_DIRECTORY) # Folder path
    if not fn: return False # If cancelled, stop the script

    counter = 0 # Initialize a counter variable
    for i, s in enumerate(selectedMaterials): # Iterate through selectedmaterials
        progress = u.RangeMap(i, 0, len(selectedMaterials), 0, 100, True)
        c4d.StatusSetText("Exporting %s of %s" % (i,len(selectedMaterials)))
        c4d.StatusSetBar(progress)
        c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_STATICBREAK)
        matClone = s.GetClone()  # Get clone of the material
        ExportMaterial(matClone, fn) # Export material to own file
        c4d.GeSyncMessage(c4d.EVMSG_UPDATEBASEDRAW)
        counter = counter + 1
    
    #print(str(counter) + " material(s) exported to: " + fn) # Print some info
    c4d.StatusClear() # Clear status

# Execute the main function
if __name__ == '__main__':
    main()