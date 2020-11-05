"""
AR_ConsolidateMaterialTags

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ConsolidateMaterialTags
Version: 1.0
Description-US: Consolidates different polygon selections together that uses same materials. Messes up with material projection. Select object(s) and run the script.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def ConsolidateMaterialSelections(s):
    """
    Given a list of material objects.

    Args:
        s: (todo): write your description
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selectionTags = [] # Initialize list for selection tags
    materialTags = [] # Initialize list for material tags
    materials = [] # Initialize list for materials
    tags = s.GetTags() # Get object's tags

    # Collect information
    for t in tags: # Iterate through tags
        #print t.GetType(), t.GetName()
        if t.GetType() == 5673: # If tag is a selection tag
            selectionTags.append(t) # Add tag to selection tags list
        elif t.GetType() == 5616: # If tag is a material tag
            materialTags.append(t) # Add tag to material tags list
            if t[c4d.TEXTURETAG_MATERIAL] not in materials: # If material is not already in materials
                materials.append(t[c4d.TEXTURETAG_MATERIAL]) # Add material to materials list
        else: # Otherwise
            pass # Do nothing

    # Action
    for m in materials: # Iterate through materials
        materialTag = c4d.BaseTag(5616) # Initialize a material tag
        selectionTag = c4d.SelectionTag(c4d.Tpolygonselection) # Initialize a selection tag
        selectionTag.SetName(m.GetName()+"_sel") # Set selection tag's name
        for mt in materialTags: # Iterate through material tags
            doc.AddUndo(c4d.UNDOTYPE_DELETE, s) # Add undo for deleting tags
            if mt[c4d.TEXTURETAG_MATERIAL] == m: # If material tag uses material
                for st in selectionTags: # Iterate through selection tags
                    if mt[c4d.TEXTURETAG_RESTRICTION] == st.GetName(): # If material tag is using this selection tag
                        fromSelect = st.GetBaseSelect() # Get old selection
                        toSelect = selectionTag.GetBaseSelect() # Get selection
                        toSelect.Merge(fromSelect) # Add to selection
                    st.Remove() # Remove old selection tag
                mt.Remove() # Remove old material tag
        s.InsertTag(selectionTag) # Insert selection tag to the object
        s.InsertTag(materialTag) # Insert new material tag
        doc.AddUndo(c4d.UNDOTYPE_NEW, s) # Add undo for new tags
        materialTag[c4d.TEXTURETAG_MATERIAL] = m # Set material
        materialTag[c4d.TEXTURETAG_RESTRICTION] = selectionTag.GetName() # Set selection

def main():
    """
    The main routine.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get selected objects
    for s in selection: # Iterate through selection
        ConsolidateMaterialSelections(s) # Run the function    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()