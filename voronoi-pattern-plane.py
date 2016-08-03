import c4d
import random as r

def main():
    p = c4d.BaseObject(c4d.Oplane)
    p[c4d.PRIM_PLANE_SUBW] = 50
    p[c4d.PRIM_PLANE_SUBH] = 50
    
    dis = c4d.BaseObject(1018685)
    noise = c4d.BaseList2D(c4d.Xnoise)
    noise[c4d.SLA_NOISE_SEED] = r.randrange(100000)
    dis[c4d.ID_MG_SHADER_SHADER] = noise
    dis.InsertShader(noise)
    dis.InsertUnder(p)
    
    red = c4d.BaseObject(c4d.Opolyreduction)
    red.InsertUnderLast(p)
    
    f = c4d.BaseObject(c4d.Oformula)
    f[c4d.FORMULAOBJECT_EFFECT] = 0
    f[c4d.FORMULAOBJECT_FY] = "0"
    
    sds = c4d.BaseObject(c4d.Osds)
    sds[c4d.SDSOBJECT_SUBRAY_CM] = 1
    
    doc.InsertObject(sds)
    p.InsertUnder(sds)
    
    s = c4d.BaseObject(1024529)
    s.InsertUnderLast(p)
    
    doc.SetActiveObject(p)
    c4d.CallCommand(12233, 12233)
    p.Remove()
    
    p = sds.GetDown()
    doc.SetActiveObject(p)
    c4d.CallCommand(16351)
    c4d.CallCommand(13323, 13323)
    c4d.CallCommand(12559, 12559)
    doc.SetActiveObject(sds)
    c4d.CallCommand(12236)
    c4d.CallCommand(440000043, 440000043)
    c4d.CallCommand(12187)
    c4d.CallCommand(13323, 13323)
    c4d.CallCommand(12559, 12559)
    c4d.CallCommand(12479, 12479)
    c4d.CallCommand(12109, 12109)

    c4d.EventAdd()

if __name__=='__main__':
    main()
