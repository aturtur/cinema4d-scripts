"""
AR_NodesDisconnect

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesDisconnect
Version: 1.0
Description-US: Disconnect all connection(s) of selected node or connection(s) between selected nodes

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
try:
    import redshift
except:
    pass
from c4d import utils as u

# Functions
def RemoveConnection(nodeMaster):
    """
    Removes all pending nodes.

    Args:
        nodeMaster: (todo): write your description
    """
    nodes = [] # Initialize a list
    root = nodeMaster.GetRoot() # Get node master root
    nodeMaster.AddUndo() # Add undo for changing nodes
    for node in root.GetChildren(): # Iterate through nodes
        if node.GetBit(c4d.BIT_ACTIVE): # If node is selected
            nodes.append(node) #

    cnt = len(nodes) # Get amount of nodes
    if cnt >= 2: # If more than 1 node selected
        for node in nodes: # Iterate through nodes
            outPorts = node.GetOutPorts() # Get outports
            for outPort in outPorts: # Iterate through outPorts
                destPorts = outPort.GetDestination() # Get destination ports
                for destPort in destPorts: # Iterate through destination ports
                    destNode = destPort.GetNode() # Get destination node
                    if destNode.GetBit(c4d.BIT_ACTIVE): # If destination node is selected
                        destPort.Remove() # Remove connection
    else: # Otherwise
        nodes[0].RemoveConnections() # Remove all connections

def main():
    """
    Main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    try: # Try to execute following script
        # Xpresso
        for s in selection: # Iterate through selection
            if type(s).__name__ == "XPressoTag": # If operator is xpresso tag
                xpnm = s.GetNodeMaster() # Get node master
                RemoveConnection(xpnm) # Run the main function
        # Redshift
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                RemoveConnection(rsnm) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()