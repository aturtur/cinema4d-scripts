"""
AR_CloneFirstSelectedToChildOfRest

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CloneFirstSelectedToChildOfRest
Description-US: Clones first selected object to the rest of the selected objects
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get selection
        for i, s in enumerate(selection): # Loop through selected objects
            if i != 0: # If not first loop round
                clone = selection[0].GetClone() # Clone first object
                clone.InsertUnder(s) # Insert clone under the object
                doc.AddUndo(c4d.UNDOTYPE_NEW, clone) # Add undo command for inserting a new object
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()
