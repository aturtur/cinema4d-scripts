import c4d
doc.StartUndo()

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def IterateHierarchy(op, materials):
    if op is None:
        return 
    count = 0
    while op:
        count += 1
        objName = op.GetName()
        for m in materials:
            if m.GetName() == objName:
                t = c4d.BaseTag(5616)
                op.InsertTag(t)
                doc.AddUndo(c4d.UNDOTYPE_NEW, t)
                tag = op.GetFirstTag()
                tag[c4d.TEXTURETAG_MATERIAL] = m
        op = GetNextObject(op) 

def main():
    materials = doc.GetMaterials()
    start_object = doc.GetFirstObject()
    IterateHierarchy(start_object, materials)
    
    c4d.EventAdd()
    doc.EndUndo()
  
if __name__=='__main__':
main()