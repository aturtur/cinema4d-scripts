import c4d
from c4d import gui

def main():
    doc.StartUndo()
    s = doc.GetSelection()
    p = int(gui.InputDialog("Subd multiplier",0))    
    spline = c4d.SplineObject(len(s), c4d.SPLINETYPE_LINEAR)
    points = []
    try:
        for x in s:
            pos = x.GetMg().off
            points.append(pos)
            x.DelBit(c4d.BIT_ACTIVE)
        spline.SetAllPoints(points)
        doc.InsertObject(spline)
        doc.AddUndo(c4d.UNDOTYPE_NEW, spline)    
        spline.SetBit(c4d.BIT_ACTIVE)
        for i in xrange(0, p):
            c4d.CallCommand(14047)
    except:
        pass
    c4d.EventAdd()
    doc.EndUndo()
    
if __name__=='__main__':
    main()