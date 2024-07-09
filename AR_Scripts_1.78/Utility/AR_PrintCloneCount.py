"""
AR_PrintCloneCount

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintCloneCount
Version: 1.0.0
Description-US: Prints to console count of the clones of the selected MoGraph object

Written for Maxon Cinema 4D 2024.2.0
Python version 3.11.4

Change log:
1.0.0 (20.02.2024) - Initial realease
"""

# Libraries
import c4d
from c4d.modules import mograph as mo

# Functions
def PrintCloneCount(op):
    data = mo.GeGetMoData(op) # Get mograph data
    if data is None: return None # If no data, return none

    name = op.GetName() # Get object's name
    count = data.GetCount() # Get clone count
    farr = data.GetArray(c4d.MODATA_FLAGS) # Get flags array
    visible = count
    hidden = 0
    for i in range(0, count):
        if farr[i] == 0: # If clone is hidden
            hidden += 1
            visible -= 1
    
    # Print stuff to console
    print("Object: " + str(name))
    print("Total count: " + str(count))
    print("Visible count: " + str(visible))
    print("Hidden count: " + str(hidden))
    print("----------------------")

def main():
    selection = doc.GetActiveObjects(0) # Get selected objects
    for s in selection: # Loop through selected objects
        PrintCloneCount(s) # Print clone count
    pass

# Execute main
if __name__ == '__main__':
    main()