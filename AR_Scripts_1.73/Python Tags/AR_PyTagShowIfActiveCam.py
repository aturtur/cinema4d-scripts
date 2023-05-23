"""
AR_PyTagShowIfActiveCam

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagShowIfActiveCam
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (16.09.2022) - First version
"""

# Libraries
import c4d
from c4d import utils as u

# Functions
def CreatePythonTag(obj):
    pyTag = c4d.BaseTag(1022749)
    scriptPath = __file__
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    pyTag.SetName("AR If Active Camera")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)

    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# AR_ShowOnlyIfCorrectCam (Python Tag)\n\
# Author: Arttu Rautio (aturtur)\n\
# Website: http://aturtur.com/\n\
# Version: 1.0.0\n\
\n\
# Written for Maxon Cinema 4D R26.013\n\
# Python version 3.9.1\n\
\n\
# Libraries\n\
import c4d\n\
\n\
# Functions\n\
def main():\n\
    bd = doc.GetActiveBaseDraw() # Get active base draw\n\
    activeCam = bd.GetSceneCamera(doc) # Get active camera\n\
    cam = op.GetObject() # Get camera\n\
    if cam == activeCam:\n\
        cam[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0\n\
    else:\n\
        cam[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1"
    # -------------------------------------------------------
    return True # All good

def main():
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(1)
    if len(selection) != 0:
        for s in selection:
            CreatePythonTag(s) # Run the function
    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()