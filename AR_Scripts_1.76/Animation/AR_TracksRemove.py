"""
AR_RemoveTracks

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RemoveTracks
Version: 1.0.0
Description-US: Removes animated tracks from selected item(s)

Written for Maxon Cinema 4D 2023.2.2
Python version 3.10.8

Change log:
1.0.0 (28.06.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def RemoveTracks(obj):
    ctracks = obj.GetCTracks() # Get ctracks
    for ctrack in ctracks: # Iterate throuch ctracks
        doc.AddUndo(c4d.UNDOTYPE_DELETE, ctrack) # Add undo step
        ctrack.Remove() # Remove ctrack

def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get selected items
    for s in selection: # Iterate through selected items
        RemoveTracks(s) # Run the function
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main
if __name__ == '__main__':
    main()