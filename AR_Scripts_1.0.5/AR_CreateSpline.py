"""
AR_CreateSpline

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateSpline
Version: 1.0
Description-US: Creates a spline various ways

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d import utils as u
from c4d import gui
from collections import OrderedDict

# Functions
def GetKeyMod():
    """
    Retrieves the key from the key.

    Args:
    """
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

def GetGlobalPosition(obj): # Get object's global position
    """
    Return the position of the given object.

    Args:
        obj: (todo): write your description
    """
    return obj.GetMg().off

def GetGlobalRotation(obj): # Get object's global rotation
    """
    Returns the rotation object.

    Args:
        obj: (todo): write your description
    """
    return u.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj): # Get object's global scale
    """
    Return a vector object.

    Args:
        obj: (todo): write your description
    """
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalPosition(obj, pos): # Set object's global position
    """
    Sets position.

    Args:
        obj: (todo): write your description
        pos: (int): write your description
    """
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot): # Set object's global rotation
    """
    Sets the rotation matrix.

    Args:
        obj: (todo): write your description
        rot: (todo): write your description
    """
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector(m.v1.GetLength(),
                       m.v2.GetLength(),
                       m.v3.GetLength())
    m = u.HPBToMatrix(rot)
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SetGlobalScale(obj, scale): # Set object's global scale
    """
    Sets scale scale.

    Args:
        obj: (todo): write your description
        scale: (float): write your description
    """
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def CenterAxis(obj): # Center object's axis
    """
    Generate a 3disisisis.

    Args:
        obj: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = [] # Initialize empty list
    pointCount = obj.GetPointCount() # Get object's point count
    for i in range(0, pointCount): # Loop through points
        points.append(obj.GetPoint(i)) # Add point to points list
    matrix = obj.GetMg() # Get object's global matrix
    axis = obj.GetAbsPos() # Get object's absolute position
    center = obj.GetMp() # Get Object's bounding box center in local space
    difference = axis - (axis + center) # Calculate difference
    if difference != c4d.Vector(0): # If there is a difference
        for i in xrange(pointCount): # Loop through object's points
            obj.SetPoint(i, points[i] + difference) # Set new point position
        obj.Message(c4d.MSG_UPDATE) # Send update message
        obj.SetMg(c4d.Matrix((matrix * center),
            matrix.v1, matrix.v2, matrix.v3)) # Set new matrix for the object

def Subdivide(op, amount):
    """
    Applies a subdivide operation.

    Args:
        op: (int): write your description
        amount: (int): write your description
    """
    bc = c4d.BaseContainer() # Initialize Base Container
    bc[c4d.MDATA_SUBDIVIDE_SPLINESUB] = int(amount) # Subdivision rate
    mcommand = c4d.MCOMMAND_SUBDIVIDE # Mcommand 'Make Editable'
    op = c4d.utils.SendModelingCommand(mcommand, [op], 0, bc, doc, c4d.MODELINGCOMMANDFLAGS_CREATEUNDO) # Subdivide

def CollectPositions(objects):
    """
    Returns a list of positions for a given objects.

    Args:
        objects: (todo): write your description
    """
    positions = []
    for i, obj in enumerate(objects):
        positions.append(obj.GetMg().off)
    return positions

def CreateSpline(pointCount, pointPositions):
    """
    Creates a point array from a pointline coordinates.

    Args:
        pointCount: (str): write your description
        pointPositions: (todo): write your description
    """
    spline = c4d.SplineObject(pointCount, c4d.SPLINETYPE_LINEAR) # Initialize a spline object
    spline.SetAllPoints(pointPositions) # Set spline points
    spline[c4d.SPLINEOBJECT_TYPE] = 0 # Set spline's type to Linear
    spline[c4d.SPLINEOBJECT_INTERPOLATION] = 0 # Set spline's interpolation to None
    return spline # Return the spline

def CreateControls(spline, selectedPoints):
    """
    Creates plots for each spline

    Args:
        spline: (todo): write your description
        selectedPoints: (str): write your description
    """

    def CreateNull(spline, parentNull):
        """
        Creates a point map.

        Args:
            spline: (todo): write your description
            parentNull: (todo): write your description
        """
        pointNull = c4d.BaseObject(c4d.Onull) # Initialize point null object
        pointNull.SetMg(spline.GetUpMg()*spline.GetMg())
        pointNull.SetName(spline.GetName()+" Control "+str(i)) # Set point null's name
        pointNull[c4d.NULLOBJECT_DISPLAY] = 2 # Set point null's display mode circle
        pointNull.SetAbsPos(spline.GetPoint(i)) # Set null's position
        return pointNull

    nullsDict = OrderedDict() # Initialize a dictionary for storing cool stuff

    splinePointCount = len(spline.GetAllPoints()) # Get spline point count
    pointSelection = spline.GetPointS() # Get spline point selection
    pointSelection.DeselectAll() # Deselect all spline points

    # Create parent (group) null
    parentNull = c4d.BaseObject(c4d.Onull) # Initialize parent null object
    SetGlobalPosition(parentNull,GetGlobalPosition(spline)) # Set global position, rotation and scale
    SetGlobalRotation(parentNull,GetGlobalRotation(spline))
    SetGlobalScale(parentNull,GetGlobalScale(spline))
    doc.InsertObject(parentNull) # Insert parent null to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, parentNull) # Add undo command for adding new object
    parentNull.SetName(str(spline.GetName()) + " Controls") # Set parent null's name

    # Select points and create controllers
    if selectedPoints == "All":
        pointSelection.SelectAll(splinePointCount - 1) # Select all spline points
    elif selectedPoints == "Ends":
        pointSelection.Select(0) # Select the first point
        pointSelection.Select(splinePointCount-1) # Select the last point

    for i in range(splinePointCount): # Loop through points
        if(pointSelection.IsSelected(i)): # If point is selected
            pointNull = CreateNull(spline, parentNull)
            #nulls.append(pointNull)
            nullsDict[i] = pointNull
            pointNull.InsertUnderLast(parentNull) # Insert point null last object under parent null
            doc.AddUndo(c4d.UNDOTYPE_NEW, pointNull) # Add undo command for adding new object
            doc.AddUndo(c4d.UNDOTYPE_BITS, pointNull)
            pointNull.SetBit(c4d.BIT_ACTIVE)
    pointSelection.DeselectAll() # Deselect all spline points

    #DeleteWithoutChildren(parentNull)
    #return nulls
    return nullsDict

def CreateDynamics(spline, controllers, subd):
    """
    Create a list of the subdynamaint objects.

    Args:
        spline: (todo): write your description
        controllers: (dict): write your description
        subd: (str): write your description
    """
    def CreateConstraintTag(spline, obj):
        """
        Creates a constraint object.

        Args:
            spline: (todo): write your description
            obj: (todo): write your description
        """
        constraintTag = spline.MakeTag(1018074) # Create hair constraint tag
        doc.AddUndo(c4d.UNDOTYPE_NEW, constraintTag) # Add undo for creating a tag
        constraintTag[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = obj # Set link
        doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
        c4d.CallButton(constraintTag, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR) # Press 'Set' button

    if subd != 0:
        Subdivide(spline, subd)

    pointSelection = spline.GetPointS() # Get spline point selection
    pointSelection.DeselectAll() # Deselect all spline points

    if type(controllers).__name__ == "list":
        for i, obj in enumerate(controllers):
            if subd == 0:
                pointSelection.Select(i) # Select point
            else:
                pointSelection.Select(i*subd) # Select point
            CreateConstraintTag(spline, obj) # Create constraint tag
            pointSelection.DeselectAll() # Deselect all spline points

    elif type(controllers).__name__ == "OrderedDict":
        nullsList = list(controllers.items())
        for i, obj in controllers.items():
            if subd == 0:
                pointSelection.Select(i) # Select point
            else:
                pointSelection.Select(i*subd) # Select point
            CreateConstraintTag(spline, obj) # Create constraint tag
            pointSelection.DeselectAll() # Deselect all spline points

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, spline) # Add undo for changing object
    spline[c4d.SPLINEOBJECT_TYPE] = 0 # Set to linear
    sdTag = c4d.BaseTag(1018068)
    sdTag[c4d.HAIR_SDYNAMICS_TAG_STIFFNESS] = 0 # Set stiffness to zero
    spline.InsertTag(sdTag) # Insert spline dynamics tag
    doc.AddUndo(c4d.UNDOTYPE_NEW, sdTag) # Add undo for creating a new object
    #c4d.CallCommand(14039) # Optimize, remove overlapping points
    return spline

def InsertObject(obj):
    """
    Flush an object.

    Args:
        obj: (todo): write your description
    """
    doc.InsertObject(obj) # Insert obj to the document
    doc.AddUndo(c4d.UNDOTYPE_NEW, obj) # Add undo command for changing bits
    obj.SetBit(c4d.BIT_ACTIVE) # Select obj object in Object Manager

def SplineFromObjects(objects, keyMod):   
    """
    Creates a spline object from a list of objects.

    Args:
        objects: (list): write your description
        keyMod: (str): write your description
    """
    if keyMod == "None":
        pointPositions = CollectPositions(objects)
        pointCount     = len(pointPositions)
        spline         = CreateSpline(pointCount, pointPositions)
        InsertObject(spline)
        CenterAxis(spline) # Center spline's axis

    if keyMod == "Shift":
        cnt = len(objects) # Count of the objects
        for i in range(0, cnt-1): # Iterate through objects
            objA = objects[i]
            objB = objects[i+1]
            posA = objA.GetMg().off
            posB = objB.GetMg().off
            spline = CreateSpline(2, [posA, posB])
            InsertObject(spline)
            CenterAxis(spline) # Center spline's axis

    if keyMod == "Ctrl":
        subd = gui.InputDialog('Subdivide', "0")
        pointPositions = CollectPositions(objects)
        pointCount     = len(pointPositions)
        spline         = CreateSpline(pointCount, pointPositions)
        InsertObject(spline)
        CenterAxis(spline) # Center spline's axis
        CreateDynamics(spline, objects, int(subd)) # Create spline dynamic

    if keyMod == "Ctrl+Shift":
        subd = gui.InputDialog('Subdivide', "0")
        cnt = len(objects) # Count of the objects
        for i in range(0, cnt-1): # Iterate through objects
            objA = objects[i]
            objB = objects[i+1]
            posA = objA.GetMg().off
            posB = objB.GetMg().off
            spline = CreateSpline(2, [posA, posB])
            InsertObject(spline)
            CenterAxis(spline) # Center spline's axis
            CreateDynamics(spline, [objA, objB], int(subd)) # Create spline dynamic

def DeleteWithoutChildren(s):
    """
    Removes all children from a string.

    Args:
        s: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    children = s.GetChildren() # Get selected object's children
    for child in reversed(children): # Loop through children
        globalMatrix = child.GetMg() # Get current global matrix
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child) # Add undo command for moving item
        child.InsertAfter(s) # Move child
        child.SetMg(globalMatrix) # Set old global matrix
    doc.AddUndo(c4d.UNDOTYPE_DELETE, s) # Add undo command for deleting selected object
    s.Remove() # Remove selected object


def main():
    """
    The main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    editorMode = doc.GetMode() # Get editor's active mode
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active objects
    cnt = len(selection) # Count of selected objects

    if editorMode == c4d.Medges:
        edgeToSpline = c4d.MCOMMAND_EDGE_TO_SPLINE # Mcommand 'Edge To Spline'
        modeEdgeSel = c4d.MODELINGCOMMANDMODE_EDGESELECTION # Modeling command mode 'Edge Selection'
        createUndo = c4d.MODELINGCOMMANDFLAGS_CREATEUNDO # Modeling command flag 'Create undo'
        bc = c4d.BaseContainer() # Initialize base container
        u.SendModelingCommand(edgeToSpline, selection, modeEdgeSel, bc, doc, createUndo) # Send modeling command 'Edge To Spline'

        obj = selection[0]
        spline = obj.GetDown()
        spline.InsertBefore(obj)
        spline.SetMg(obj.GetMg())
        CenterAxis(spline)

        doc.AddUndo(c4d.UNDOTYPE_BITS, selection[0]) # Add undo command for changing bits
        selection[0].DelBit(c4d.BIT_ACTIVE) # Deselect object
        doc.AddUndo(c4d.UNDOTYPE_BITS, spline)
        spline.SetBit(c4d.BIT_ACTIVE)
        doc.SetMode(c4d.Mmodel)

    else:
        if cnt == 0: # If no active objects
            if keyMod == "None":
                spline = CreateSpline(2, [c4d.Vector(0,0,0),c4d.Vector(0,0,100),])
                InsertObject(spline)
            if keyMod == "Shift":
                spline = CreateSpline(2, [c4d.Vector(0,0,0),c4d.Vector(0,100,0),])
                InsertObject(spline)
            if keyMod == "Ctrl":
                spline = CreateSpline(2, [c4d.Vector(0,0,0),c4d.Vector(100,0,0),])
                InsertObject(spline)

        elif cnt == 1: # Only one selected
            if selection[0].GetType() == 5101: # If spline object
                subd = gui.InputDialog('Subdivide', "0")
                if keyMod == "None":
                    controllers = CreateControls(selection[0], "Ends")
                elif keyMod == "Shift":
                    controllers = CreateControls(selection[0], "All")
                CreateDynamics(selection[0], controllers, int(subd))
                doc.AddUndo(c4d.UNDOTYPE_BITS, selection[0]) # Add undo command for changing bits
                selection[0].DelBit(c4d.BIT_ACTIVE) # Deselect object
        
        else:
            for s in selection: # Iterate through selection
                doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
                s.DelBit(c4d.BIT_ACTIVE) # Deselect object

            if selection[0].GetType() == 5101: # If spline object
                subd = gui.InputDialog('Subdivide', "0")
                for s in selection:
                    if keyMod == "None":
                        controllers = CreateControls(s, "Ends")
                    elif keyMod == "Shift":
                        controllers = CreateControls(s, "All")
                    CreateDynamics(s, controllers, int(subd))
                    doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
            else:
                SplineFromObjects(selection, keyMod)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__ == "__main__":
    main()