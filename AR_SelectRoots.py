"""
AR_SelectRoots

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectRoots
Description-US: Select root level parent object(s) from selected object(s)
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def GetRoot(obj):
    while obj: # Infinite loop
        if obj.GetUp() == None: # If object has no parent
            return obj # Return object
            break # Break the loop
        obj = obj.GetUp() # Objct is object's parent

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get active selection
    try: # Try to execute following script
        for x in selection: # Loop through selection
            p = GetRoot(x) # Get root object
            doc.AddUndo(c4d.UNDOTYPE_BITS, x) # Add undo command for changing bits
            x.DelBit(c4d.BIT_ACTIVE) # Deselect original object
            doc.AddUndo(c4d.UNDOTYPE_BITS, p) # Add undo command for changing bits
            p.SetBit(c4d.BIT_ACTIVE) # Select root object
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()