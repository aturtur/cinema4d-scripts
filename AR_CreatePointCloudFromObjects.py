"""
AR_CreatePointCloudFromObjects

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreatePointCloudFromObjects
Description-US: Create point cloud from selected objects
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        points = [] # Initialize empty list for points
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active object selection (selection order enabled)
        for obj in selection: # Loop through selection
            mat = obj.GetMg() # Get object's matrix
            pos = mat.off # Get object's position
            points.append(pos) # Add point to points list
        poly = c4d.PolygonObject(len(points), 0) # Initialize polygon object
        poly.SetAllPoints(points) # Set all points to polygon object
        doc.InsertObject(poly) # Insert polygon object to document
        doc.AddUndo(c4d.UNDOTYPE_NEW, poly) # Add undo command for adding new polygon object
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()