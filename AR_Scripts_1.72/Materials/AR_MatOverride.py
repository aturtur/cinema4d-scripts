"""
AR_MatOverride

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MatOverride
Version: 1.0.0
Description-US: Overrides selected materials with the top of the list selected material

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.0.0 (28.03.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectMaterialTags(op, material):
    materialTags = []
    if op is None:
        return
    while op:
        tags = op.GetTags()
        for t in tags:
            if t.GetType() == 5616: # Material tag
                if t[c4d.TEXTURETAG_MATERIAL] == material:
                    materialTags.append(t)
        op = GetNextObject(op)
    return materialTags

def main():
    doc.StartUndo()
    materials = doc.GetMaterials()
    selected = []
    
    # Collect materials
    for m in materials:
        if m.GetBit(c4d.BIT_ACTIVE) == True:
            selected.append(m)
    
    # Get texture tags
    startObj = doc.GetFirstObject()
    MaterialTags = []
    for s in selected:
        MaterialTags.extend(CollectMaterialTags(startObj, s))

    # Assign the first material to all material tags
    mat = selected[0]
    for t in MaterialTags:
        doc.AddUndo(c4d.UNDO_CHANGE, t)
        t[c4d.TEXTURETAG_MATERIAL] = mat
    
    # Delete materials
    for i in range(1,len(selected)):
        doc.AddUndo(c4d.UNDOTYPE_DELETEOBJ, selected[i])
        selected[i].Remove()
        
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()