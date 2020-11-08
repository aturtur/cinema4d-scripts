"""
AR_CreateGuide

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateGuide
Version: 1.0
Description-US: Creates a guide object from two selected objects or points.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
import math
from c4d import utils as u

# Functions
def CreateGuide(positions):
    guide = c4d.BaseObject(1027657) # Initialize a guide object
    doc.InsertObject(guide) # Insert guide object to the document
    doc.AddUndo(c4d.UNDOTYPE_NEW, guide) # Record undo
    midPosition = u.MixVec(positions[0], positions[1], 0.5) # Get position between poitns
    guide.SetAbsPos(midPosition) # Set position
    
    # Single out position components
    x1 = positions[0].x
    x2 = positions[1].x
    y1 = positions[0].y
    y2 = positions[1].y
    z1 = positions[0].z
    z2 = positions[1].z
    
    directionVector = c4d.Vector((x2 - x1), (y2 - y1), (z2 - z1)) # Calculate direction vector
    normalVector = directionVector.GetNormalized() # Normalize the direction vector
    hpb = u.VectorToHPB(normalVector) # Convert vector to HPB
    
    guide[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = hpb.x
    guide[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = hpb.y
    guide[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z] = hpb.z
    guide[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Set display color: "On"
    guide[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(140.0/255.0, 203.0/255.0, 1) # Set color

def CreateGuideFromPoints(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = obj.GetPointS() # Get object's points
    pointCount = obj.GetPointCount() # Get point count of object
    positions = [] # Initialize a list for point positions
    for i in range(pointCount): # Loop through points
        if(points.IsSelected(i)): # If point is selected
            pointPosition = obj.GetPoint(i) # Get point's position
            marr = c4d.Matrix() # Initialize a matrix
            marr.off = pointPosition # Set matrix position
            marr = op.GetMg() * marr # Calculate global matrix
            positions.append(marr.off) # Add point position to the list
    CreateGuide(positions) # Create the guide
    
def CreateGuideFromObjects(selection):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selection = doc.GetActiveObjects(1) # Get selected objects
    positions = [selection[0].GetMg().off, selection[1].GetMg().off] # Positions
    CreateGuide(positions) # Create the guide

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    editorMode = doc.GetMode() # Get editor's active mode
    if editorMode == c4d.Mpoints: # # If Point mode is activated
        if op != None: # If there are an object selected
            CreateGuideFromPoints(op)
        else: # Otherwise
            CreateGuide([c4d.Vector(0,0,-100), c4d.Vector(0,0,100)]) # Create guide to origin
    else:
        selection = doc.GetActiveObjects(1) # Get selected objects
        if len(selection) > 1: # If there are more than one selected object
            CreateGuideFromObjects(selection)
        else:
            CreateGuide([c4d.Vector(0,0,-100), c4d.Vector(0,0,100)]) # Create guide to origin
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()