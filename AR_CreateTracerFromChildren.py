"""
AR_CreateTracerFromChildren

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateTracerFromChildren
Description-US: Create tracer object from selected object's children
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selected = doc.GetActiveObject()  # Get selected object
    children = selected.GetChildren() # Get selected object's children
    tracer = c4d.BaseObject(1018655) # Initialize tracer object
    tracerList = c4d.InExcludeData() # Initialize in-exclude data list

    for obj in children: # Loop through children objects
        tracerList.InsertObject(obj, 1) # Add object to list
    
    tracer[c4d.MGTRACEROBJECT_OBJECTLIST] = tracerList # Update tracer object list
    doc.InsertObject(tracer) # Insert tracer object to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, tracer) # Add undo command for inserting new object

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()