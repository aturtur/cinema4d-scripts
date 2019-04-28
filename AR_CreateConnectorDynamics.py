"""
AR_CreateConnectorDynamics

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateConnectorDynamics
Description-US: Creates setup with voronoi fracture and connectors for selected cloner
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def CreateConnectorDynamics(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    voroFrac = c4d.BaseObject(1036557) # Initialize voronoi fracture object
    voroFrac[c4d.ID_BASELIST_NAME] = "Connector Dynamics" # Set name
    voroFrac[c4d.ID_FRACTURE_COLORIZE] = 0 # Don't colorize fragments
    dynTag = c4d.BaseTag(180000102) # Initialize dynamics body tag
    dynTag[c4d.RIGID_BODY_SPLIT_CACHE] = 2 # Set 'individual elements'' to 'top level'
    doc.AddUndo(c4d.UNDOTYPE_NEW, voroFrac) # Add undo command for creating new object
    doc.InsertObject(voroFrac, None, obj) # Insert voronoi fracture object to document
    doc.AddUndo(c4d.UNDOTYPE_NEW, dynTag) # Add undo command for creating new tag
    voroFrac.InsertTag(dynTag) # Insert tag to voronoi fracture object
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Add undo command
    obj.InsertUnder(voroFrac) # Insert object under voronoi fracture object
    doc.ExecutePasses(None, 0, 1, 1, 0) # Needed when pressing buttons virtually
    c4d.CallButton(voroFrac, c4d.ID_FRACTURE_AUTOCONNECTOR_ENABLE) # Press 'Create Fixed Connector'
    connector = voroFrac.GetDown() # Get connector object
    doc.AddUndo(c4d.UNDOTYPE_BITS, connector) # Add undo command for changing bits
    connector.SetBit(c4d.BIT_ACTIVE) # Select connector object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active selection
        for obj in selection: # Loop through selected items
            CreateConnectorDynamics(obj) # Run CreateConnectorDynamics function
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.DelBit(c4d.BIT_ACTIVE) # Deselect object
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()
