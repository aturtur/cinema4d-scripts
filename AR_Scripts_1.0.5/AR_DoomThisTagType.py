"""
AR_DoomThisTagType

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DoomThisTagType
Version: 1.0
Description-US: Removes selected tag type from selected objects.
If there is no object selection, tag type will be doomed in whole project.
Note: Select object, select tag and run the script¨.

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

def IterateHierarchy(op, theTag, sel):
    """
    Returns true if the given operation.

    Args:
        op: (todo): write your description
        theTag: (todo): write your description
        sel: (todo): write your description
    """
    if op is None:
        return
    while op:
        if sel == True:
            if op.GetBit(c4d.BIT_ACTIVE) == 1: # If object is active
                tags = op.GetTags() # Get tags of object
                for t in tags: # Loop Through tags
                    if t.GetType() == theTag.GetType():
                        doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                        t.Remove() # Remove tag
            op = GetNextObject(op)
        elif sel == False:
            tags = op.GetTags() # Get tags of object
            for t in tags: # Loop Through tags
                if t.GetType() == theTag.GetType():
                    doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Add undo command for removing tag
                    t.Remove() # Remove tag
            op = GetNextObject(op)
    return True

def main():
    """
    Main entry point.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag, c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag, c4d.modules.character.CAWeightTag,
    c4d.VariableTag, c4d.modules.graphview.XPressoTag, c4d.VertexColorTag, c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags
    try: # Try to execute following script
        selection = doc.GetSelection() # Get active selection
        activeObjects = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active objects
        if activeObjects:
            sel = True  # There is object selection
        elif not activeObjects:
            sel = False # No object selection
        for s in selection : # Loop through selection
            if type(s) in commonTags: # If selected item is a tag
                theTag = s # Selected tag type is doomed
        start_object = doc.GetFirstObject() # Get first object
        IterateHierarchy(start_object, theTag, sel) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()