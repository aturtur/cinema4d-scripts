# create nulls to selected points
import c4d
from c4d import utils

def GetGlobalPosition(obj):
    return obj.GetMg().off

def GetGlobalRotation(obj):
    return utils.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj):
    m = obj.GetMg()
    return c4d.Vector(  m.v1.GetLength(),
                        m.v2.GetLength(),
                        m.v3.GetLength())

def SetGlobalPosition(obj, pos):
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot):
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector( m.v1.GetLength(),
                        m.v2.GetLength(),
                        m.v3.GetLength())
    m = utils.HPBToMatrix(rot)
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SetGlobalScale(obj, scale):
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def main():
    doc.StartUndo()
    obj = doc.GetActiveObject()
    sel = obj.GetPointS()
    count = obj.GetPointCount()
    null = c4d.BaseObject(c4d.Onull)
    null.SetName(str(obj.GetName())+"_points")
    null[c4d.NULLOBJECT_DISPLAY]=14
    SetGlobalPosition(null,GetGlobalPosition(obj))
    SetGlobalRotation(null,GetGlobalRotation(obj))
    SetGlobalScale(null,GetGlobalScale(obj))
    doc.InsertObject(null)

    for i in range(count):

        if(sel.IsSelected(i)):
            point = c4d.BaseObject(c4d.Onull)
            point.SetName("p_"+str(i))
            point[c4d.NULLOBJECT_DISPLAY]=2
            pointpos = obj.GetPoint(i)
            fposx = pointpos[0]
            fposy = pointpos[1]
            fposz = pointpos[2]
            point.SetAbsPos(c4d.Vector(fposx, fposy, fposz))
            point.InsertTag(c4d.BaseTag(1019364))
            tag = point.GetFirstTag()
            tag[c4d.ID_CA_CONSTRAINT_TAG_CLAMP]=1
            tag[50004,1]=3
            tag[50004,4]=3
            tag[50001]=obj
            tag[50004,7]=1
            point.InsertUnder(null)
            doc.AddUndo(c4d.UNDOTYPE_NEW, null)
            
    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()