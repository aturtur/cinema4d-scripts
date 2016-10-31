import c4d

def main():
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
                t.SetMaterial(copy)                
c4d.EventAdd()

if __name__=='__main__':
    main()
