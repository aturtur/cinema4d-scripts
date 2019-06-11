"""
AR_AxisCenter
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AxisCenter
Description-US: Creates setup with voronoi fracture and connectors for selected cloner
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def CenterAxis(obj): # Center object's axis
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = [] # Initialize empty list
    pointCount = obj.GetPointCount() # Get object's point count
    for i in range(0, pointCount): # Loop through points
        points.append(obj.GetPoint(i)) # Add point to points list
    matrix = obj.GetMg() # Get object's global matrix
    center = obj.GetMp() # Get Object's bounding box center in local space
    axis = obj.GetAbsPos() # Get object's absolute position
    difference = axis - (axis + center) # Calculate difference
    if difference != c4d.Vector(0): # If there is a difference
        for i in xrange(pointCount): # Loop through object's points
            obj.SetPoint(i, points[i] + difference) # Set new point position
        obj.Message(c4d.MSG_UPDATE) # Send update message
        obj.SetMg(c4d.Matrix((matrix * center),
            matrix.v1, matrix.v2, matrix.v3)) # Set new matrix for the object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    flag = c4d.GETACTIVEOBJECTFLAGS_NONE # Only the topmost parent of each chain is added
    selection = doc.GetActiveObjects(flag) # Get active objects
    for obj in selection: # Loop through selection
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Add undo command for making changes to object
        CenterAxis(obj) # Center spline's axis
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
main()