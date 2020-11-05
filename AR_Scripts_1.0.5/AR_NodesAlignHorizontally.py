"""
AR_NodesAlignHorizontally

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesAlignHorizontally
Version: 1.0
Description-US: Aligns selected graph nodes horizontally

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
from operator import attrgetter
try:
    import redshift
except:
    pass

# Classes
class nodeObject(object):
    def __init__(self, obj, px, py, sx, sy):
        """
        Initialize a p : class

        Args:
            self: (todo): write your description
            obj: (todo): write your description
            px: (float): write your description
            py: (float): write your description
            sx: (int): write your description
            sy: (todo): write your description
        """
        self.node = obj # Node object
        self.px = px # X position
        self.py = py # Y position
        self.sx = sx # X scale
        self.sy = sy # Y scale

# Functions
def AlignNodesHor(nodeMaster, keyMod):
    """
    Resignsxsignal object to a pandas.

    Args:
        nodeMaster: (todo): write your description
        keyMod: (str): write your description
    """
    nodes = [] # Initialize a list for collecting nodes
    root = nodeMaster.GetRoot() # Get xpresso root
    for node in root.GetChildren(): # Iterate through nodes
        if node.GetBit(c4d.BIT_ACTIVE): # If node is selected
            bc = node.GetData() # Get copy of base container
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER) # Get copy of shape container
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER) # Get copy of operator container
            px  = bcd.GetReal(100) # Get x position
            py  = bcd.GetReal(101) # Get y position
            sx  = bcd.GetReal(108) # Get x scale
            sy  = bcd.GetReal(109) # Get y scale
            nodes.append(nodeObject(node, px, py, sx, sy)) # Create nodeObject and add it to a list
    if nodes:
        theNode = min(nodes, key=attrgetter('py'))
        nodes.sort(key=attrgetter('py')) # Sort nodes by y position
    nodeMaster.AddUndo() # Add undo for changing nodes
    for i in range(0, len(nodes)): # Iterate through collected nodes
        node =  nodes[i].node # Get node
        bc = node.GetDataInstance() # Get base container
        bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
        bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
        p = theNode.px
        if keyMod == "Shift":
            if i != 0:
                tAnchor = nodes[i].sx / 2.0
                sAnchor = (theNode.px + (theNode.sx / 2.0))
                p = (sAnchor - tAnchor)
        elif keyMod == "Ctrl":
            if i != 0:
                tAnchor = nodes[i].sx
                sAnchor = (theNode.px + theNode.sx)
                p = (sAnchor - tAnchor)        
        bcd.SetReal(100, p) # Set x position

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    try: # Try to execute following script
        # Xpresso
        for s in selection: # Iterate through selection
            if type(s).__name__ == "XPressoTag": # If operator is xpresso tag
                xpnm = s.GetNodeMaster() # Get node master
                AlignNodesHor(xpnm, keyMod) # Run the main function
        # Redshift
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                AlignNodesHor(rsnm, keyMod) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()