import c4d
import math
import random as rand

def main():

    minimum = 0.1
    maximum = 1000
    enable_x = 1
    enable_y = 0
    enable_z = 1

    objs = doc.GetActiveObjects(0)    
    if len(objs) == 0:return
    
    for obj in objs:
        
        if enable_x == 1:
            x = math.floor((rand.random() * ((maximum-minimum)+1)*minimum))
        else:
            x = obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X]
        if enable_y == 1:
            y = math.floor((rand.random() * ((maximum-minimum)+1)*minimum))
        else:
            y = obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y]
        if enable_z == 1:
            z = math.floor((rand.random() * ((maximum-minimum)+1)*minimum))
        else:
            z = obj[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z]
        
        obj[c4d.ID_BASEOBJECT_REL_POSITION] = c4d.Vector(x,y,z)
    
    c4d.EventAdd()

if __name__=='__main__':
    main()