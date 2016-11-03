import c4d
import random as rand

def main():
    doc.StartUndo()
    objs = doc.GetActiveObjects(0)
    
    if len(objs) == 0:return
    
    for obj in objs:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE,obj)
        obj[c4d.ID_BASEOBJECT_USECOLOR] = 2
        r = rand.random()
        g = rand.random()
        b = rand.random()
        doc.AddUndo(c4d.UNDOTYPE_CHANGE,obj)
        obj[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(r,g,b)
    
    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()