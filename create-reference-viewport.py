import c4d
from c4d import storage as s
from c4d import gui as g

def main():
    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,"Select reference file",c4d.FILESELECT_LOAD)
    if fn == None: return None
    res = g.InputDialog("Resolution","1280x720")
    width = float(res.split("x")[0])
    height = float(res.split("x")[1])
    ren = doc.GetActiveRenderData()
    zpos = ren[c4d.RDATA_XRES_VIRTUAL]
    c4d.CallCommand(12544) # Create new viewport
    bd = doc.GetActiveBaseDraw()
    cam = c4d.BaseObject(c4d.Ocamera)
    cam.SetName("REFERENCE_CAMERA")
    cam[c4d.CAMERAOBJECT_TARGETDISTANCE] = width
    cam[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2
    doc.InsertObject(cam)
    plane = c4d.BaseObject(c4d.Oplane)
    plane[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2
    plane.SetName("REFERENCE_PLANE")
    plane[c4d.PRIM_AXIS] = 5
    plane[c4d.PRIM_PLANE_SUBW] = 1
    plane[c4d.PRIM_PLANE_SUBH] = 1
    plane[c4d.PRIM_PLANE_WIDTH] = width
    plane[c4d.PRIM_PLANE_HEIGHT] = height
    plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = zpos
    plane.InsertUnder(cam)
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat.SetName("REFERENCE_MATERIAL")
    mat[c4d.MATERIAL_USE_REFLECTION] = 0
    mat[c4d.MATERIAL_ANIMATEPREVIEW] = 1
    color = c4d.BaseShader(c4d.Xbitmap)
    color[c4d.BITMAPSHADER_FILENAME] = fn
    doc.ExecutePasses(None, 0, 1, 1, 0)
    c4d.CallButton(color, c4d.BITMAPSHADER_CALCULATE)
    mat[c4d.MATERIAL_COLOR_SHADER] = color
    mat.InsertShader(color)
    mat.Message(c4d.MSG_UPDATE)
    mat.Update(True, True)
    doc.InsertMaterial(mat)
    t = c4d.BaseTag(5616)
    plane.InsertTag(t)
    tag = plane.GetFirstTag()
    tag[c4d.TEXTURETAG_MATERIAL] = mat
    tag[c4d.TEXTURETAG_PROJECTION] = 6
    bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 1
    bd[c4d.BASEDRAW_DATA_CAMERA] = cam
    bd[c4d.BASEDRAW_TITLE] = "REFERENCE_VIEWPORT"
    cam[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 5000000
    c4d.EventAdd()

if __name__=='__main__':
    main()