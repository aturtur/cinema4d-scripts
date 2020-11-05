"""
AR_CopyTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CopyTags
Version: 1.0
Description-US: Copy selected tag(s) to selected object(s)

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def main():
    """
    The main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get selected items
    collectedTags = [] # Initialize list for tags
    collectedObjects = [] # Initialize list for objects
    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag,
                  c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag,
                  c4d.modules.character.CAWeightTag, c4d.VariableTag,
                  c4d.modules.graphview.XPressoTag, c4d.VertexColorTag,
                  c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags
    for s in selection: # Loop through selected items
        if type(s) in commonTags: # If selected item is a tag
            collectedTags.append(s) # Add tag to tag collection
        else: # If selected item is not a tag
            collectedObjects.append(s) # Add object to object collection
    for obj in collectedObjects: # Loop through objects
        for tag in collectedTags: # Loop through tags
            clonedTag = tag.GetClone() # Clone tag
            obj.InsertTag(clonedTag) # Add tag to object
            doc.AddUndo(c4d.UNDOTYPE_NEW, clonedTag) # Add undo command for inserting new tag
            
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()