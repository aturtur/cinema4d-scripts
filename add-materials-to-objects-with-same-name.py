import c4d

def main():
    doc.StartUndo()
    i = 0
    materials = doc.GetMaterials()    
    for m in materials:            
        matName = materials[i].GetName()    
        obj = doc.SearchObject(matName)
        i = i+1
        if obj != None:
            objName = obj.GetName()
            if matName == objName:
                t = c4d.BaseTag(5616)
                obj.InsertTag(t)
                doc.AddUndo(c4d.UNDOTYPE_NEW, t)
                tag = obj.GetFirstTag()
                tag[c4d.TEXTURETAG_MATERIAL] = m
    i = i + 1

    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()