"""
AR_RemoveTextureTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveTextureTags
Version: 1.0
Description-US: If there is no selected objects, script will remove every texture tags. If there is selected object(s), script will remove texture tags from selected object(s).

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
 
def RemoveAll(op):
    """
    Removes all of the given a op.

    Args:
        op: (todo): write your description
    """
    if op is None:
        return
    while op:
        tags = op.GetTags() # Get tags of object
        for t in tags: # Loop Through tags
            if t.GetType() == 5616: # If tag is texture tag
                doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                t.Remove() # Remove tag
        op = GetNextObject(op)
    return True

def RemoveSelected(op):
    """
    Removes op.

    Args:
        op: (todo): write your description
    """
    if op is None:
        return
    while op:
        if op.GetBit(c4d.BIT_ACTIVE) == True: # If object is selected
            tags = op.GetTags()
            for t in tags:
                if t.GetType() == 5616:
                    doc.AddUndo(c4d.UNDOTYPE_DELETE, t)
                    t.Remove()
        op = GetNextObject(op)
    return True

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get object selection
        start_object = doc.GetFirstObject() # Get first object
        if selection == []: # If there is no selected objects        
            RemoveAll(start_object) # Do the thing
        else:
            RemoveSelected(start_object) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
  
# Execute main()
if __name__=='__main__':
    main()