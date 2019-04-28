"""
AR_CreateSelectionTagWithField

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateSelectionTagWithField
Description-US: Creates polygon selection tag with linear field object
Written for Maxon Cinema 4D R20.057
"""
import c4d
from c4d.modules import mograph as mo
# Main function
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        fieldObject = mo.FieldObject(440000266) # Initialize 'Linear Field'
        stag = c4d.SelectionTag(c4d.Tpolygonselection) # Initialize polygon selection tag
        doc.AddUndo(c4d.UNDOTYPE_NEW, stag) # Add undo command for inserting new tag
        op.InsertTag(stag) # Add selection tag to operator
        stag[c4d.POLYGONSELECTIONTAG_ENABLEFIELDS] = 1 # Enable fields
        fieldList = stag[c4d.POLYGONSELECTIONTAG_FIELDS] # Get field list
        fieldLayer = mo.FieldLayer(440000251) # Initialize linear field layer
        fieldLayer.SetLinkedObject(fieldObject) # Link field object to field layer
        fieldList.InsertLayer(fieldLayer) # Add layer to field list
        stag[c4d.POLYGONSELECTIONTAG_FIELDS] = fieldList # Update fields
        doc.AddUndo(c4d.UNDOTYPE_NEW, fieldObject) # Add undo command for inserting new object    
        doc.InsertObject(fieldObject) # Insert field object to document
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Add undo command for changing bits
        op.DelBit(c4d.BIT_ACTIVE) # Deselect operator
        stag.SetBit(c4d.BIT_ACTIVE) # Select tag
        fieldObject.SetBit(c4d.BIT_ACTIVE) # Select field object
    except: # If something goes wrong
        pass # Do nothing

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
# Execute main()
if __name__=='__main__':
    main()