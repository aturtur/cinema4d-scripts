"""
AR_PyTagAlignToSpline

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PyTagAlignToSpline
Version: 1.0.0
Description-US: Adds a custom python tag for selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.0 (21.04.2022) - First version
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
    bc[c4d.DESC_CUSTOMGUI] = 200000281    
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

def CreateUserDataPercentSlider(obj, name, val=0, parentGroup=None, unit=c4d.DESC_UNIT_PERCENT):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_REALSLIDER
    bc[c4d.DESC_MINSLIDER] = 0
    bc[c4d.DESC_MAXSLIDER] = 1
    bc[c4d.DESC_STEP] = 0.01
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataInteger(obj, name, val=0, parentGroup=None, unit=c4d.DESC_UNIT_LONG):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_CUSTOMGUI] = c4d.CUSTOMGUI_LONG
    bc[c4d.DESC_MIN] = 0
    bc[c4d.DESC_STEP] = 1      
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

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
    pyTag[c4d.ID_BASELIST_ICON_FILE] = "5699"
    pyTag[1041670] = True # Icon color
    pyTag[c4d.ID_BASELIST_ICON_COLOR] = c4d.Vector(153.0/255.0, 153.0/255.0, 255.0/255.0) # Set color
    pyTag.SetName("AR Align To Spline")
    obj.InsertTag(pyTag)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, pyTag)

    CreateUserDataLink(pyTag, "Spline", None)
    CreateUserDataLink(pyTag, "Rail", None)
    CreateUserDataCheckbox(pyTag, "Tangential")
    CreateUserDataPercentSlider(pyTag, "Progress")
    CreateUserDataInteger(pyTag, "Segment", 0)
    CreateUserDataCycle(pyTag, "Orientation", "+X,-X,+Y,-Y,+Z,-Z")

    # Python Tag code
    # -------------------------------------------------------
    pyTag[c4d.TPYTHON_CODE] = "# AR_AlignToSpline (Python Tag)\n\
# Author: Arttu Rautio (aturtur)\n\
# Website: http://aturtur.com/\n\
# Version: 1.0.0\n\
\n\
#Written for Maxon Cinema 4D R25.117\n\
#Python version 3.9.1\n\
# Libraries\n\
import c4d\n\
\n\
def main():\n\
\n\
    # User Data\n\
    spline = op[c4d.ID_USERDATA,1]\n\
    rail = op[c4d.ID_USERDATA,2]\n\
    position = op[c4d.ID_USERDATA,4]%1\n\
    segment = op[c4d.ID_USERDATA,5]\n\
    orient = op[c4d.ID_USERDATA,6]\n\
    tangential = op[c4d.ID_USERDATA,3]\n\
\n\
    # Error checking\n\
    if spline == None:\n\
        return\n\
\n\
    # Align to Spline\n\
    shelp = c4d.utils.SplineHelp()\n\
    if (spline != None) and (rail != None):\n\
        if not shelp.InitSplineWithRail(spline, rail, c4d.SPLINEHELPFLAGS_GLOBALSPACE | c4d.SPLINEHELPFLAGS_CONTINUECURVE | c4d.SPLINEHELPFLAGS_USERDEFORMERS):\n\
            return\n\
    if (spline != None) and (rail == None):\n\
        if not shelp.InitSplineWith(spline, c4d.SPLINEHELPFLAGS_GLOBALSPACE | c4d.SPLINEHELPFLAGS_CONTINUECURVE | c4d.SPLINEHELPFLAGS_USERDEFORMERS):\n\
            return\n\
\n\
    mat = shelp.GetMatrix(position, segment)\n\
\n\
    # Orientation\n\
    if orient == 0: # X+\n\
        v1 = c4d.Vector(0,1,0)\n\
        a1 = 90\n\
        v2 = c4d.Vector(-1,0,0)\n\
        a2 = 90\n\
\n\
    elif orient == 1: # X-\n\
        v1 = c4d.Vector(0,-1,0)\n\
        a1 = 90\n\
        v2 = c4d.Vector(-1,0,0)\n\
        a2 = 90\n\
\n\
    elif orient == 2: # Y+\n\
        v1 = c4d.Vector(-1,0,0)\n\
        a1 = 90\n\
        v2 = c4d.Vector(0,1,0)\n\
        a2 = -90\n\
\n\
    elif orient == 3: # Y-\n\
        v1 = c4d.Vector(1,0,0)\n\
        a1 = 90\n\
        v2 = c4d.Vector(0,1,0)\n\
        a2 = 90\n\
\n\
    elif orient == 4: # Z+\n\
        v1 = c4d.Vector(0,0,1)\n\
        a1 = -90\n\
        v2 = c4d.Vector(0,0,0)\n\
        a2 = 0\n\
\n\
    elif orient == 5: # Z-\n\
        v1 = c4d.Vector(0,0,1)\n\
        a1 = 90\n\
        v2 = c4d.Vector(0,1,0)\n\
        a2 = 180\n\
\n\
    #\n\
    if tangential:\n\
        mat = mat * c4d.utils.RotAxisToMatrix(v1, c4d.utils.DegToRad(a1)) * c4d.utils.RotAxisToMatrix(v2, c4d.utils.DegToRad(a2))\n\
        op.GetObject().SetMg(mat)\n\
    else:\n\
        m = op.GetObject().GetMg()\n\
        m.off = mat.off\n\
        op.GetObject().SetMg(m)\n\
        pass"
    # -------------------------------------------------------

    pyTag[c4d.ID_USERDATA,5] = 0
    pyTag[c4d.ID_USERDATA,6] = 4

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