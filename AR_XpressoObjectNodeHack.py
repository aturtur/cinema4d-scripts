"""
AR_XpressoObjectNodeHack

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_XpressoObjectNodeHack
Description-US: Create xpresso object node with object link output port using user data.
Cinema 4D has a bug that you can't create object port for object node with python in xpresso, so this is a hack for that.
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None): # Create user data link
    if obj is None: return False # If there is no object stop the function
    if shortname is None: shortname = name # Short name is name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK) # Initialize user data
    bc[c4d.DESC_NAME] = name # Set user data name
    bc[c4d.DESC_SHORT_NAME] = shortname # Set userdata short name
    bc[c4d.DESC_DEFAULT] = link # Set default value
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF # Disable animation option
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None: # If there is parent group
        bc[c4d.DESC_PARENTGROUP] = parentGroup # Set parent group
    element = obj.AddUserData(bc) # Add user data
    obj[element] = link # Set user data value
    return element # Return user data field

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    link1 = CreateUserDataLink(op, "Object", op) # Create user data link  

    xptag = c4d.BaseTag(c4d.Texpresso) # Initialize xpresso tag
    xptag.SetName("My Xpresso Tag") # Set xpresso tag name
    op.InsertTag(xptag) # Insert tag to object
    nodemaster = xptag.GetNodeMaster() # Get node master
    objectNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, None, x=200, y=100) # Create object node
    objPort = objectNode.AddPort(c4d.GV_PORT_OUTPUT, # Add 'user data link' output port to node
        c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER, 0),c4d.DescLevel(1)), message=True)

    c4d.modules.graphview.RedrawMaster(nodemaster) # Refresh xpresso
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()