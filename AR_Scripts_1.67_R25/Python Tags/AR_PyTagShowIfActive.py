"""
AR_PyTagShowIfActive

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagShowIfActive
Version: 1.0.1
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (05.04.2022) - First version
1.0.1 (19.08.2022) - Added option to select between "Active" and "Selected"
"""

# Libraries
import c4d
from c4d import utils as u

# Functions
def CreateUserDataCycle(obj, name, val, parentGroup=None, unit=c4d.DESC_UNIT_LONG):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLE
    cycleBC = c4d.BaseContainer()
    items = val.split(',')
    for i, item in enumerate(items):
        cycleBC.SetString(i, item)
    bc[c4d.DESC_CYCLE] = cycleBC
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    return element

def CreatePythonTag(obj):
    pyTag = c4d.BaseTag(1022749)
    scriptPath = __file__
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    pyTag.SetName("AR Show If Active")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)
    CreateUserDataCycle(pyTag, "Method", "Selected,Active")

    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# AR_ShowIfActive (Python Tag)\n\
# Author: Arttu Rautio (aturtur)\n\
# Website: http://aturtur.com/\n\
# Version: 1.0.0\n\
\n\
# Written for Maxon Cinema 4D R25.117\n\
# Python version 3.9.1\n\
\n\
# Libraries\n\
import c4d\n\
\n\
# Functions\n\
def main():\n\
    obj = op.GetObject() # Get object\n\
    method = op[c4d.ID_USERDATA,1]\n\
    if method == 1:\n\
        if obj == doc.GetActiveObject(): # If object is active\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0 # Set 'Visible in Editor' to 'On'\n\
        else: # Otherwise\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1 # Set 'Visible in Editor' to 'Off'\n\
    elif method == 0:\n\
        if obj.GetBit(c4d.BIT_ACTIVE) == True: # If object is active\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0 # Set 'Visible in Editor' to 'On'\n\
        else: # Otherwise\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1 # Set 'Visible in Editor' to 'Off'"
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