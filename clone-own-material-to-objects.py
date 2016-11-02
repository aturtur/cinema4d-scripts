import c4d

def main():
    doc.StartUndo()
    s = doc.GetSelection()
    for x in s:     
        tags = x.GetTags()
        for t in tags:
            if t.GetTypeName() == "Texture":
                objname = x.GetName()
                mat = t.GetMaterial()
                matname = mat.GetName()
                copy = mat.GetClone()
                copy.SetName(objname+"_"+matname)
                doc.InsertMaterial(copy)
                doc.AddUndo(c4d.UNDOTYPE_NEW, copy)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, t)
                t.SetMaterial(copy)
                
    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()