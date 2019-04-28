"""
AR_MoveSelectedTag

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoveSelectedTag
Description-US: Moves selected tags. If you hold shift when you run the script tags will move backwards
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import gui

# Functions
def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() #Get selection
    bc = c4d.BaseContainer() # Get base container
    forward = True # Initialize direction variable
    
    # Input qualifier check
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT: # If shift is pressed
            forward = False # Set direction to backwards
    
    try: # Try following
        commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag, c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag, c4d.modules.character.CAWeightTag,
        c4d.VariableTag, c4d.modules.graphview.XPressoTag, c4d.VertexColorTag, c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags
        hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Hidden tags
        for s in selection: # Loop trough selection
            if type(s) in commonTags: # If selected item is a tag
                obj = s.GetObject() # Get object
                tags = obj.GetTags() # Get tags
                tagList = [] # Initialize list for tags
                index = 0 # Initialize index variable
                spot = 0 # Initialize spot variable
                
                # Collect tags
                for tag in tags: # Loop through tags
                    if tag not in hiddenTags: # If tag is not hidden tag
                        tagList.append(tag) # Add tag to list
                        if tag.GetBit(c4d.BIT_ACTIVE): # Check if tag is selected
                            spot = index # Set spot index
                        index = index+1 # Increase index by one
                
                # Remove tags
                for tag in tags: # Loop again trough tags
                    doc.AddUndo(c4d.UNDOTYPE_DELETE, tag) # Add undo command for deleting tag
                    tag.Remove() # Remove tag
                    
                # Move tags
                if forward: # If direction is forward
                    tagList.insert(spot+1, tagList.pop(spot)) # Move tag forwards
                else: # Otherwise
                    if spot != 0: # If tag is not the first tag
                        tagList.insert(spot-1, tagList.pop(spot)) # Move tag backwards
                tagList.reverse() # Reverse list items order
                
                # Add tags back
                for tag in tagList: # Loop trough tagList
                    obj.InsertTag(tag) # Insert tag back to object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, tag) # Add undo command for inserting tag
                    
    except: # If something goes wrong
        pass # Do nothing

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()