"""
AR_AxisToCenter

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AxisToCenter
Version: 1.0.2
Description-US: Puts axis to center of the object(s). If non-editable object is selected, tries to move object to center of the children.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.2 (12.03.2021) - Support for nested objects
1.0.1 (23.10.2020) - Major bug fix
"""
# Libraries
import c4d

# Global variables
toClean = []

# Functions
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

def ConnectObjects(lst):
    objects = []
    tempDoc = c4d.documents.BaseDocument()
    for op in lst:
        if isinstance(op, c4d.PolygonObject):
            objects.append(op.GetClone())
        elif (isinstance(op, c4d.BaseObject)) and (op.GetType() != 5103) and (op.GetType() != 5101):
            objects.append(MakeEditable(op, tempDoc))
    if len(objects) != 0:
        null = c4d.BaseObject(c4d.Onull)
        tempDoc.InsertObject(null)
        for o in objects:
            if o != None:
                o.InsertUnder(null)
        joined = Join(null, tempDoc)
        return joined
    return None

def clean():
    global toClean
    for x in toClean:
        if x.IsAlive():
         x.Remove()

def CenterNull(null):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    children = null.GetChildren() # Get children objects
    if len(children) != 0: # If there are children
        childrenMats = [] # Init list for children original matrixes
        for child in children: # Iterate through matrixes
            childrenMats.append(child.GetMg())
        connected = ConnectObjects(children) # Connect children to one single object
        CenterAxis(connected)
        null.SetMg(connected.GetMg())
        for i, mat in enumerate(childrenMats):
            children[i].SetMg(mat)

def CenterAxis(obj): # Center object's axis
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = [] # Initialize empty list
    pointCount = obj.GetPointCount() # Get object's point count
    for i in range(0, pointCount): # Loop through points
        points.append(obj.GetPoint(i)) # Add point to points list
    matrix = obj.GetMg() # Get object's global matrix
    center = obj.GetMp() # Get Object's bounding box center in local space
    axis = obj.GetAbsPos() # Get object's absolute position
    difference = axis - (axis + center) # Calculate difference
    if difference != c4d.Vector(0): # If there is a difference
        for i in range(pointCount): # Loop through object's points
            obj.SetPoint(i, points[i] + difference) # Set new point position
        obj.Message(c4d.MSG_UPDATE) # Send update message
        obj.SetMg(c4d.Matrix((matrix * center),
            matrix.v1, matrix.v2, matrix.v3)) # Set new matrix for the object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active objects
        for obj in selection: # Loop through selection
            
            childrenMat = [] # Initialize list for children matrices
            children = obj.GetChildren() # Get object's children
            for child in children: # Iterate through children
                childMat = child.GetMg() # Get child's matrix
                childrenMat.append(childMat) # Add matrix to the matrices list
            
            if (obj.GetType() != 5100) and (obj.GetType() != 5101): # If selected object is non-editable
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Add undo command for making changes to object
                CenterNull(obj) # Move null
                clean()
            else: # Otherwise
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Add undo command for making changes to object
                                
                CenterAxis(obj) # Center object's axis
                
            for i, child in enumerate(children): # Iterate through children
                child.SetMg(childrenMat[i]) # Reset matrix
                
    except: # If something goes wront
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()