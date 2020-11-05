"""
AR_RemoveTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveTags
Version: 1.0
Description-US: Removes all tags. If object(s) selected removes tags only from selected object(s)

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def GetNextObject(op):
    """
    Returns the next op.

    Args:
        op: (todo): write your description
    """
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def RemoveTags(op, selection):
    """
    Removes all tags from the given op.

    Args:
        op: (todo): write your description
        selection: (str): write your description
    """
    if op is None:
        return
    while op:
        tags = op.GetTags() # Get tags of object
        if selection:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Tag types that you dont wan't to delete
                for t in tags: # Loop Through tags
                    if type(t) not in hiddenTags: # If not protected tag type
                        doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                        t.Remove() # Remove tag
        else:
            hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Tag types that you dont wan't to delete
            for t in tags: # Loop Through tags
                if type(t) not in hiddenTags: # If not protected tag type
                    doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                    t.Remove() # Remove tag
        op = GetNextObject(op)
    return True

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
    try: # Try to execute following script
        start_object = doc.GetFirstObject() # Get first object
        if len(selection) != 0:
            RemoveTags(start_object, True) # Do the thing
        else:
            RemoveTags(start_object, False) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
  
# Execute main()
if __name__=='__main__':
    main()