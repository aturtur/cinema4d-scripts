"""
AR_TagsCloneHierarchy

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TagsCloneHierarchy
Version: 1.0.2
Description-US: Clones specific tags from first selected hierarchy to second selected hierarchy.

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.2 (07.10.2023) - New feature: if selected tag(s), only those tag type(s) are cloned
1.0.2 (19.01.2022) - R25 update
1.0.1 (03.01.2022) - Bug fix (hiddentags)

To do:
    - If hierarchy does not match tell which objects are different
    - Add option to clone tag hierarchy based on object name

"""

# Libraries
import c4d
from c4d import gui

# Global variables
hiddenTags = [5604, # PolygonTag
              5600] # PointTag]

# Main function
def GetAllChildren(op):

    def CheckRoot(op, root):
        while op: # Infinite loop            
            if op == root:
                return True
            if op.GetUp() == None: # If item has no parent
                if op == root:
                    return True
                else:
                    return False
                break
            op = op.GetUp() # Item is object's parent

    def GetNextObject(op): # Get next object from Object Manager
        if op is None: # If there is no object
            return None # Return none
        if op.GetDown(): # If can go deeper in hierarchy
            return op.GetDown() # Return object
        while not op.GetNext() and op.GetUp(): # If can't go to next object, but can go up
            op = op.GetUp() # Object is parent object
        return op.GetNext() # Return object
    
    root = op # The root object
    collectedObjects = [op] # List for collecting the objects

    while op != None: # While there is an object
        op = GetNextObject(op) # Get the next object
        if op != None: # If the object exsists
            if CheckRoot(op, root): # Check the root object
                collectedObjects.append(op)
                
    return collectedObjects
    
def main():
    doc.StartUndo()

    commonTags = [c4d.BaseTag, c4d.TextureTag, c4d.NormalTag, c4d.UVWTag, c4d.SelectionTag, c4d.modules.character.CAPoseMorphTag, c4d.modules.character.CAWeightTag,
    c4d.VariableTag, c4d.modules.graphview.XPressoTag, c4d.VertexColorTag, c4d.modules.hair.HairVertexMapTag, c4d.modules.hair.HairSelectionTag] # List of tags

    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active objects
    selected_tags = doc.GetSelection() # Get selection

    lists = [] # Initialize a list for collecting hierarchies
    tagTypes = [] # Initialize a list for selected tag types

    # Check if two objects are selected
    if len(selection) < 2:
        gui.MessageDialog('Select two objects!')
        return False

    # Collect hierarchys
    for i, s in enumerate(selection): # Iterate through selected objects
        lists.append(GetAllChildren(selection[i]))

    # Collect tags
    for s in selected_tags: # Iterate through selection
        if type(s) in commonTags:
            tagTypes.append(s.GetType())

    # If hierarchies are different
    if len(lists[0]) != len(lists[1]):
        gui.MessageDialog('Hierarchies does not match!\nMake sure you select two identical hierarchies!')
        return False

    # Iterate through the first hierarchy and clone the tags
    for i in range(0, len(lists[0])):

        tags = lists[0][i].GetTags() # Get object's tags

        # If no tags selected
        if len(tagTypes) == 0:
            for t in tags: # Iterate through the tags
                if t.GetType() not in hiddenTags: # Check if tag type is allowed or not
                    tagClone = t.GetClone() # Clone the tag
                    currTags = lists[1][i].GetTags() # Get target object's tags

                    if len(currTags) > 0: # If there is tags
                        lastTag = currTags[-1] # Get last tag
                        lists[1][i].InsertTag(tagClone, lastTag) # Add tag to after the last tag found

                    else: # If no tags founds
                        lists[1][i].InsertTag(tagClone) # Add tag to the object

                    doc.AddUndo(c4d.UNDOTYPE_NEW, tagClone) # Add undo command for inserting new tag

        # If no custom tag selection
        else:
            for t in tags: # Iterate through the tags
                if t.GetType() not in hiddenTags: # Check if tag type is allowed or not
                    if t.GetType() in tagTypes: # Check if tag type is selected
                        tagClone = t.GetClone() # Clone the tag
                        currTags = lists[1][i].GetTags() # Get target object's tags

                        if len(currTags) > 0: # If there is tags
                            lastTag = currTags[-1] # Get last tag
                            lists[1][i].InsertTag(tagClone, lastTag) # Add tag to after the last tag found

                        else: # If no tags founds
                            lists[1][i].InsertTag(tagClone) # Add tag to the object

                        doc.AddUndo(c4d.UNDOTYPE_NEW, tagClone) # Add undo command for inserting new tag

    doc.EndUndo()
    c4d.EventAdd() # Update

# Execute main()
if __name__=='__main__':
    main()