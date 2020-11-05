"""
AR_SwapObjects

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SwapObjects
Version: 1.0
Description-US: Swaps selected objects between each other. Holding SHIFT while executing script swaps also objects place in hierarchy.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def swapObjects():
    """
    Swap all objects

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    bc = c4d.BaseContainer() # Initialize Base Container
    tempNullA = c4d.BaseObject(c4d.Onull) # Initialize temporary Null object
    tempNullB = c4d.BaseObject(c4d.Onull)
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE) # Get selection
    objA = selection[0] # Get object A
    objB = selection[1] # Get objet B
    matA = objA.GetMg() # Get object A's global matrix
    matB = objB.GetMg() # Get object B's global matrix
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, objA) # Add undo for changing object A
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, objB) # Add undo for changing object B
    tempNullA.InsertBefore(objA) # Insert temp Null A before object A
    tempNullB.InsertBefore(objB) # Insert temp Null B before object B
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT: # If 'shift' key is pressed
            objA.InsertAfter(tempNullB) # Move object
            objB.InsertAfter(tempNullA) # Move object
    objA.SetMg(matB) # Set new matrix to object A
    objB.SetMg(matA) # Set new matrix to object B
    tempNullA.Remove() # Delete temporary objects
    tempNullB.Remove()
    return True # Everything is fine

def main():
    """
    Main entry point.

    Args:
    """
    try: # Try to execute following script
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        doc.StartUndo() # Start recording undos
        swapObjects() # Run the script
        doc.EndUndo() # Stop recording undos
        c4d.EventAdd() # Refresh Cinema 4D
    except: # If something went wrong
        pass # Do nothing

# Execute main()
if __name__=='__main__':
    main()