"""
AR_DeleteWithoutChildren

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DeleteWithoutChildren
Description-US: Deletes selected object without deleting children
Written for Maxon Cinema 4D R20.057

"""
# Libraries
import c4d
from c4d import gui

# Functions
def deleteWithoutChildren(s):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    children = s.GetChildren() # Get selected object's children
    for child in reversed(children): # Loop through children
        globalMatrix = child.GetMg() # Get current global matrix
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child) # Add undo command for moving item
        child.InsertAfter(s) # Move child
        child.SetMg(globalMatrix) # Set old global matrix
    doc.AddUndo(c4d.UNDOTYPE_DELETE, s) # Add undo command for deleting selected object
    s.Remove() # Remove selected object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        deleteWithoutChildren(op) # Run the script
    except: # If something went wrong
        pass # Do nothing
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()