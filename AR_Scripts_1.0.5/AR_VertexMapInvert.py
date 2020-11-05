"""
AR_VertexMapInvert

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_VertexMapInvert
Version: 1.0
Description-US: Inverts selected Vertex Map tag's data

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def main():
    """
    The main function.

    Args:
    """
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get active selection
    for s in selection: # Iterate through selected items
        if s.GetType() == 5682: # If Vertex Map Tag
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Record undo
            data = s.GetAllHighlevelData() # Get Vertex Map data
            for i in xrange(0, len(data)): # Loop through data values
                data[i] = 1 - data[i] # Invert value
            s.SetAllHighlevelData(data) # Set Vertex Map data
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()