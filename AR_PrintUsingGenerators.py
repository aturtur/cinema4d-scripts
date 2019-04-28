"""
AR_PrintUsingGenerators

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintUsingGenerators
Description-US: Prints to console what MoGraph generators uses selected effector
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Global variables
selectGenerators = False # If true, generator(s) will be selected

# Functions
def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def IterateHierarchy(op, obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
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
    if op is None: # If there is no objects
        return # End script
    while op: # Infinite loop
        for gen in generators:
            if op.GetType() == generators[gen]:
                if op.GetType() in moNormal: # Cloner, Matrix, Fracture, MoInstance, MoExtrude, PolyFX
                    effectors = op[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
                elif op.GetType() == generators['MoSpline']: # If object is MoSpline
                    effectors = op[c4d.MGMOSPLINEOBJECT_EFFECTORLIST]
                elif op.GetType() == generators['Voronoi Fracture']: # If object is Voronoi Fracture
                    effectors = op[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST]
                if op.GetType() != generators['MoText']: # If object is not MoText
                    for i in range(0, effectors.GetObjectCount()): # Loop through effector list
                        if obj.GetGUID() == effectors.ObjectFromIndex(doc,i).GetGUID(): # If selected effector found in list
                            print op.GetName() # Print generator name to console
                            if selectGenerators:
                                doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                                op.SetBit(c4d.BIT_ACTIVE)
                else: # If object is MoText
                    effall = op[c4d.MGTEXTOBJECT_EFFECTORLIST_ALL]   # All
                    effline = op[c4d.MGTEXTOBJECT_EFFECTORLIST_LINE] # Line
                    effword = op[c4d.MGTEXTOBJECT_EFFECTORLIST_WORD] # Word
                    effchar = op[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR] # Letters
                    for i in range(0, effall.GetObjectCount()):
                        if obj.GetGUID() == effall.ObjectFromIndex(doc,i).GetGUID(): # If selected effector found in list
                            print op.GetName()+" (All)" # Print MoText generator name (all) to console
                            if selectGenerators:  # If select generators is true
                                doc.AddUndo(c4d.UNDOTYPE_BITS, op) # Add undo command for selecting object in Object Manager
                                op.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager
                    for i in range(0, effline.GetObjectCount()):
                        if obj.GetGUID() == effline.ObjectFromIndex(doc,i).GetGUID():
                            print op.GetName()+" (Lines)" # Print MoText generator name (lines) to console
                            if selectGenerators:
                                doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                                op.SetBit(c4d.BIT_ACTIVE)
                    for i in range(0, effword.GetObjectCount()):
                        if obj.GetGUID() == effword.ObjectFromIndex(doc,i).GetGUID():
                            print op.GetName()+" (Words)" # Print MoText generator name (words) to console
                            if selectGenerators:
                                doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                                op.SetBit(c4d.BIT_ACTIVE)
                    for i in range(0, effchar.GetObjectCount()):
                        if obj.GetGUID() == effchar.ObjectFromIndex(doc,i).GetGUID():
                            print op.GetName()+" (Letters)" # Print MoText generator name (letters) to console
                            if selectGenerators:
                                doc.AddUndo(c4d.UNDOTYPE_BITS, op)
                                op.SetBit(c4d.BIT_ACTIVE)
        op = GetNextObject(op) # Get next object in Object Manager

def main():
    global selectGenerators # Access to global variable
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    start_object = doc.GetFirstObject() # Get first object in Object Manager
    obj = doc.GetActiveObject() # Get selected object
    if obj == None: return None # If no selected object, returm none
    IterateHierarchy(start_object, obj)
    if selectGenerators: # If select generators is true
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for deselecting selected object
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()