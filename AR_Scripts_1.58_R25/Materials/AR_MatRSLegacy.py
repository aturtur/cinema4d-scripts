"""
AR_MatRSLegacy

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MatRSLegacy
Version: 1.0.0
Description-US: Creates Redshift material that uses old Redshift Shader Graph

Note: Requires Cinema 4D R26!

Written for Maxon Cinema 4D R26.013
Python version 3.9.1

Change log:
1.0.0 (20.04.2022) - Initial version
"""

# Libraries
import c4d
import redshift

# Functions
def main():
    doc.StartUndo() # Start recording undos
    material = c4d.BaseMaterial(1036224) # Initialize legacy Redshift material
    material.SetName("RS Material") # Set material name
    doc.InsertMaterial(material, checknames=True) # Add material to the document
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, material) # Record undo for creating the material

    # Redshift stuff
    rsnm = redshift.GetRSMaterialNodeMaster(material) # Get Redshift material node master
    root = rsnm.GetRoot() # Get node master root
    outputNode = root.GetChildren()[0] # Get output node
    inputPort = outputNode.GetInPorts()[0] # Get input port
    newNode = rsnm.CreateNode(root, 1036227, None, x = 150, y = 300) # Create a redshift node (RS)
    newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "Material" # Set node type
    newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.529, 0.345, 0.333) # Set node color
    newNode.GetOutPort(0).Connect(inputPort) # Connect ports

    # Selecting and deselecting
    mats = doc.GetMaterials() # Get all materials
    for m in mats: # Iterate through materials
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, m) # Record undo for deselecting
        m.DelBit(c4d.BIT_ACTIVE) # Deselect
    material.SetBit(c4d.BIT_ACTIVE) # Select new material

    doc.EndUndo() # Stop recording undos
    doc.EnetAdd() # Update Cinema 4D

if __name__ == '__main__':
    main()