"""
AR_EdgeSelectionsToSplines

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_EdgeSelectionsToSplines
Version: 1.0.0
Description-US: Creates splines for each edge selection tags

Written for Maxon Cinema 4D 2024.2.0
Python version 3.11.4

Change log:
1.0.0 (12.01.2024) - Initial release

"""

# Libraries
import c4d
from c4d import utils as u

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    storeMode = doc.GetMode() # Get current editor mode
    doc.SetMode(c4d.Medges) # Set editor mode to 'Edges'
    deselectAll = c4d.MCOMMAND_DESELECTALL # Mcommand 'Deselect all'
    makeEditable = c4d.MCOMMAND_MAKEEDITABLE # Mcommand 'Make Editable'
    edgeToSpline = c4d.MCOMMAND_EDGE_TO_SPLINE # Mcommand 'Edge To Spline'
    modeEdgeSel = c4d.MODELINGCOMMANDMODE_EDGESELECTION # Mcommand 'Edge Selection'
    createUndo = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO # Modeling command flag 'Create undo'
    bc = c4d.BaseContainer() # Initialize base container
    selection = doc.GetActiveObjects(0) # Get active objects
    for s in selection: # Iterate selected objects
        tags = s.GetTags() # Get tags
        for t in tags: # Iterate tags
            if t.GetType() == 5701: # If edge selection tag
                u.SendModelingCommand(makeEditable, [s], modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Make Editable'
                u.SendModelingCommand(deselectAll, [s], modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Deselect All'
                doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
                c4d.CallButton(t, c4d.EDGESELECTIONTAG_COMMAND1) # Press 'Select' button
                u.SendModelingCommand(edgeToSpline, [s], modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Edge To Spline'
                spline = s.GetDown() # Get spline
                doc.AddUndo(c4d.UNDOTYPE_NEW, spline) # Add undo for inserting spline object
                spline.InsertAfter(s) # Move spline next to original object
                spline.SetMg(s.GetMg()) # Reset spline objects matrix
    doc.SetMode(storeMode) # Set editor mode back as it was
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()