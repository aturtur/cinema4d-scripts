"""
AR_AddPhongTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AddPhongTags
Version: 1.0
Description-US: Adds phong tags to objects if missing

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

def CheckPhong(op, doc):
    """
    Checks that the given tag is a binary document.

    Args:
        op: (todo): write your description
        doc: (todo): write your description
    """
    phongFound = 0 # Initialize phongFound variable
    tags = op.GetTags() # Get tags of object
    for t in tags: # Loop Through tags
        if t.GetType() == 5612: # If tag is a phong tag
            phongFound = 1 # Phong tag found
    if phongFound == 0: # If phong tag is not found
        phongObjects = [5125, 1039861, 5173, 5169, 5166, 5161, 5167, 5165, 5172, 5171,
        5163, 5160, 5174, 5168, 5164, 5170, 5162, 5159, 5100] # Objects that uses phong tag
        if op.GetType() in phongObjects: # If object is in phongObjects list
            phongTag = c4d.BaseTag(5612) # Initialize phong tag
            phongTag[c4d.PHONGTAG_PHONG_ANGLELIMIT] = 1 # Set angle limit on
            phongTag[c4d.PHONGTAG_PHONG_ANGLE] = c4d.utils.DegToRad(40) # Set phong angle to 40
            phongTag[c4d.PHONGTAG_PHONG_USEEDGES] = 1 # Set use edge breaks
            op.InsertTag(phongTag) # Insert phong tag to object
            doc.AddUndo(c4d.UNDOTYPE_NEW, phongTag)
 
def IterateHierarchy(op, doc):
    """
    Perform an op. k. k. a.

    Args:
        op: (todo): write your description
        doc: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    if op is None:
        return
    while op:
        CheckPhong(op, doc) # Check phong tag
        op = GetNextObject(op) # Get next object
    return True

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(0) # Get active objects
        start_object = doc.GetFirstObject() # Get first object
        if selection: # If selected objects
            for s in selection: # Iterate through selected objects
                if s.GetBit(c4d.BIT_ACTIVE): # If object is selected
                    CheckPhong(s, doc) # Check phong tag
        else: # Otherwise
            IterateHierarchy(start_object, doc) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D  
  
# Execute main()
if __name__=='__main__':
    main()