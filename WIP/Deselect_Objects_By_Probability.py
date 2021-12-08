# By Arttu Rautio (aturtur)

import random
import c4d
from c4d import gui

# Main function
def decision(probability):
    return random.random() < probability

def main():
    
    selection   = doc.GetActiveObjects(0) # Get active objects
    
    probability = 0.5                     # Change 
    
    for obj in selection:                 # Iterate through the selection
        if decision(probability):
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
            obj.DelBit(c4d.BIT_ACTIVE)
        
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()