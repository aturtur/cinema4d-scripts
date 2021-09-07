
"""
Compares two hierarchies and moves object from the second hierarchy
to children of the first hierarchy's object which is closest in 3D space.
"""

import c4d
import sys

def main():

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)

    baseHierarchy = selection[0].GetChildren()
    slaveHierarchy = selection[1].GetChildren()

    idPair = []

    doc.StartUndo() # Start recording undos

    for i, sObj in enumerate(baseHierarchy):
        nearestDist = sys.float_info.max
        for j, tObj in enumerate(slaveHierarchy):
            sPos = sObj.GetAbsPos()
            tPos = tObj.GetAbsPos()
            dist = (sPos - tPos).GetLength()
            if dist >= nearestDist: continue
            nearestDist = dist
            closestS = sObj
            closestT = tObj

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, closestT)
        closestT.InsertUnder(closestS)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()