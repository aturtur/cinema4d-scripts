"""
AR_PyTagShowIfCorrectCam

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagShowIfCorrectCam
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (22.04.2022) - First version
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

def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None):
    if obj is None: return False # If there is no object stop the function
    if shortname is None: shortname = name # Short name is name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK) # Initialize user data
    bc[c4d.DESC_NAME] = name # Set user data name
    bc[c4d.DESC_SHORT_NAME] = shortname # Set userdata short name
    bc[c4d.DESC_DEFAULT] = link # Set default value
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF # Disable animation option
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None: # If there is parent group
        bc[c4d.DESC_PARENTGROUP] = parentGroup # Set parent group
    element = obj.AddUserData(bc) # Add user data
    obj[element] = link # Set user data value
    return element # Return user data field

def CreateUserDataCheckbox(obj, name, val=0, parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BOOL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    #bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_BOOL
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreatePythonTag(obj):
    pyTag = c4d.BaseTag(1022749)
    scriptPath = __file__
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    pyTag.SetName("AR If Correct Camera")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)

    CreateUserDataLink(pyTag, "Camera", None)
    CreateUserDataCycle(pyTag, "Active Mode", "On,Off,Default")
    CreateUserDataCycle(pyTag, "Deactive Mode", "On,Off,Default")
    CreateUserDataCheckbox(pyTag, "Affect Render Visibility")

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
    targetCam = op[c4d.ID_USERDATA,1] # UD: Assigned camera\n\
    activeMode = op[c4d.ID_USERDATA,2] # UD: Active mode\n\
    deactiveMode = op[c4d.ID_USERDATA,3] # UD: Deactive mode\n\
    render = op[c4d.ID_USERDATA,4] # UD: Affect Render Visibility\n\
    obj = op.GetObject() # Get object\n\
    if activeCam == targetCam: # If active camera is same as target camera\n\
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = activeMode # Set 'Visible in Editor' to active\n\
        if render: # If render is ticked\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = activeMode # Set 'Visible in Renderer' to active\n\
    else:\n\
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = deactiveMode # Set 'Visible in Editor' to deactive\n\
        if render: # If render is ticked\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = deactiveMode # Set 'Visible in Renderer' to deactive\n\
    pass"

    pyTag[c4d.ID_USERDATA,2] = 2 # Default
    pyTag[c4d.ID_USERDATA,3] = 1 # Off

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