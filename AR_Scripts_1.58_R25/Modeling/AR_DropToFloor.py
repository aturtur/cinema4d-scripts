"""
AR_DropToFloor

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DropToFloor
Version: 1.0.0
Description-US: Places the object on the floor.

Original code by Kuroyume

Written for Maxon Cinema 4D R25.117
Python version 3.9.1
"""

# Libraries
import c4d
from c4d import utils as u
from c4d import documents

# Classes and functions
class DropToFloor:
    def Start_Floor(self, doc, src):
        doc.StartUndo() # Start recording undos
        for i, obj in enumerate(src): # Iterate through objects
            op = self.MakePointObject(src[i]) # Convert to point object
            if op is None: continue # If couldn't get the editable object, continue to next one
            self.DropToFloorFunction(doc, src[i], op) # Drop the object to the floor
        doc.EndUndo() # Stop recording undos
        
    def MakePointObject(self, op):
        pointOp = self.CurrentStateToObject(op.GetDocument(), op) # Run 'current state to object' modeling command function
        if pointOp is None: return None # If no point object, return 'None'
        tempDoc = documents.BaseDocument() # Initialize a temporary document
        if tempDoc is None: return None # If no document, return 'None'
        null = c4d.BaseObject(c4d.Onull) # Initialize a null object
        tempDoc.InsertObject(null) # Place null object to temp doc
        pointOp.InsertUnderLast(null) # Place point object under the null
        pointOp = self.Join(tempDoc, null) # Run 'join' modeling command function
        if pointOp is None: return None # If joining failed, return 'None'

        # Get Global matrix transforms
        mg = op.GetUpMg() # Get global matrix of the parent object
        arr = pointOp.GetAllPoints() # Get all point positions
        if arr is None: return None # If no point positions, retun 'None'
        for i, obj in enumerate(arr): # Iterate through points
            arr[i] = arr[i] * mg
        pointOp.Remove() # Delete object
        documents.KillDocument(tempDoc) # Kill the temp document
        return pointOp

    def CurrentStateToObject(self, doc, op):
        res = u.SendModelingCommand(command=c4d.MCOMMAND_CURRENTSTATETOOBJECT, list=[op], doc=doc)
        if res is False: # If modeling command failed
            return None # Return 'None'
        elif not isinstance(res, list): # If didn't returned a list
            return None # Return 'None'
        return res[0]

    def Join(self, doc, op):
        res = u.SendModelingCommand(command=c4d.MCOMMAND_JOIN, list=[op], doc=doc) 
        if res is False: # If modeling command failed
            return None # Return 'None'
        elif not isinstance(res, list): # If didn't returned a list
            return None # Return 'None'
        return res[0]

    # Drop object to floor
    def DropToFloorFunction(self, doc, src, sop):
        cnt = sop.GetPointCount() # Get point count of the object
        if cnt == 0: return False # If no points, return 'False'
        arr = sop.GetAllPoints() # Get point positions
        if arr is None: return False # If no point positions found, return 'False'

        # Find lowest Y value
        minY = arr[0].y # Initialize a variable for storing minimum Y value
        for i, obj in enumerate(arr): # Iterate through point positions
            if arr[i].y < minY: # If Y value is smaller than currently smallest record
                minY = arr[i].y # Set new smallest value

        # Drop Object to Floor
        if (abs(minY) < 0.000001): return False # If the net movement is 0, do nothing
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, src) # Add undo for changing object
        vec = src.GetAbsPos() # Get absolute position
        vec.y -= minY # Set Y value
        src.SetAbsPos(vec) # Set absolute position
        src.Message(c4d.MSG_UPDATE) # Object is updated, give a message about it
        c4d.EventAdd() # Update Cinema 4D
        return True # All good!

# Main function
def main():
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get selected objects
    if len(selection) == 0: return False # If no objects selected
    dtf = DropToFloor() # Initialize a drop to floor class
    dtf.Start_Floor(doc, selection) # Run the drop the floor function

# Execute main()
if __name__=='__main__':
    main()