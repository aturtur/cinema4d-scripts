"""
AR_PlainEffectorForEveryMoGraphSelectionTag

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PlainEffectorForEveryMoGraphSelectionTag
Description-US: Creates Plain Effector for every MoGraph Selection Tag
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def PlainEffForEveryMgSelTag(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document

    tags = obj.GetTags() # Get object's tags
    mstag = c4d.BaseTag(1021338) # Initialize MoGraph selection tag
    i = 0 # Initialize iteration variable
    generators = { # MoGraph generators dictionary
        'Cloner':           1018544,   
        'Matrix':           1018545,   
        'Fracture':         1018791,   
        'MoSpline':         440000054, 
        'MoInstance':       1018957,   
        'Voronoi Fracture': 1036557,   
        'MoText':           1019268,   
        'MoExtrude':        1019358,   
        'PolyFX':           1019222,
    }
    for x in tags: # Loop through tags
        if x.GetType() == 1021338: # If tag is MoGraph selection tag
            plain = c4d.BaseObject(1021337) # Initialize plain effector
            plain[c4d.ID_MG_BASEEFFECTOR_SELECTION] = x.GetName() # Set MoGraph selection tag to plain effector selection
            doc.InsertObject(plain) # Insert plain effector
            doc.AddUndo(c4d.UNDOTYPE_NEW, plain) # Add undo command for inserting plain effector to document
            effList = c4d.InExcludeData() # Initialize effector list
            if obj.GetType() == generators['MoText']: # If object is MoText
                effList = obj[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR] # Clone generator's effector lsit
                effList.InsertObject(plain,1) # Add plain effector to effector list
                obj[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR] = effList # Set updated effector list
            elif obj.GetType() == generators['Voronoi Fracture']: # If object is Voronoi Fracture
                effList = obj[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST]
                effList.InsertObject(plain,1)
                obj[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST] = effList
            elif obj.GetType() == generators['MoSpline']: # If object is MoSpline
                effList = obj[c4d.MGMOSPLINEOBJECT_EFFECTORLIST]
                effList.InsertObject(plain,1)
                obj[c4d.MGMOSPLINEOBJECT_EFFECTORLIST] = effList
            else: # If object is any else MoGraph generator
                effList = obj[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
                effList.InsertObject(plain,1)
                obj[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = effList
            i = i + 1 # Increase iteration variable value by one

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get active object(s)
    for obj in selection: # Loop through selection
        PlainEffForEveryMgSelTag(obj) # Create Plain Effector forevery MoGraph selection tag
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()
