# Libraries
import c4d
from c4d import utils as u

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    storeMode = doc.GetMode() # Get current editor mode
    doc.SetMode(c4d.Medges) # Set editor mode to 'Edges'
    selection = doc.GetActiveObjects(0) # Get active objects
    makeEditable = c4d.MCOMMAND_MAKEEDITABLE # Mcommand 'Make Editable'
    selectAll = c4d.MCOMMAND_SELECTALL # Mcommand 'Select All'
    edgeToSpline = c4d.MCOMMAND_EDGE_TO_SPLINE # Mcommand 'Edge To Spline'
    modeEdgeSel = c4d.MODELINGCOMMANDMODE_EDGESELECTION # Modeling command mode 'Edge Selection'
    createUndo = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO # Modeling command flag 'Create undo'
    bc = c4d.BaseContainer() # Initialize base container
    u.SendModelingCommand(makeEditable, selection, modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Make Editable'
    u.SendModelingCommand(selectAll, selection, modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Select All'
    u.SendModelingCommand(edgeToSpline, selection, modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Edge To Spline'
    for obj in selection: # Iterate through selected objects
        spline = obj.GetDown() # Get spline
        doc.AddUndo(c4d.UNDOTYPE_NEW, spline) # Add undo for inserting spline object
        spline.InsertAfter(obj) # Move spline next to original object
        spline.SetMg(obj.GetMg()) # Reset spline objects matrix
        obj.Remove() # Delete original object
    doc.SetMode(storeMode) # Set editor mode back as it was
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()