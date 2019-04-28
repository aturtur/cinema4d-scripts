"""
AR_SelectSameMaterialTextureTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectSameMaterialTextureTags
Description-US: Select texture tag and run the script and texture tags with same material will be selected
Written for Maxon Cinema 4D R20.057
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
 
def IterateHierarchy(op, s):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    if op is None:
        return 
    while op: # While there is an object
        material = s[c4d.TEXTURETAG_MATERIAL] # Selected tag's material'
        tags = op.GetTags() # Get tags
        for t in tags: # Loop through tags
            if type(t) is c4d.TextureTag: # If tag is texture tag
                if t[c4d.TEXTURETAG_MATERIAL] == material: # If tag has same material as selected tag
                    doc.AddUndo(c4d.UNDOTYPE_BITS, t) # Add undo command for changing bits
                    t.SetBit(c4d.BIT_ACTIVE) # Set tag active
        op = GetNextObject(op) # Get next object
    return True

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos    
    selection = doc.GetSelection() # Get active selection
    start_object = doc.GetFirstObject() # Get first object in document
    for s in selection: # Loop through selected items
        if type(s) is c4d.TextureTag: # If selected item is texture tag
            IterateHierarchy(start_object, s) # Do the thing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()