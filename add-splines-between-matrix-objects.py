# MATRIX SPLINE SCRIPT
# does not support scaling or rotation, pure position matrix
import c4d
from c4d import utils as u
from c4d.modules import mograph as mo

def main():
    doc.StartUndo()
    selo = doc.GetActiveObjects(0)
        
    if len(selo) > 0:
        positions = []
        for o in selo:            
            # store positions
            
            md = mo.GeGetMoData(o)
            if md is None: return False
            cnt = md.GetCount()
            marr = md.GetArray(c4d.MODATA_MATRIX)
            for i in reversed(xrange(0, cnt)):
                positions.append(marr[i].off+o.GetAbsPos())
            o.DelBit(c4d.BIT_ACTIVE)
            
        # make splines
        matrixA = positions[:len(positions)/2]
        matrixB = positions[len(positions)/2:]
        
        for x in xrange(0,len(matrixA)):
            points = []
            c = 10
            spline = c4d.SplineObject(c, c4d.SPLINETYPE_LINEAR)
            a = matrixA[x] # first point
            b = matrixB[x] # last point
            
            # subd spline
            for k in xrange(0, c):
                t = u.RangeMap(k, 0, c-1, 0, 1, True)
                point = u.MixVec(a, b, t)
                points.append(point)
                
            spline.SetAllPoints(points)
            
            select_points = spline.GetPointS()
            pc = len(spline.GetAllPoints())
            select_points.DeselectAll()
            select_points.Select(0)
            select_points.Select(pc-1)
            spline.InsertTag(c4d.BaseTag(1018068))
            tag = spline.MakeTag(1018068)
            doc.InsertObject(spline)
            doc.AddUndo(c4d.UNDOTYPE_NEW, spline)
            
            spline.SetBit(c4d.BIT_ACTIVE)

            c4d.CallButton(tag, c4d.HAIR_SDYNAMICS_TAG_SET_FIXED)            
            c4d.EventAdd()
            doc.EndUndo()

if __name__=='__main__':
    main()
