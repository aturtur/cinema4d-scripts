"""
AR_PyTagShowWhenAnimated

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagShowWhenAnimated
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (05.04.2022) - First version
"""

# Libraries
import c4d
from c4d import utils as u

# Functions
def CreateUserDataSeparator(obj, name, parentGroup=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_SEPARATOR)
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_SEPARATOR
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_SEPARATORLINE] = False
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    return obj.AddUserData(bc)

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

def CreateUserDataGroup(obj, name, parentGroup=None, columns=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_GROUP)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_TITLEBAR] = False
    bc[c4d.DESC_GUIOPEN] = False
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    if columns is not None:
        bc[c4d.DESC_COLUMNS] = columns
    return obj.AddUserData(bc)

def CreatePythonTag(obj):
    pyTag = c4d.BaseTag(1022749)
    scriptPath = __file__
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    pyTag[c4d.ID_BASELIST_ICON_FILE] = iconPath
    pyTag.SetName("AR Show When Animated")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)

    CreateUserDataSeparator(pyTag, "Between the Keys")
    CreateUserDataCycle(pyTag, "Visible in Editor", "On,Off,Default")
    CreateUserDataCycle(pyTag, "Visible in Renderer", "On,Off,Default")
    CreateUserDataSeparator(pyTag, "Otherwise")
    CreateUserDataCycle(pyTag, "Visible in Editor", "On,Off,Default")
    CreateUserDataCycle(pyTag, "Visible in Renderer", "On,Off,Default")

    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# AR_ShowWhenAnimated (Python Tag)\n\
# Author: Arttu Rautio (aturtur)\n\
# Website: http://aturtur.com/\n\
# Version: 1.0.0\n\
\n\
#Written for Maxon Cinema 4D R25.117\n\
#Python version 3.9.1\n\
\n\
# Libraries\n\
import c4d\n\
\n\
# Functions\n\
def main():\n\
    obj       = op.GetObject() # Get the object\n\
    ctracks   = obj.GetCTracks() # Get tracks\n\
    curFrame  = doc.GetTime().GetFrame(doc.GetFps()) # Get current frame\n\
\n\
    vEditorA  = op[c4d.ID_USERDATA,2]\n\
    vRenderA  = op[c4d.ID_USERDATA,3]\n\
    vEditorB  = op[c4d.ID_USERDATA,5]\n\
    vRenderB  = op[c4d.ID_USERDATA,6]\n\
\n\
    minFrame = 0\n\
    maxFrame = 0\n\
\n\
    for ctrack in ctracks: # Iterate through tracks\n\
        curve      = ctrack.GetCurve() # Get current curve\n\
        firstFrame = curve.GetStartTime().GetFrame(doc.GetFps()) # Get number of the first key\n\
        lastFrame  = curve.GetEndTime().GetFrame(doc.GetFps())  # Get number of the last key\n\
\n\
        if minFrame < firstFrame:\n\
            minFrame = firstFrame\n\
        if maxFrame < lastFrame:\n\
            maxFrame = lastFrame\n\
\n\
        if (curFrame >= minFrame) and (curFrame <= maxFrame):\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = vEditorA\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = vRenderA\n\
        else:\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = vEditorB\n\
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = vRenderB\n\
    pass"
    # -------------------------------------------------------

    pyTag[c4d.ID_USERDATA,5] = 1 # Set Otherwise Visible in Editor to 'Off'
    pyTag[c4d.ID_USERDATA,6] = 1 # Set Otherwise Visible in Renderer to 'Off'

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