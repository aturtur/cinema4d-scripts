"""
AR_MatMerge

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MatMerge
Version: 1.0.0
Description-US: Merges materials with the same name.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (14.04.2022) - Initial version
"""

# Libraries
import c4d, re

# Classes
class matObject:
    matList = []    
    def __init__(self, name):
        self.name = name
        self.mats = []
        matObject.matList.append(self)
    def addMat(self, newMat):
        self.mats.append(newMat)

# Functions
def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectTextureTags(op):
    tTags = []
    if op is None:
        return
    while op:
        tags = op.GetTags()
        for t in tags:
            if t.IsInstanceOf(c4d.Ttexture):
                tTags.append(t)
        op = GetNextObject(op)
    return tTags

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    
    # Collect materials
    matObjs = {}
    for i, m in enumerate(materials): # Iterate through materials
        name = re.split("\\.\\d$", m.GetName())[0] # Get name of the material
        if name not in matObjs: # If material name not already in matObjs list
            matObjs[name] = matObject(name) # Create a new material
        matObjs[name].addMat(m) # Add material to the material object
    
    # Assign new materials
    tTags = CollectTextureTags(doc.GetFirstObject()) # Collect all texture tags 
    for t in tTags: # Iterate through texture tags
        mat = t[c4d.TEXTURETAG_MATERIAL] # Get material of the texture tag
        for m in matObjs: # Iterate through material objects
            if matObjs[m].name == re.split("\\.\\d$", mat.GetName())[0]:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, t) # Record undo
                t[c4d.TEXTURETAG_MATERIAL] = matObjs[m].mats[0] # Set new material
        
    # Deleting materials
    for m in matObjs: # Iterate through material objects
        cnt = len(matObjs[m].mats) # Get count of materials
        for i in range(1, cnt): # Iterate through materials, skipping first one
            mat = matObjs[m].mats[i] # Get the material
            doc.AddUndo(c4d.UNDOTYPE_DELETE, mat) # Record undo
            mat.Remove() # Detele material

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()