"""
AR_CreateStickyNullsFromObjects

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateStickyNullsFromObjects
Description-US: Create null objects with constraint tag (PSR) from selected object(s)
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import utils as u

# Functions
def GetGlobalPosition(obj): # Get object's global position
    return obj.GetMg().off

def GetGlobalRotation(obj): # Get object's global rotation
    return u.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj): # Get object's global scale
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalPosition(obj, pos): # Set object's global position
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot): # Set object's global rotation
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector(m.v1.GetLength(),
                       m.v2.GetLength(),
                       m.v3.GetLength())
    m = u.HPBToMatrix(rot)
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SetGlobalScale(obj, scale): # Set object's global scale
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def CreateNulls(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    try: # Try to execute following script
        objectNull = c4d.BaseObject(c4d.Onull) # Initialize null object
        objectNull.SetName(str(obj.GetName()) + " Points") # Set null's name
        objectNull[c4d.NULLOBJECT_DISPLAY] = 14 # Set null's display mode to none
        SetGlobalPosition(objectNull,GetGlobalPosition(obj)) # Set global position, rotation and scale
        SetGlobalRotation(objectNull,GetGlobalRotation(obj))
        SetGlobalScale(objectNull,GetGlobalScale(obj))
        doc.InsertObject(objectNull) # Insert null to document
        objectNull.SetName(obj.GetName()+"_Null") # Set null's name
        objectNull[c4d.NULLOBJECT_DISPLAY] = 2 # Set null's display mode circle
        objectNull.InsertTag(c4d.BaseTag(1019364)) # Insert constraint tag to null
        tag = objectNull.GetFirstTag() # Select constraint tag
        tag[c4d.ID_CA_CONSTRAINT_TAG_PSR] = 1 # Activate PSR constraint
        tag[10001] = obj # Set Target        
        doc.AddUndo(c4d.UNDOTYPE_NEW, objectNull) # Add undo command for adding new object
    except: # If something went wrong
        pass # Do nothing

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
    for obj in selection: # Loop through selected items
        CreateNulls(obj) # Run CreateNulls function
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()