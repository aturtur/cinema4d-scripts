"""
AR_TagsClone

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TagsClone
Version: 1.0.1
Description-US: Clone selected tag(s) to selected object(s).

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (14.03.2022) - R25 update
"""
# Libraries
import c4d

# Functions
def main():
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