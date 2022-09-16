"""
AR_PyTagShowGivenFrames

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagShowGivenFrames
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.0 (02.05.2022) - First version
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

def CreateUserDataString(obj, name, val="", parentGroup=None):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    #bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_CYCLE
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
    pyTag.SetName("AR Show Given Frames")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)

    CreateUserDataString(pyTag, "Frames")
    CreateUserDataCycle(pyTag, "Selected", "On,Off,Default")
    CreateUserDataCycle(pyTag, "Not Selected", "On,Off,Default")

    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# Aspect Ratio Guide (Python Tag)\n\
# By Arttu Rautio (aturtur)\n\
# https://aturtur.com\n\
# Updated: 02.05.2022\n\
\n\
# Libraries\n\
import c4d\n\
import re\n\
\n\
# Functions\n\
def main():\n\
    frames = op[c4d.ID_USERDATA,1]\n\
    selected = op[c4d.ID_USERDATA,2]\n\
    notselected = op[c4d.ID_USERDATA,3]\n\
\n\
    fps = doc.GetFps()\n\
    frame = doc.GetTime().GetFrame(fps)\n\
    frameList = []\n\
    obj = op.GetObject()\n\
\n\
    globalMin = str(doc.GetMinTime().GetFrame(fps))\n\
    globalMax = str(doc.GetMaxTime().GetFrame(fps))\n\
    loopMin = str(doc.GetLoopMinTime().GetFrame(fps))\n\
    loopMax = str(doc.GetLoopMaxTime().GetFrame(fps))\n\
\n\
    try:\n\
        frames = frames.replace('prevstart', loopMin)\n\
        frames = frames.replace('prevend', loopMax)\n\
        frames = frames.replace('start', globalMin)\n\
        frames = frames.replace('end', globalMax)\n\
        array = re.sub(r'\\r', r',', frames)\n\
        array = array.split(',')\n\
        for i in range(0, len(array)):\n\
            rangeItem = array[i].split('-')\n\
            for x in range(int(rangeItem[0]),int(rangeItem[1])+1):\n\
                frameList.append(x)\n\
    except:\n\
        pass\n\
\n\
    if (frame in frameList):\n\
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = selected\n\
        obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = selected\n\
    else:\n\
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = notselected\n\
        obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = notselected"
    # -------------------------------------------------------

    pyTag[c4d.ID_USERDATA,2] = 2 # Set Selected to 'Default'
    pyTag[c4d.ID_USERDATA,3] = 1 # Set Not Selected to 'Off'

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