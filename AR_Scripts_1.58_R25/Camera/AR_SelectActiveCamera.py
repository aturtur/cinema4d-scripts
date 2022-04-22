"""
AR_SelectActiveCamera

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectActiveCamera
Version: 1.0
Description-US: Selects the active camera

Written for Maxon Cinema 4D R25.010
Python version 3.9.1
"""

# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    bd = doc.GetActiveBaseDraw() # Get active base draw
    activeCam = bd.GetSceneCamera(doc) # Get active camera
    selection = doc.GetSelection() # Get active selection
    if len(selection) != 0: # If there is selected items
        for s in selection: # Iterate through selection
            doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Record undo
            s.DelBit(c4d.BIT_ACTIVE) # Deselect object
    doc.AddUndo(c4d.UNDOTYPE_BITS, activeCam) # Record undo
    activeCam.SetBit(c4d.BIT_ACTIVE) # Select camera
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()