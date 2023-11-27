"""
AR_AbsRenderPaths

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AbsRenderPaths
Version: 1.0.0
Description-US: Converts relative render paths to absolute.

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.0 (03.05.2022) - First version
"""

# Libraries
import c4d
import os

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    renderData = doc.GetActiveRenderData() # Get document render data
    
    renderPath = renderData[c4d.RDATA_PATH] # Get render path
    multipassPath = renderData[c4d.RDATA_MULTIPASS_FILENAME] #  Get multi-pass path
    
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData) # Add undo step for render data changes
    
    # Regular Image
    if renderPath != "": # If render path is not empty
        renderData[c4d.RDATA_PATH] = os.path.abspath(renderPath) # Set absolute path

    # Multi-Pass Image
    if multipassPath != "": # If multi-pass path is not empty
        renderData[c4d.RDATA_MULTIPASS_FILENAME] = os.path.abspath(multipassPath) # Set absolute path

    doc.SetActiveRenderData(renderData) # Set render settings
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

if __name__ == '__main__':
    main()