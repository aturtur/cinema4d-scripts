"""
AR_MergeSelectionTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MergeSelectionTags
Version: 1.0.1
Description-US: Merges selection tags, supports object and tag selections

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (05.03.2022) - Updated to R25 and fixed naming conflict
"""
# Libraries
import c4d

# Functions
def SortTags(collectedTags):
    polyTags = [] # Init list for polygon selection tags
    edgeTags = [] # Init list for edge selection tags
    pointTags = [] # Init list for point selection tags
    objects = [] # Init list for objects

    # Sort
    for t in collectedTags:
        if t.GetType() == 5673: # Polygon selection
            polyTags.append(t)
            objects.append(t.GetObject().GetGUID())
        elif t.GetType() == 5701: # Edge selection
            edgeTags.append(t)
            objects.append(t.GetObject().GetGUID())
        elif t.GetType() == 5674: # Point selection
            pointTags.append(t)
            objects.append(t.GetObject().GetGUID())

    objects = list(dict.fromkeys(objects)) # Remove duplicates
    return polyTags, edgeTags, pointTags, objects

def MergePolySelectionTags(polyTags, edgeTags, pointTags, objects):
    removeList = []
    for o in objects:
        objPolyTags = []
        objEdgeTags = []
        objPointTags = []

        for t in polyTags:
            k = t.GetObject()
            if k != None:
                if k.GetGUID() == o:
                    objPolyTags.append(t)
        for t in edgeTags:
            k = t.GetObject()
            if k != None:
                if k.GetGUID() == o:
                    objEdgeTags.append(t)
        for t in pointTags:
            k = t.GetObject()
            if k != None:
                if k.GetGUID() == o:
                    objPointTags.append(t)

        if len(objPolyTags) >= 2:
            obj = objPolyTags[0].GetObject() # Get reference object
            polyTag = c4d.SelectionTag(c4d.Tpolygonselection) # Initialize a poly selection tag
            polyTag.SetName(objPolyTags[0].GetName()) # Use the name of the first selected tag
            obj.InsertTag(polyTag, obj.GetLastTag()) # Insert tag to the object
            doc.AddUndo(c4d.UNDOTYPE_NEW, polyTag) # Record undo for inserting a new tag
            polySelection = polyTag.GetBaseSelect() # Initialize a polygon selection
            for t in objPolyTags: # Iterate through tags
                polySelection.Merge(t.GetBaseSelect()) # Merge selection
                removeList.append(t)

        # Edge tags
        if len(objEdgeTags) >= 2:
            obj = objEdgeTags[0].GetObject() # Get reference object
            edgeTag = c4d.SelectionTag(c4d.Tedgeselection) # Initialize a edge selection tag
            edgeTag.SetName(objEdgeTags[0].GetName()) # Use the name of the first selected tag
            obj.InsertTag(edgeTag, obj.GetLastTag()) # Insert tag to the object
            doc.AddUndo(c4d.UNDOTYPE_NEW, edgeTag) # Record undo for inserting a new tag
            edgeSelection = edgeTag.GetBaseSelect() # Initialize a edge selection
            for t in objEdgeTags: # Iterate through tags
                edgeSelection.Merge(t.GetBaseSelect()) # Merge selection
                removeList.append(t)

        # Point tags
        if len(objPointTags) >= 2:
            obj = objPointTags[0].GetObject() # Get reference object
            pointTag = c4d.SelectionTag(c4d.Tpointselection) # Initialize a point selection tag
            pointTag.SetName(objPointTags[0].GetName()) # Use the name of the first selected tag
            obj.InsertTag(pointTag, obj.GetLastTag()) # Insert tag to the object
            doc.AddUndo(c4d.UNDOTYPE_NEW, pointTag) # Record undo for inserting a new tag
            pointSelection = pointTag.GetBaseSelect() # Initialize a point selection
            for t in objPointTags: # Iterate through tags
                pointSelection.Merge(t.GetBaseSelect()) # Merge selection
                removeList.append(t)

        for t in removeList:
            doc.AddUndo(c4d.UNDOTYPE_DELETE, t) # Record undo for deleting a tag
            t.Remove() # Detele the tag

def MergeSelectionTags(selection):

    collectedObjects = [] # Collect objects
    collectedTags = [] # Collect tags

    for s in selection: # Iterate through selection
        if (type(s).__name__ == "PolygonObject") or (type(s).__name__ == "BaseObject"):
            collectedObjects.append(s)
        elif type(s).__name__ == "SelectionTag":
            collectedTags.append(s)

    if len(collectedTags) == 0: # If no tags selected
        for i, obj in enumerate(collectedObjects):
            collectedTags = []
            tags = obj.GetTags()
            for t in tags:
                if type(t).__name__ == "SelectionTag":
                    collectedTags.append(t)
            polyTags, edgeTags, pointTags, objects = SortTags(collectedTags)
            MergePolySelectionTags(polyTags, edgeTags, pointTags, objects)
    else: # If tags selected
        polyTags, edgeTags, pointTags, objects = SortTags(collectedTags)
        MergePolySelectionTags(polyTags, edgeTags, pointTags, objects)

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetSelection() # Get active selection
    MergeSelectionTags(selection) # Do the thing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D  
  
# Execute main()
if __name__=='__main__':
    main()