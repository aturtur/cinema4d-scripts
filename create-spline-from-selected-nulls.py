import c4d
from c4d import utils as u
from c4d import gui

def main():
    doc.StartUndo()
    s = doc.GetSelection()
    p = 10;
    p = int(gui.InputDialog("Subdivisions",10))
    spline = c4d.SplineObject(p*len(s)-p, c4d.SPLINETYPE_LINEAR)
    positions = []
    points = []
    
    for x in s:
        pos = x.GetMg().off
        positions.append(pos)
    for i in xrange(0, len(s)-1):
        for k in xrange(0, p):
            t = u.RangeMap(k, 0, p-1, 0, 1, True)
            point = u.MixVec(positions[i], positions[i+1], t)
            points.append(point)

    spline.SetAllPoints(points)
    doc.InsertObject(spline)
    doc.AddUndo(c4d.UNDOTYPE_NEW, spline)

    c4d.EventAdd()
    doc.EndUndo()
    
if __name__=='__main__':
    main()