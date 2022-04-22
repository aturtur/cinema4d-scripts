"""
AR_PointCloud

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PointCloud
Version: 1.0.0
Description-US: Creates point cloud from selected objects' positions

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.0 (25.03.2021) - First version
"""

# Libraries
import c4d

# Main function
def main():
    doc.StartUndo() # Start recording undos
    
    positions = [] # Init list for positions
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get selected objects
    cnt = len(selection) # Count of objects
    if cnt == 0: return # Break if no selected objects    
    for s in selection: # Iterate through selected objects
        positions.append(s.GetMg().off) # Get object's position and put it to the list
    
    polygon = c4d.PolygonObject(cnt, 0) # Init a polygon object
    polygon.SetAllPoints(positions) # Set points
    polygon.SetName("PointCloud") # Set name
    
    doc.InsertObject(polygon) # Insert polygon object to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, polygon) # Record undo step
    
    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()