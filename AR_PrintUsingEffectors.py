"""
AR_PrintUsingEffectors

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintUsingEffectors
Description-US: Prints to console what MoGraph effectors uses selected field. Does not support subfields or tags!
Written for Maxon Cinema 4D R20.057
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
        if link.GetGUID() == obj.GetGUID(): print effector.GetName()
        op = GetNextItem(op)

def IterateHierarchy(op, obj): # Iterate objects
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

    doc = c4d.documents.GetActiveDocument()
    if op is None: return
    while op:
        if op.GetType() in commonEffectors:
            field = op[c4d.FIELDS] # Get field list
            fieldRoot = field.GetLayersRoot() # Get field root
            IterateFieldList(fieldRoot.GetFirst(), obj, op)
        op = GetNextItem(op)
    return True

def main():
    doc = c4d.documents.GetActiveDocument()
    try:
        start_object = doc.GetFirstObject()
        obj = doc.GetActiveObject()
        IterateHierarchy(start_object, obj)
    except:
        pass

# Execute main()
if __name__=='__main__':
    main()