"""
AR_SortRandom

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SortRandom
Version: 1.0.0
Description-US: Randomize order of selected objects in Object Manager

Note: Objects has to be in same level in the hierarchy!

Written for Maxon Cinema 4D R26.013
Python version 3.9.1
"""

# Libraries
import c4d
import random

# Functions
def main():
    doc.StartUndo() # Start recording undos
    #try: # Try to execute following script
    
    selection = doc.GetActiveObjects(0) # Get selected objects
    
    pO = c4d.BaseObject(c4d.Onull) # Initialize temp null
    if selection[0].GetPred() is not None: # If there is previous object
        insertPos = selection[0].GetPred() # Set insertion position to start from previous object
        insertMode = 1 # Set insert mode to 1
    elif selection[0].GetUp() is not None: # If there is no parent object
        insertPos = selection[0].GetUp() # Set insertion position to start from parent object
        insertMode = 2 # Set insert mode to 2
    else: # If there is no previous or parent object
        insertPos = selection[0] # Set insertion position to start from first object
        insertMode = 3 # Set insert mode to 3
    position = selection[0].GetPred()

    random.shuffle(selection) # Randomize selected objects list
    for s in selection: # Loop through selected objects
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
        if insertMode == 1: # If insert mode is 1
            s.InsertAfter(insertPos) # Move object next to insert position
        elif insertMode == 2: # If insert mode is 2
            s.InsertUnder(insertPos) # Move object next to insert position
        else: # If insert mode is 3
            doc.InsertObject(pO) # Insert temp null to document
            s.InsertAfter(doc.GetFirstObject()) # Move object to first
            pO.Remove() # Remove temp null

    #except: # If something went wrong
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D


# Execute main()
if __name__=='__main__':
    main()