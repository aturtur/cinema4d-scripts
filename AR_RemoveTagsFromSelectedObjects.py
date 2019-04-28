"""
AR_RemoveTagsFromSelectedObjects

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveTagsFromSelectedObjects
Description-US: Removes all tags from selected objects
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def IterateHierarchy(op):
    if op is None:
        return
    while op:
        if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
            tags = op.GetTags() # Get tags of object
            hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Tag types that you dont wan't to delete
            for t in tags: # Loop Through tags
                if type(t) not in hiddenTags: # If not protected tag type
                    doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                    t.Remove() # Remove tag
        op = GetNextObject(op)
    return True

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        start_object = doc.GetFirstObject() # Get first object
        IterateHierarchy(start_object) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
  
# Execute main()
if __name__=='__main__':
    main()