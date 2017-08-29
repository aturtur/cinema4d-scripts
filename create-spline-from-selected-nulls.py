import c4d

def main():
    doc.StartUndo()
    s = doc.GetSelection()
    c = len(s)
    spline = c4d.SplineObject(c, c4d.SPLINETYPE_LINEAR)
    points = []

    for x in s:
        pos = x.GetMg().off
        points.append(pos)

    spline.SetAllPoints(points)
    doc.InsertObject(spline)
    doc.AddUndo(c4d.UNDOTYPE_NEW, spline)

    c4d.EventAdd()
    doc.EndUndo()
    
if __name__=='__main__':
    main()