import c4d

def main():
    obj = op.GetObject()
    
    if obj.GetLayerObject(doc) != None:
        layer = obj.GetLayerObject(doc)
        color = layer[c4d.ID_LAYER_COLOR]
        obj[c4d.ID_BASEOBJECT_COLOR] = color
    else:
        obj[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0.5,0.5,0.5)