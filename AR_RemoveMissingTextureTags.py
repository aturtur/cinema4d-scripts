"""
AR_RemoveMissingTextureTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveMissingTextureTags
Description-US: Removes texture tags that does not have assigned material
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
        tags = op.GetTags() # Get tags of object
        for t in tags: # Loop Through tags
            if t.GetType() == 5616: # If tag is texture tag
                if t[c4d.TEXTURETAG_MATERIAL] == None: # If tag doesn't have material
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