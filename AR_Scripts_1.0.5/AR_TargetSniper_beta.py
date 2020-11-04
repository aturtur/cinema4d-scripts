"""
AR_TargetSniper_beta

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TargetSniper_beta
Version: 1.0
Description-US: Shoots ray from the selected camera(s) and cretes focus null to closest hitting point.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d import utils

# Global variables
global toClean
toClean = []

# Functions
def GetKeyMod():
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

def Join(op, tempDoc):
    if (not op): return op
    if op != None: 
        bc = c4d.BaseContainer() # Initialize Base Container
        res = c4d.utils.SendModelingCommand(c4d.MCOMMAND_JOIN, [op], c4d.MODELINGCOMMANDMODE_ALL, bc, tempDoc)
        return res[0]

def MakeEditable(op, tempDoc):
    global toClean

    if op != None:
        clone = op.GetClone() # Get clone
        clone.SetMg(op.GetMg())
        doc.InsertObject(clone) # Insert clone to document
        toClean.append(clone)
        #clone.SetMg(op.GetMg()) # Copy global matrix
        bc = c4d.BaseContainer() # Initialize Base Container
        makeEditable = c4d.MCOMMAND_MAKEEDITABLE # Mcommand 'Make Editable'
        op = c4d.utils.SendModelingCommand(makeEditable, [clone], 0, bc, doc) # Make editable
        if op: return op[0] # Return object

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def IterateHierarchy(op):
    objects = []
    tempDoc = c4d.documents.BaseDocument()
    if op is None: return
    while op:
        if isinstance(op, c4d.PolygonObject):
            objects.append(op.GetClone())
        elif (isinstance(op, c4d.BaseObject)) and (op.GetType() != 5103):
            objects.append(MakeEditable(op, tempDoc))
        op = GetNextObject(op) # Get next object
    if len(objects) != 0:
        null = c4d.BaseObject(c4d.Onull)
        tempDoc.InsertObject(null)
        for o in objects:
            if o != None:
                o.InsertUnder(null)
        joined = Join(null, tempDoc)
        return joined
    return True

# Convert object points to global coordinates
def GetGlobalPoint(obj):
    if not isinstance(obj, c4d.PointObject): return

    mg = obj.GetMg()
    pnt = obj.GetAllPoints()
    pnt_cnt = obj.GetPointCount()

    for id in xrange (pnt_cnt):
        pnt[id] = mg.__mul__(pnt[id])
    return pnt

# Convert global coordinate list to object's local coordinates
def GetLocalPoint(pnt, obj):
    if not isinstance(obj, c4d.BaseObject): return
    if type(pnt) != list: return
    mg = obj.GetMg()
    inv_mg = mg.__invert__()
    for id in xrange(len (pnt)):
        pnt[id] = inv_mg.__mul__(pnt[id])
    return pnt

def GuideSpline(cam, length):
    positions = []
    pos1 = cam.GetMg().off

    m = c4d.Matrix()
    m.off = c4d.Vector(0, 0, length)
    mpos2 = cam.GetMg() * m

    pos2 = mpos2.off
    positions.append(pos1)
    positions.append(pos2)

    splineObject = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
    splineObject.SetAllPoints(positions)

    return splineObject

def GetRayCollision(cam, obj, length, keyMod):
    global toClean
    ray = GuideSpline(cam, length)
    pnt = GetGlobalPoint(ray)
    pnt = GetLocalPoint(pnt, obj)
    direct = pnt[1] - pnt[0]
    rc = utils.GeRayCollider()
    rc. Init(obj)
    rayCollision = rc.Intersect(pnt[0], direct, length)
    if rayCollision:
        intersection = rc.GetNearestIntersection()
        target = c4d.BaseObject(c4d.Onull)
        target[c4d.NULLOBJECT_DISPLAY] = 2
        target.SetName(cam.GetName()+"_Target")
        target.SetAbsPos(intersection['hitpos'])

        doc.AddUndo(c4d.UNDOTYPE_NEW, target)
        if keyMod == "None":
            target.SetMg(obj.GetMg()*target.GetMg())
            doc.InsertObject(target)
        elif keyMod == "Shift":
            null = c4d.BaseObject(c4d.Onull)
            null.SetMg(obj.GetMg()*target.GetMg())
            doc.InsertObject(null)
            target.InsertUnder(cam)
            target.SetMg(null.GetMg())
            toClean.append(null)
            target[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = 0
            target[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = 0
            target[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z] = 0
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, cam)
        cam[c4d.CAMERAOBJECT_TARGETOBJECT] = target
        
def clean():
    global toClean
    for x in toClean:
        if x.IsAlive():
         x.Remove()

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    start_object = doc.GetFirstObject()
    selection = doc.GetActiveObjects(0)
    if len(selection) == 0: return
    result = IterateHierarchy(start_object)
    length = 100000
    for s in selection:
        if s.GetType() == 5103:
            GetRayCollision(s, result, length, keyMod)
    clean()
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()