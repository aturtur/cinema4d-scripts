"""
AR_PyTagKeepOnFloor

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagKeepOnFloor
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (09.04.2022) - First version
"""

# Libraries
import c4d
from c4d import utils as u

# Functions
def CreatePythonTag(obj):
    pyTag = c4d.BaseTag(1022749)
    pyTag.SetName("AR Keep On Floor")
    scriptPath = __file__
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)

    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# AR_KeepOnFloor (Python Tag)\n\
# Author: Arttu Rautio (aturtur)\n\
# Website: http://aturtur.com/\n\
# Version: 1.0.0\n\
\n\
# Original code by Kuroyume\n\
\n\
# Written for Maxon Cinema 4D R25.117\n\
# Python version 3.9.1\n\
\n\
# Libraries\n\
import c4d\n\
from c4d import utils as u\n\
from c4d import documents\n\
\n\
# Classes and functions\n\
class DropToFloor:\n\
    def Start_Floor(self, doc, src):\n\
        for i, obj in enumerate(src): # Iterate through objects\n\
            op = self.MakePointObject(src[i]) # Convert to point object\n\
            if op is None: continue # If couldn't get the editable object, continue to next one\n\
            self.DropToFloorFunction(doc, src[i], op) # Drop the object to the floor\n\
\n\
    def MakePointObject(self, op):\n\
        pointOp = self.CurrentStateToObject(op.GetDocument(), op) # Run 'current state to object' modeling command function\n\
        if pointOp is None: return None # If no point object, return 'None'\n\
        tempDoc = documents.BaseDocument() # Initialize a temporary document\n\
        if tempDoc is None: return None # If no document, return 'None'\n\
        null = c4d.BaseObject(c4d.Onull) # Initialize a null object\n\
        tempDoc.InsertObject(null) # Place null object to temp doc\n\
        pointOp.InsertUnderLast(null) # Place point object under the null\n\
        pointOp = self.Join(tempDoc, null) # Run 'join' modeling command function\n\
        if pointOp is None: return None # If joining failed, return 'None'\n\
\n\
        # Get Global matrix transforms\n\
        mg = op.GetUpMg() # Get global matrix of the parent object\n\
        arr = pointOp.GetAllPoints() # Get all point positions\n\
        if arr is None: return None # If no point positions, retun 'None'\n\
        for i, obj in enumerate(arr): # Iterate through points\n\
            arr[i] = arr[i] * mg\n\
        pointOp.Remove() # Delete object\n\
        documents.KillDocument(tempDoc) # Close the temp document\n\
        return pointOp\n\
\n\
    def CurrentStateToObject(self, doc, op):\n\
        res = u.SendModelingCommand(command=c4d.MCOMMAND_CURRENTSTATETOOBJECT, list=[op], doc=doc)\n\
        if res is False: # If modeling command failed\n\
            return None # Return 'None'\n\
        elif not isinstance(res, list): # If didn't returned a list\n\
            return None # Return 'None'\n\
        return res[0]\n\
\n\
    def Join(self, doc, op):\n\
        res = u.SendModelingCommand(command=c4d.MCOMMAND_JOIN, list=[op], doc=doc)\n\
        if res is False: # If modeling command failed\n\
            return None # Return 'None'\n\
        elif not isinstance(res, list): # If didn't returned a list\n\
            return None # Return 'None'\n\
        return res[0]\n\
\n\
    # Drop object to floor\n\
    def DropToFloorFunction(self, doc, src, sop):\n\
        cnt = sop.GetPointCount() # Get point count of the object\n\
        if cnt == 0: return False # If no points, return 'False'\n\
        arr = sop.GetAllPoints() # Get point positions\n\
        if arr is None: return False # If no point positions found, return 'False'\n\
\n\
        # Find lowest Y value\n\
        minY = arr[0].y # Initialize a variable for storing minimum Y value\n\
        for i, obj in enumerate(arr): # Iterate through point positions\n\
            if arr[i].y < minY: # If Y value is smaller than currently smallest record\n\
                minY = arr[i].y # Set new smallest value\n\
\n\
        # Drop Object to Floor\n\
        if (abs(minY) < 0.000001): return False # If the net movement is 0, do nothing\n\
        vec = src.GetAbsPos() # Get absolute position\n\
        vec.y -= minY # Set Y value\n\
        src.SetAbsPos(vec) # Set absolute position\n\
        #src.Message(c4d.MSG_UPDATE)\n\
        #c4d.EventAdd() # Update Cinema 4D\n\
        return True # All good!\n\
\n\
def main():\n\
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get selected objects\n\
    if len(selection) == 0: return False # If no objects selected\n\
    dtf = DropToFloor() # Initialize a drop to floor class\n\
    dtf.Start_Floor(doc, selection) # Run the drop the floor function\n\
\n\
    pass"
    # -------------------------------------------------------

    return True # All good

def main():
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(0)
    if len(selection) != 0:
        for s in selection:
            CreatePythonTag(s) # Run the function
    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()