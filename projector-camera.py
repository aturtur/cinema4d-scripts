import c4d

def main():
    # variables
    selection = doc.GetSelection()
    plane = selection[0]
    null = c4d.BaseObject(c4d.Onull)
    null.SetName("Projector Camera")
    camera = c4d.BaseObject(c4d.Ocamera)

    # null settings
    null[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]
    null[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X]
    null[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = plane[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y]
    null[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = plane[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X]
    null[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = plane[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y]
    null[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z] = plane[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z]
    
    # camera settings
    camera[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] =  - plane[c4d.PRIM_PLANE_WIDTH]
    camera[c4d.CAMERAOBJECT_TARGETDISTANCE] = plane[c4d.PRIM_PLANE_WIDTH]
    
    # insert objects
    doc.InsertObject(null)    
    camera.InsertUnder(null)
    
    c4d.EventAdd()

if __name__=='__main__':
    main()
