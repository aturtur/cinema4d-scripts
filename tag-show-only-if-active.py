import c4d

def main():
    obj = op.GetObject()    
    if obj == doc.GetActiveObject():
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 0
    else:
        obj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1