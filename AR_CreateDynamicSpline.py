"""
AR_CreateDynamicSpline

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateDynamicSpline
Description-US: Creates a dynamic spline between two selected objects
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import utils as u

# Global variables
interpolation = 8 # Points in one spline 'segment' (from object a to b) (min value = 2)

# Functions
def CenterAxis(obj): # Center object's axis
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = [] # Initialize empty list
    pointCount = obj.GetPointCount() # Get object's point count
    for i in range(0, pointCount): # Loop through points
        points.append(obj.GetPoint(i)) # Add point to points list
    matrix = obj.GetMg() # Get object's global matrix
    axis = obj.GetAbsPos() # Get object's absolute position
    center = obj.GetMp() # Get Object's bounding box center in local space
    difference = axis - (axis + center) # Calculate difference
    if difference != c4d.Vector(0): # If there is a difference
        for i in xrange(pointCount): # Loop through object's points
            obj.SetPoint(i, points[i] + difference) # Set new point position
        obj.Message(c4d.MSG_UPDATE) # Send update message
        obj.SetMg(c4d.Matrix((matrix * center),
            matrix.v1, matrix.v2, matrix.v3)) # Set new matrix for the object

def CreateSpline(interpolation = 2):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active object selection (selection order enabled)
    positions = [] # Initialize empty list for objects' positions
    points = [] # Initialize empty list for spline points
    if interpolation < 2: interpolation = 2 # If too few points, fix it
    try: # Try to execute following script
        for obj in selection: # Loop through object in selection
            pos = obj.GetMg().off # Get objects global position
            positions.append(pos) # Insert object's position to position list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager
        pointCount = interpolation*(len(positions)-1) # Calculate point count
        for x in range(0, len(positions)-1): # Loop through
            for i in range(0, interpolation): # Loop through
                step = 1.0/float((interpolation-1.0)) # Calculate new step for point
                point = u.MixVec(positions[x],positions[x+1],step*float(i)) # Calculate point position
                points.append(point) # Insert point position to points list
        spline = c4d.SplineObject(pointCount, c4d.SPLINETYPE_LINEAR) # Initialize spline object
        spline.SetAllPoints(points) # Set spline points from points list
        doc.InsertObject(spline) # Insert spline object to document
        doc.AddUndo(c4d.UNDOTYPE_NEW, spline) # Add undo command for creating new object
        spline[c4d.SPLINEOBJECT_TYPE] = 3 # Set spline's type to B-Spline
        spline[c4d.SPLINEOBJECT_INTERPOLATION] = 2 # Set spline's interpolation to Uniform
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, spline) # Add undo command for making changes to spline object
        CenterAxis(spline) # Center spline's axis
        splinePointsCount = len(spline.GetAllPoints()) # Get spline point count
        pointSelection = spline.GetPointS() # Get spline point selection
        # Point A
        pointSelection.DeselectAll() # Deselect all spline points
        pointSelection.Select(0) # Select spline's first point
        objectA = selection[0] # First object
        constraintTagA = spline.MakeTag(1018074) # Create hair constraint tag
        constraintTagA[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = objectA # Set link
        doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
        c4d.CallButton(constraintTagA, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR) # Press 'Set' button
        c4d.EventAdd() # Refresh Cinema 4D
        # Point B
        pointSelection.DeselectAll() # Deselect all spline points
        pointSelection.Select(splinePointsCount-1) # Select spline's first point
        objectB = selection[1] # Second object
        constraintTagB = spline.MakeTag(1018074) # Create hair constraint tag
        constraintTagB[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = objectB # Set link
        doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
        c4d.CallButton(constraintTagB, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR) # Press 'Set' button
        c4d.EventAdd() # Refresh Cinema 4D
        # Rest of the stuff
        spline.InsertTag(c4d.BaseTag(1018068)) # Insert spline dynamics tag
        doc.AddUndo(c4d.UNDOTYPE_BITS, spline) # Add undo command for changing bits
        spline.SetBit(c4d.BIT_ACTIVE) # Select spline object in Object Manager
        c4d.CallCommand(14039) # Optimize, remove overlapping points
    except: # If something went wrong
        pass # Do nothing

def main():
    global interpolation # Access to global variable
    doc.StartUndo() # Start recording undos
    CreateSpline(interpolation) # Run create spline function
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__ == "__main__":
    main()