"""
AR_SelectTopParents

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectTopParents
Description-US: Selects top level parent object(s) from selected object(s)
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
            while x: # While 'x' is not none
                x.DelBit(c4d.BIT_ACTIVE) # Deselect object
                if x.GetUp() == None: # If parent is not none
                    x.SetBit(c4d.BIT_ACTIVE) # Select object
                    break # Exit loop
                x = x.GetUp() # Get parent
        except: # If something went wrong
            pass # Do nothing
    doc.EndUndo() # Refresh Cinema 4D
    c4d.EventAdd() # Refresh Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()