"""
AR_CreateTracerFromSelection
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateTracerFromSelection
Description-US: Creates a tracer object and fills it with selected objects
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def tracerFromSelection(selection):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    tracer = c4d.BaseObject(1018655) # Initialize tracer object
    tracerList = c4d.InExcludeData() # Initialize in-exclude data list
    for s in selection: # Loop through selection
        tracerList.InsertObject(s, 1) # Add object to list    
    tracer[c4d.MGTRACEROBJECT_OBJECTLIST] = tracerList # Update tracer object list
    tracer[c4d.MGTRACEROBJECT_MODE] = 1 # 'Connect All Objects'
    tracer[c4d.MGTRACEROBJECT_USEPOINTS] = False # Disable 'Trace Vertices'
    doc.InsertObject(tracer) # Insert tracer object to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, tracer) # Add undo command for inserting new object

def main():
    try: # Try to execute followind script
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        doc.StartUndo() # Start recording undos
        flag = c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER # The selection array is sorted in the selection order
        selection = doc.GetActiveObjects(flag) # Get selected objects
        tracerFromSelection(selection) # Run the function
        doc.EndUndo() # Stop recording undos
        c4d.EventAdd() # Refresh Cinema 4D
    except: # If something went wrong
        pass # Do nothing

# Execute main()
if __name__=='__main__':
    main()