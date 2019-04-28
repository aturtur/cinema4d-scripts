"""
AR_CreateVertexMapWithField

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateVertexMapWithField
Description-US: Creates vertex map tag with linear field object
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
        wtag = op.MakeVariableTag(c4d.Tvertexmap, op.GetPointCount()) # Initialize weight tag
        doc.AddUndo(c4d.UNDOTYPE_NEW, wtag) # Add undo command for inserting new tag
        wtag[c4d.ID_TAGFIELD_ENABLE] = 1 # Enable fields
        fieldList = wtag[c4d.ID_TAGFIELDS] # Get field list
        fieldLayer = mo.FieldLayer(440000251) # Initialize linear field layer
        fieldLayer.SetLinkedObject(fieldObject) # Link field object to field layer
        fieldList.InsertLayer(fieldLayer) # Add layer to field list
        wtag[c4d.ID_TAGFIELDS] = fieldList # Update fields
        doc.AddUndo(c4d.UNDOTYPE_NEW, fieldObject) # Add undo command for inserting new object
        doc.InsertObject(fieldObject) # Insert field object to document
        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Add undo command for changing bits
        op.DelBit(c4d.BIT_ACTIVE) # Deselect operator
        wtag.SetBit(c4d.BIT_ACTIVE) # Select tag
        fieldObject.SetBit(c4d.BIT_ACTIVE) # Select field object
    except: # If something goes wrong
        pass # Do nothing
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
# Execute main()
if __name__=='__main__':
    main()