import c4d
from c4d import gui

def makeSpline():
    selo = doc.GetActiveObjects(0)
    points = []
    for o in selo:
        spline = c4d.SplineObject(2, c4d.SPLINETYPE_LINEAR)
        pos = o.GetMg().off
        points.append(pos)
    p = int(gui.InputDialog("Subd multiplier",4))
    
    for x in selo:
        x.DelBit(c4d.BIT_ACTIVE)
        
    spline.SetAllPoints(points)
    doc.InsertObject(spline)
    
    doc.AddUndo(c4d.UNDOTYPE_NEW, spline)
    spline.SetBit(c4d.BIT_ACTIVE)
        
    # subdivide spline
    for i in xrange(0, p):
        c4d.CallCommand(14047)
    c4d.EventAdd()
    
    return spline

def makeConnections(spline,selo):    
    select_points = spline.GetPointS()
    pc = len(spline.GetAllPoints())
    select_points.DeselectAll()
    select_points.Select(0)
    
    # point a
    aTag = spline.MakeTag(1018074)
    aTag[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = selo[0]
    doc.ExecutePasses(None, 0, 1, 1, 0)
    c4d.CallButton(aTag, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR)
    c4d.EventAdd()
    
    select_points.DeselectAll()
    select_points.Select(pc-1)
    
    # point b
    bTag = spline.MakeTag(1018074)
    bTag[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = selo[1]
    doc.ExecutePasses(None, 0, 1, 1, 0)
    c4d.CallButton(bTag, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR)
    c4d.EventAdd()
    spline.InsertTag(c4d.BaseTag(1018068))

def main():
    selo = doc.GetActiveObjects(0)
    makeConnections(makeSpline(),selo)    
    c4d.EventAdd()
    
if __name__ == "__main__":
    main()