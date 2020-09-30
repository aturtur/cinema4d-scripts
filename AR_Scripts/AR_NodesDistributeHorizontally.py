"""
AR_NodesDistributeHorizontally

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesDistributeHorizontally
Version: 1.0
Description-US: Distributes selected nodes horizontally

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
try:
    import redshift
except:
    pass
from operator import attrgetter
from c4d import utils as u

# Classes
class nodeObject(object):
    def __init__(self, obj, px, py, sx, sy):
        self.node = obj # Node object
        self.px = px # X position
        self.py = py # Y position
        self.sx = sx # X scale
        self.sy = sy # Y scale

# Functions
def DistributeNodes(nodeMaster):
    nodes = [] # Initialize a list
    root = nodeMaster.GetRoot() # Get node master root
    for node in root.GetChildren(): # Iterate through nodes
        if node.GetBit(c4d.BIT_ACTIVE): # If node is selected
            bc  = node.GetData() # Get copy of base container
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER) # Get copy of shape container
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER) # Get copy of operator container
            px  = bcd.GetReal(100) # Get x position
            py  = bcd.GetReal(101) # Get y position
            sx  = bcd.GetReal(108) # Get x scale
            sy  = bcd.GetReal(109) # Get y scale
            nodes.append(nodeObject(node, px, py, sx, sy)) # Create nodeObject and add it to a list
            
    if nodes: # If there is nodes
        firstNode = min(nodes, key=attrgetter('px')) # Get the node with the minimum x position value
        lastNode  = max(nodes, key=attrgetter('px')) # Get the node with the maximum x position value
        fpos = firstNode.px + firstNode.sx # Get first position
        lpos = lastNode.px # Get last position
        nodes.sort(key=attrgetter('px')) # Sort nodes by x position
        totalScale = 0 # Init total scale variable
        for i in range (len(nodes)): # Iterate through nodes
            if i != 0 and i != len(nodes)-1: # Not first nor last
                totalScale = totalScale + nodes[i].sx # Calculate total scale
        distance = lpos - fpos # Calculate distance between first and last node
        count = len(nodes) # Get count of nodes
        gap = float((distance-totalScale))/float((count-1)) # Calculate gap between nodes
        r = fpos # Initialize a r variable
    helper = 0 # Initialize a helper variable
    nodeMaster.AddUndo() # Add undo for changing nodes
    for i in range(0, len(nodes)): # Iterate through collected nodes
        node=  nodes[i].node # Get node
        bc  = node.GetDataInstance() # Get base container
        bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
        bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
        if i != 0 and i != len(nodes)-1: # Not first nor last node
            s = nodes[i].sx # Get node length
            r = r + gap + helper # Calculate node position
            helper = s # Set helper
            bcd.SetReal(100, r) # Set x position

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    try: # Try to execute following script
        # Xpresso
        for s in selection: # Iterate through selection
            if type(s).__name__ == "XPressoTag": # If operator is xpresso tag
                xpnm = s.GetNodeMaster() # Get node master
                DistributeNodes(xpnm) # Run the main function
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                DistributeNodes(rsnm) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()