"""
AR_Guide

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Guide
Version: 1.0.1
Description-US: Creates a guide object from two selected objects, points or edge.

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (09.10.2021) - Updated to R25, fixed some bugs, added support for edge selection
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

def GetPointsPositions(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = obj.GetPointS() # Get object's points
    pointCount = obj.GetPointCount() # Get point count of object
    positions = [] # Initialize a list for point positions

    for i in range(pointCount): # Loop through points
        if(points.IsSelected(i)): # If point is selected
            pointPosition = obj.GetPoint(i) # Get point's position
            marr = c4d.Matrix() # Initialize a matrix
            marr.off = pointPosition # Set matrix position
            marr = obj.GetMg() * marr # Calculate global matrix
            positions.append(marr.off) # Add point position to the list

    return positions # Return collected point positions

def GetObjectsPositions(selection):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selection = doc.GetActiveObjects(1) # Get selected objects
    positions = [selection[0].GetMg().off, selection[1].GetMg().off] # Positions
    return positions # Return collected object positions

def GetPointsFromEdge(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document

    edgeS = obj.GetEdgeS() # Get selected edges
    maxEdgeCnt = obj.GetPolygonCount()*4 # Get maximum edge count
    edgeId = [] # Initialize a list for edge indecies
    for i in range(maxEdgeCnt): # Iterate through edges
        if edgeS.IsSelected(i): # If edge is selected
            edgeId.append(i) # Add to the list
    polygons = obj.GetAllPolygons()
    pointS = c4d.BaseSelect()
    pointId = []
    for edge in edgeId: # Iterate through stored edges
        polyId = int(edge/4)
        polyEdgeId = edge-4*(polyId)
        polygon = polygons[polyId]

        if polyEdgeId == 0:
            pointS.Select(polygon.a)
            pointS.Select(polygon.b)

        elif polyEdgeId == 1:
            pointS.Select(polygon.b)
            pointS.Select(polygon.c)

        elif polyEdgeId == 2:
            pointS.Select(polygon.c)
            pointS.Select(polygon.d)

        elif polyEdgeId == 3:
            pointS.Select(polygon.d)
            pointS.Select(polygon.a)
    
    pointS.CopyTo(obj.GetPointS())
    CreateGuide(GetPointsPositions(obj))

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    editorMode = doc.GetMode() # Get editor's active mode
    defaultGuide = [c4d.Vector(0,0,-100), c4d.Vector(0,0,100)] # Initialize a default guide positions
    selection = doc.GetActiveObjects(1) # Get selected objects

    try: # Try to execute following script

        if editorMode == c4d.Mpoints: # If 'Point' mode is activated
            if len(selection) != 0: # If there are an object selected
                if len(selection) > 1:
                    allPoints = []
                    for s in selection:
                        allPoints = allPoints + (GetPointsPositions(s))
                    CreateGuide(allPoints)
                else:
                    CreateGuide(GetPointsPositions(selection[0]))
            else: # Otherwise
                CreateGuide(defaultGuide) # Create guide to origin
    
        elif editorMode == c4d.Medges: # If 'Edge' mode is activated
            GetPointsFromEdge(selection[0])
    
        else:
            if len(selection) > 1: # If there are more than one selected object
                CreateGuide(GetObjectsPositions(selection))
            else:
                CreateGuide(defaultGuide) # Create guide to origin
    
        doc.EndUndo() # Stop recording undos
        c4d.EventAdd() # Refresh Cinema 4D
    
    except: # If something geos wrong
        pass # Do nothing

# Execute main()
if __name__=='__main__':
    main()