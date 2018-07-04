import c4d

select = False

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
def IterateHierarchy(op, obj):
    moGraph = [1018544, 1018791, 1018545, 1018957, 440000054, 1036557, 1019268, 1019358, 1019222]
    moNormal = [1018544, 1018791, 1018545, 1018957, 1019358, 1019222]
    if op is None:
        return
    while op:
        if op.GetType() in moGraph:
            if op.GetType() in moNormal: # Cloner, Matrix, Fracture, MoInstance, MoExtrude, PolyFX
                effectors = op[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
            elif op.GetType() == 440000054: # MoSpline
                effectors = op[c4d.MGMOSPLINEOBJECT_EFFECTORLIST]
            elif op.GetType() == 1036557: # Voronoi
                effectors = op[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST]
                            
            if op.GetType() != 1019268:
                for i in range(0, effectors.GetObjectCount()):
                    if obj.GetGUID() == effectors.ObjectFromIndex(doc,i).GetGUID():
                        print op.GetName()
                        if select:
                            doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                            op.SetBit(c4d.BIT_ACTIVE)
            else: # MoText
                effectorsall = op[c4d.MGTEXTOBJECT_EFFECTORLIST_ALL]
                effectorsline = op[c4d.MGTEXTOBJECT_EFFECTORLIST_LINE]
                effectorsword = op[c4d.MGTEXTOBJECT_EFFECTORLIST_WORD]
                effectorschar = op[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR]
                for i in range(0, effectorsall.GetObjectCount()):
                    if obj.GetGUID() == effectorsall.ObjectFromIndex(doc,i).GetGUID():
                        print op.GetName()+" (All)"
                        if select:
                            doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                            op.SetBit(c4d.BIT_ACTIVE)
                for i in range(0, effectorsline.GetObjectCount()):
                    if obj.GetGUID() == effectorsline.ObjectFromIndex(doc,i).GetGUID():
                        print op.GetName()+" (Lines)"
                        if select:
                            doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                            op.SetBit(c4d.BIT_ACTIVE)
                for i in range(0, effectorsword.GetObjectCount()):
                    if obj.GetGUID() == effectorsword.ObjectFromIndex(doc,i).GetGUID():
                        print op.GetName()+" (Words)"
                        if select:
                            doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                            op.SetBit(c4d.BIT_ACTIVE)
                for i in range(0, effectorschar.GetObjectCount()):
                    if obj.GetGUID() == effectorschar.ObjectFromIndex(doc,i).GetGUID():
                        print op.GetName()+" (Letters)"
                        if select:
                            doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                            op.SetBit(c4d.BIT_ACTIVE)
                        
        op = GetNextObject(op)
    return None

def main():
    doc.StartUndo()
    start_object = doc.GetFirstObject()
    obj = doc.GetActiveObject()
    if obj == None: return None
    IterateHierarchy(start_object, obj)
    if select:
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE)
    c4d.EventAdd()
    doc.EndUndo()    

if __name__=='__main__':
main()