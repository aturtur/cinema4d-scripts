"""
AR_ShiftSelectedTag

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ShiftSelectedTag
Version: 1.0
Description-US: Shifts selected tag(s). If you hold shift when you run the script tags will shift to the left, otherwise tag is shifted to the right

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
    
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() #Get selection
    bc = c4d.BaseContainer() # Get base container
    forward = True # Initialize direction variable
    
    # Input qualifier check
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT: # If shift is pressed
            forward = False # Set direction to backwards
    
    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag, c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag, c4d.modules.character.CAWeightTag,
    c4d.VariableTag, c4d.modules.graphview.XPressoTag, c4d.VertexColorTag, c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags
    hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Hidden tags
    
    objList = []
    prevGUID = None
    selection = doc.GetSelection() #Get selection
    
    # Collect objects
    for s in selection: # Iterate trough selection
        if type(s) in commonTags: # If selected item is a tag
            obj = s.GetObject() # Get the object
            objGUID = obj.GetGUID() # Get object's GUID
            if objGUID != prevGUID: # If everytime different object
                objList.append(obj) # Add object to the object list
            prevGUID = objGUID # Store previous object's GUID
    # Do the thing
    for obj in objList: # Iterate through collected objects
        tags = obj.GetTags() # Get tags
        tagList = [] # Initialize list for tags
        index = 0 # Initialize index variable
        # Collect active tags
        for tag in tags: # Loop through tags
            if tag not in hiddenTags: # If tag is not a hidden tag
                if tag.GetBit(c4d.BIT_ACTIVE): # Check if tag is selected
                    tagList.append([tag, index]) # Add selected tag to the list
                else:
                    tagList.append([tag, None]) # Add not selected tag to the list
                index = index + 1 # Increase index by one
        # Remove tags
        for tag in tags: # Loop again trough tags
            doc.AddUndo(c4d.UNDOTYPE_DELETE, tag) # Add undo command for deleting tag
            tag.Remove() # Remove tag
        # Move tags
        if forward: # If direction is forward
            for i, data in reversed(list(enumerate(tagList))): # Loop once again trough tags
                if data[1] != None:
                    tagList.insert(data[1] + 1, tagList.pop(i)) # Move tag forwards
            #tagList.insert(spot + 1, tagList.pop(spot)) # Move tag forwards
        else: # Otherwise
            for i, data in enumerate(tagList): # Loop once again trough tags
                if data[1] != None:
                    if data[1] != 0: # If tag is not the first tag
                        tagList.insert(data[1] - 1, tagList.pop(i)) # Move tag backwards
        tagList.reverse() # Reverse list items order
        # Add tags back
        for data in tagList: # Loop trough tagList
            obj.InsertTag(data[0]) # Insert tag back to object
            doc.AddUndo(c4d.UNDOTYPE_NEW, data[0]) # Add undo command for inserting tag
                
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()