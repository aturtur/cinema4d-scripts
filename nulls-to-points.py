import c4d

def main():
    doc.StartUndo()
    points = []
    s = doc.GetSelection()
    for x in s:
        mat = x.GetMg()
        pos = mat.off
        posx = pos[0]
        posy = pos[1]
        posz = pos[2]
        pos = c4d.Vector(posx, posy, posz)
        points.append(pos)    
    poly = c4d.PolygonObject(len(points),0)
    poly.SetAllPoints(points)
    doc.InsertObject(poly)
    doc.AddUndo(c4d.UNDOTYPE_NEW, poly)
    
    doc.EndUndo()
    c4d.EventAdd() 

if __name__=='__main__':
    main()