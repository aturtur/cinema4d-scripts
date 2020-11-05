"""
AR_SetMoGraphWeightMap

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SetMoGraphWeightMap
Version: 1.0
Description-US: Sets current MoGraph weights to new MoGraph weight map tag

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from c4d.modules import mograph as mo

# Functions
def SetMoGraphWeightMap(op):
    """
    Sets whether or not encoder for a given op.

    Args:
        op: (todo): write your description
    """
    md = mo.GeGetMoData(op)
    if md is None: return False
    cnt = md.GetCount()
    warr = md.GetArray(c4d.MODATA_WEIGHT)
    moWeightMapTag = c4d.BaseTag(c4d.Tmgweight)
    doc.AddUndo(c4d.UNDOTYPE_NEW, moWeightMapTag)
    op.InsertTag(moWeightMapTag)
    mo.GeSetMoDataWeights(moWeightMapTag, warr)

def main():
    """
    The main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    generators = [1018544, 1018545, 1018791, 440000054, 1018957, 1036557, 1019268]    
    selection = doc.GetActiveObjects(0)
    for s in selection:
        if s.GetType() in generators:
            SetMoGraphWeightMap(s)
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()