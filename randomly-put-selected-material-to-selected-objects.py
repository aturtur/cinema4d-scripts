import c4d
import random as rnd
def main():
    doc.StartUndo()    
    s = doc.GetSelection()
    m = doc.GetActiveMaterials()    
    for x in s:
        if rnd.randint(0,1) == 1:
            texTag = c4d.BaseTag(5616)
            texTag[c4d.TEXTURETAG_MATERIAL] = m[0]
            x.InsertTag(texTag)
            doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)
    c4d.EventAdd()
    doc.EndUndo()
if __name__=='__main__':
    main()
