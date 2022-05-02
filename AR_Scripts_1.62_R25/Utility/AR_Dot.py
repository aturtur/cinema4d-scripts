"""
AR_Dot

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Dot
Version: 1.0.0
Description-US: Creates a dot null.

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.0 (02.05.2022) - First version
"""

# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    doc.StartUndo() # Start recording undos

    null = c4d.BaseObject(c4d.Onull) # Init a null object
    null[c4d.ID_BASELIST_ICON_FILE] = "17106" # Set icon to 'Circle'
    null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Set icon color to 'Custom'
    null[c4d.ID_BASELIST_ICON_COLOR] = c4d.Vector(0.235, 0.239, 0.239) # Set icon color
    null[c4d.NULLOBJECT_DISPLAY] = 14 # Set shape to 'None'
    null.SetName(" ") # Set null's name

    doc.InsertObject(null) # Insert null to the project
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Add undo step for inserting a new object


    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()