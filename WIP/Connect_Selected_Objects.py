import c4d
global toClean
toClean = []

def Join(op, tempDoc):
    if (not op): return op
    bc = c4d.BaseContainer() # Initialize Base Container
    res = c4d.utils.SendModelingCommand(c4d.MCOMMAND_JOIN, [op], c4d.MODELINGCOMMANDMODE_ALL, bc, tempDoc)
    return res[0]

def MakeEditable(op):
    global toClean
    clone = op.GetClone() # Get clone
    doc.InsertObject(clone) # Insert clone to document
    clone.SetMg(op.GetMg())
    toClean.append(clone)
    bc = c4d.BaseContainer() # Initialize Base Container
    makeEditable = c4d.MCOMMAND_MAKEEDITABLE # Mcommand 'Make Editable'
    op = c4d.utils.SendModelingCommand(makeEditable, [clone], 0, bc, doc) # Make editable
    if op: return op[0] # Return object
    else: pass # Otherwise return nothing

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
    if op is None: return
    while op:
        if isinstance(op, c4d.PolygonObject):
            objects.append(op.GetClone())
        else:
            objects.append(MakeEditable(op))
        op = GetNextObject(op) # Get next object
    if len(objects) != 0:
        tempDoc = c4d.documents.BaseDocument()

        materials = doc.GetMaterials()
        for m in materials:
            mclone = m.GetClone()
            tempDoc.InsertMaterial(mclone)

        null = c4d.BaseObject(c4d.Onull)
        tempDoc.InsertObject(null)
        for o in objects:
            if o != None:
                o.InsertUnder(null)
        joined = Join(null, tempDoc)
        return joined
    return True

def Clean():
    global toClean
    for x in toClean:
        if x.IsAlive():
            x.Remove()

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    start_object = doc.GetFirstObject()
    result = IterateHierarchy(start_object)
    doc.InsertObject(result)
    Clean()
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()