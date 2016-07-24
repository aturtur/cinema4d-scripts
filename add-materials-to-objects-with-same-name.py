# add materials to objects with same name
import c4d

def main():
    i = 0
    materials = doc.GetMaterials()    
    for m in materials:            
        matName = materials[i].GetName()    
        obj = doc.SearchObject(matName)
        i = i+1
        if obj != None:
            objName = obj.GetName()
            print(objName)
            if matName == objName:
                obj.InsertTag(c4d.BaseTag(5616))
                tag = obj.GetFirstTag()
                tag[c4d.TEXTURETAG_MATERIAL] = m
    i = i + 1        
    c4d.EventAdd()

if __name__=='__main__':
    main()