"""
AR_SelectParents

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectParents
Description-US: Selects one level parent object(s) from selected object(s)
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get active selection
    for x in selection: # Loop through selection
        try: # Try to execute following script
            p = x.GetUp() # Get one level up in Object Manager
            doc.AddUndo(c4d.UNDOTYPE_BITS, x) # Add undo command for changing bits
            x.DelBit(c4d.BIT_ACTIVE) # Deselect original object
            doc.AddUndo(c4d.UNDOTYPE_BITS, p) # Add undo command for changing bits
            p.SetBit(c4d.BIT_ACTIVE) # Select object
        except: # If something went wrong
            pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()