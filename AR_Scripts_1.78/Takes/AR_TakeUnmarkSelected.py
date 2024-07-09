"""
AR_TakeUnmarkSelected

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TakeUnmarkSelected
Version: 1.0.0
Description-US: Unmarks selected take(s)

Written for Maxon Cinema 4D 2024.4.0
Python version 3.11.4

Change log:
1.0.0 (26.04.2024) - Initial realease
"""

# Libraries
import c4d
from c4d import gui
from c4d.gui import GeDialog

# Functions
def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def CollectTakes(op):
    takes = []
    if op is None:
        return
    while op:
        if op.GetBit(c4d.BIT_ACTIVE) == True:
            takes.append(op)
        op = GetNextObject(op)
    return takes

def main():
    doc.StartUndo() # Start recording undos

    # Take stuff
    takeData  = doc.GetTakeData() # Get take data
    mainTake  = takeData.GetMainTake() # Get main take
    takes = CollectTakes(mainTake) # Collect all selected takes

    for take in takes: # Iterate through takes
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, take) # Add undo for modifying take
        take[c4d.TAKEBASE_CHECK] = False # Unmark take

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()