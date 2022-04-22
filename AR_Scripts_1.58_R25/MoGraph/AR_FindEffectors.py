"""
AR_FindEffectors

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_FindEffectors
Version: 1.0.1
Description-US: Selects MoGraph Effector(s) that use(s) selected Field. Selects MoGraph Effector(s) that are used in selected Generator. Does not support subfields or tags!

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (29.03.2022) - Updated to R25
"""

# Libraries
import c4d

# Functions
def GetNextItem(op): # Get next item
    if op==None: return None
    if op.GetDown(): return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def IterateFieldList(op, obj, effector): # Iterate fields
    doc = c4d.documents.GetActiveDocument()
    if op is None: return
    while op:
        link = op.GetLinkedObject(doc)
        if link != None:
            if link.GetGUID() == obj.GetGUID():
                doc.AddUndo(c4d.UNDOTYPE_BITS, effector)
                effector.SetBit(c4d.BIT_ACTIVE)
        op = GetNextItem(op)

def SelectEffectors(op, obj): # Iterate objects
    doc = c4d.documents.GetActiveDocument()

    generators = { # MoGraph generators dictionary
        'Cloner':           1018544,
        'Matrix':           1018545,
        'Fracture':         1018791,
        'MoSpline':         440000054,
        'MoInstance':       1018957,
        'Voronoi Fracture': 1036557,
        'MoText':           1019268,
        'MoExtrude':        1019358,
        'PolyFX':           1019222,
    }
    moNormal = [1018544, 1018791, 1018545, 1018957, 1019358, 1019222]

    commonEffectors = [
        1021337,   # Plain effector
        1019234,   # Delay effector
        1018883,   # Formula effector
        1018775,   # Inheritance effector
        440000219, # Push apart effector
        1025800,   # Python effector
        1018643,   # Random effector
        440000234, # ReEffector effector
        1018561,   # Shader effector
        440000255, # Sound effector
        1018774,   # Spline effector
        1018881,   # Step effector
        1018889,   # Target effector
        1018935,   # Time effector
        1021287    # Volume effector
    ]

    isGenerator = False
    for gen in generators:
        if obj.GetType() == generators[gen]:
            isGenerator = True

    if op is None: return
    while op:
        if isGenerator == True:
            if obj.GetType() in moNormal: # Cloner, Matrix, Fracture, MoInstance, MoExtrude, PolyFX
                effectors = obj[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
            elif obj.GetType() == generators['MoSpline']: # If object is MoSpline
                effectors = obj[c4d.MGMOSPLINEOBJECT_EFFECTORLIST]
            elif obj.GetType() == generators['Voronoi Fracture']: # If object is Voronoi Fracture
                effectors = obj[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST]
            if obj.GetType() != generators['MoText']: # If object is not MoText
                for i in range(0, effectors.GetObjectCount()): # Loop through effector list
                    if op.GetGUID() == effectors.ObjectFromIndex(doc,i).GetGUID(): # If selected effector found in list
                        #stringList.append(op.GetName())
                        doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                        op.SetBit(c4d.BIT_ACTIVE)
            else: # If object is MoText
                effall = obj[c4d.MGTEXTOBJECT_EFFECTORLIST_ALL]   # All
                effline = obj[c4d.MGTEXTOBJECT_EFFECTORLIST_LINE] # Line
                effword = obj[c4d.MGTEXTOBJECT_EFFECTORLIST_WORD] # Word
                effchar = obj[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR] # Letters
                for i in range(0, effall.GetObjectCount()):
                    if op.GetGUID() == effall.ObjectFromIndex(doc,i).GetGUID(): # If selected effector found in list
                        #stringList.append(op.GetName()+" (All)")
                        doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Add undo command for selecting object in Object Manager
                        op.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager
                for i in range(0, effline.GetObjectCount()):
                    if op.GetGUID() == effline.ObjectFromIndex(doc,i).GetGUID():
                        #stringList.append(op.GetName()+" (Lines)")
                        doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                        op.SetBit(c4d.BIT_ACTIVE)
                for i in range(0, effword.GetObjectCount()):
                    if op.GetGUID() == effword.ObjectFromIndex(doc,i).GetGUID():
                        #stringList.append(op.GetName()+" (Words)")
                        doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                        op.SetBit(c4d.BIT_ACTIVE)
                for i in range(0, effchar.GetObjectCount()):
                    if op.GetGUID() == effchar.ObjectFromIndex(doc,i).GetGUID():
                        #stringList.append(op.GetName()+" (Letters)")
                        doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                        op.SetBit(c4d.BIT_ACTIVE)
        else:
            if op.GetType() in commonEffectors:
                field = op[c4d.FIELDS] # Get field list
                fieldRoot = field.GetLayersRoot() # Get field root
                IterateFieldList(fieldRoot.GetFirst(), obj, op)

        op = GetNextItem(op)
    return True

def main():
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo() # Start recording undos
    try:
        start_object = doc.GetFirstObject()
        obj = doc.GetActiveObject()
        SelectEffectors(start_object, obj)
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj)
        obj.DelBit(c4d.BIT_ACTIVE)
    except:
        pass

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()