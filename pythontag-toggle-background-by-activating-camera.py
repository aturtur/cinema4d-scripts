import c4d

def main():
    bd = doc.GetActiveBaseDraw()
    cam = bd.GetSceneCamera(doc)
    
    bg = op[c4d.ID_USERDATA,1] #userdata background
    fg = op[c4d.ID_USERDATA,2] #userdata foreground
    
    if cam == op.GetObject():
        if bg != None:
            bg[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
        if fg != None:
            fg[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2
    else:
        if bg != None:
            bg[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1
        if fg != None:
            fg[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1