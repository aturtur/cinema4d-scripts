import c4d

def main():
    bd = doc.GetActiveBaseDraw()
    cam = bd.GetSceneCamera(doc)
    obj = op.GetObject()
    camera = op[c4d.ID_USERDATA,1] # user data link: camera
    
    if cam.GetName() == camera.GetName():
        if camera != None:
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 0  
    else:
        if camera != None:
            obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
            obj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1