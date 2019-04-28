"""
AR_CreateNulls

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateNulls
Description-US: Create null objects from selected points
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
        points = obj.GetPointS() # Get object's points
        pointCount = obj.GetPointCount() # Get point count of object
        parentNull = c4d.BaseObject(c4d.Onull) # Initialize parent null object
        parentNull.SetName(str(obj.GetName()) + " Points") # Set parent null's name
        parentNull[c4d.NULLOBJECT_DISPLAY] = 14 # Set parent null's display mode to none
        SetGlobalPosition(parentNull,GetGlobalPosition(obj)) # Set global position, rotation and scale
        SetGlobalRotation(parentNull,GetGlobalRotation(obj))
        SetGlobalScale(parentNull,GetGlobalScale(obj))
        doc.InsertObject(parentNull) # Insert parent null to document

        for i in range(pointCount): # Loop through points
            if(points.IsSelected(i)): # If point is selected
                pointNull = c4d.BaseObject(c4d.Onull) # Initialize point null object
                pointNull.SetName("Point "+str(i)) # Set point null's name
                pointNull[c4d.NULLOBJECT_DISPLAY] = 2 # Set point null's display mode circle
                pointNull.SetAbsPos(obj.GetPoint(i)) # Set null's position
                pointNull.InsertUnderLast(parentNull) # Insert point null last object under parent null
                doc.AddUndo(c4d.UNDOTYPE_NEW, parentNull) # Add undo command for adding new object
    except: # If something went wrong
        pass # Do nothing

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active selection
    for obj in selection: # Loop through selected items
        CreateNulls(obj) # Run CreateNulls function
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()