"""
AR_CreateOwnMaterials

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateOwnMaterials
Version: 1.0
Description-US: Creates own materials for selected objects from existing materials

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(0) # Get active objects
        for x in reversed(selection): # Loop through selection
            if isinstance(x, c4d.BaseObject): # If item is instance of Base Object
                tags = x.GetTags() # Get objects tags
                for t in tags: # Loop through tags
                    if type(t).__name__ == "TextureTag": # If Texture tag founded
                        objname = x.GetName() # Get object's name
                        mat = t.GetMaterial() # Get material
                        matname = mat.GetName() # Get material name
                        copy = mat.GetClone() # Clone material
                        copy.SetName(objname+"_"+matname) # Set cloned material name
                        doc.InsertMaterial(copy) # Insert cloned material to document
                        doc.AddUndo(c4d.UNDOTYPE_NEW, copy)
                        doc.AddUndo(c4d.UNDOTYPE_CHANGE, t)
                        t.SetMaterial(copy) # Set cloned material to object's texture tag
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()