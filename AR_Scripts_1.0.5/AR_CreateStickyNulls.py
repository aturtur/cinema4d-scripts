"""
AR_CreateStickyNulls

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateStickyNulls
Version: 1.0
Description-US: Creates null objects with constraint tag (clamp) from selected point(s) or creates null objects with constraint tag (PSR) from selected object(s)

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
import math
from c4d import utils as u

# Functions
def GetGlobalPosition(obj): # Get object's global position
    """
    Return the position of the given object.

    Args:
        obj: (todo): write your description
    """
    return obj.GetMg().off

def GetGlobalRotation(obj): # Get object's global rotation
    """
    Returns the rotation object.

    Args:
        obj: (todo): write your description
    """
    return u.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj): # Get object's global scale
    """
    Return a vector object.

    Args:
        obj: (todo): write your description
    """
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalPosition(obj, pos): # Set object's global position
    """
    Sets position.

    Args:
        obj: (todo): write your description
        pos: (int): write your description
    """
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot): # Set object's global rotation
    """
    Sets the rotation matrix.

    Args:
        obj: (todo): write your description
        rot: (todo): write your description
    """
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
    """
    Sets scale scale.

    Args:
        obj: (todo): write your description
        scale: (float): write your description
    """
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def CreateNullsFromPoints(obj):
    """
    Creates a list.

    Args:
        obj: (todo): write your description
    """
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
                pointNull.InsertTag(c4d.BaseTag(1019364)) # Insert constraint tag to point null
                tag = pointNull.GetFirstTag() # Select constraint tag
                tag[c4d.ID_CA_CONSTRAINT_TAG_CLAMP] = 1 # Set constraint tag's mode to clamp
                tag[50004,1] = 3 # Set To Point
                tag[50004,4] = 3 # Set Align Y+
                tag[50001] = obj # Set Target obj
                tag[50004,7] = 1 # Set Lock Position
                pointNull.InsertUnderLast(parentNull) # Insert point null last object under parent null
                doc.AddUndo(c4d.UNDOTYPE_NEW, parentNull) # Add undo command for adding new object
                pointNull.SetBit(c4d.BIT_ACTIVE)
    except: # If something went wrong
        pass # Do nothing

def CreateNullsFromObjects(obj):
    """
    Creates a circle object from an object.

    Args:
        obj: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    try: # Try to execute following script
        objectNull = c4d.BaseObject(c4d.Onull) # Initialize null object
        SetGlobalPosition(objectNull,GetGlobalPosition(obj)) # Set global position, rotation and scale
        SetGlobalRotation(objectNull,GetGlobalRotation(obj))
        SetGlobalScale(objectNull,GetGlobalScale(obj))
        doc.InsertObject(objectNull) # Insert null to document
        objectNull.SetName(obj.GetName()+"_Null") # Set null's name
        objectNull[c4d.NULLOBJECT_DISPLAY] = 2 # Set null's display mode circle

        bbox = obj.GetRad()
        sizes = [bbox.x, bbox.y, bbox.z]
        sizes.sort()
        width = sizes[-1]
        height = sizes[-2]
        diagonal = math.sqrt(pow((width*2), 2) + pow((height*2), 2))
        radius = diagonal / 2    
        objectNull[c4d.NULLOBJECT_RADIUS] = radius

        objectNull.InsertTag(c4d.BaseTag(1019364)) # Insert constraint tag to null
        tag = objectNull.GetFirstTag() # Select constraint tag
        tag[c4d.ID_CA_CONSTRAINT_TAG_PSR] = 1 # Activate PSR constraint
        tag[10001] = obj # Set Target        
        doc.AddUndo(c4d.UNDOTYPE_NEW, objectNull) # Add undo command for adding new object
        objectNull.SetBit(c4d.BIT_ACTIVE)

    except: # If something went wrong
        pass # Do nothing

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    editorMode = doc.GetMode() # Get editor's active mode
    if editorMode == c4d.Mpoints: # # If Point mode is activated
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active selection
        for obj in selection: # Loop through selected items
            CreateNullsFromPoints(obj) # Run CreateNulls function
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
            obj.DelBit(c4d.BIT_ACTIVE)
    else:
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
        for obj in selection: # Loop through selected items
            CreateNullsFromObjects(obj) # Run CreateNulls function
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
            obj.DelBit(c4d.BIT_ACTIVE)
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()