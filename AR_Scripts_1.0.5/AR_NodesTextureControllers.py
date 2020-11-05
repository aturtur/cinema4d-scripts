"""
AR_NodesTextureControllers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesTextureControllers
Version: 1.0
Description-US: Creates individual scale, offset and rotate control nodes for Redshift texture and triplanar nodes.

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
def GetPortIndex(node, portId):
    """
    Returns the index of the port

    Args:
        node: (todo): write your description
        portId: (int): write your description
    """
    inPorts = node.GetInPorts()
    for i, port in enumerate(inPorts):
        if port.GetMainID() == portId:
            return i

def AddControllers(nodeMaster):
    """
    Adds a cluster to the network.

    Args:
        nodeMaster: (todo): write your description
    """
    nodes = [] # Initialize a list
    root = nodeMaster.GetRoot() # Get node master root
    nodeMaster.AddUndo() # Add undo for changing nodes
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
        firstNode = min(nodes, key=attrgetter('py')) # Get the node with the minimum y position value

        # Node generation
        scaleNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1) # Crete a constant node (RS)
        offsetNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1)
        rotateNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1)
        newNodes = [scaleNode, offsetNode, rotateNode]

        scaleNode.SetBit(c4d.BIT_ACTIVE) # Select node
        offsetNode.SetBit(c4d.BIT_ACTIVE) # Select node
        rotateNode.SetBit(c4d.BIT_ACTIVE) # Select node

        # Node settings and ports
        for i in range(0, len(nodes)): # Iterate through collected nodes
            node = nodes[i].node # Get node
            node.DelBit(c4d.BIT_ACTIVE)
            if node.GetOperatorID() == 1036227:
                if node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "TextureSampler":
                    scaleID = 10011
                    offsetID = 10012
                    rotateID = 10013

                    scaleNode[c4d.ID_BASELIST_NAME] = "SCALE" # Set name
                    scaleNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                    scaleNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    scaleNode[c4d.GV_CONST_VALUE] = c4d.Vector(1, 1, 1) # Set default values
                    offsetNode[c4d.ID_BASELIST_NAME] = "OFFSET" # Set name
                    offsetNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                    offsetNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    rotateNode[c4d.ID_BASELIST_NAME] = "ROTATE" # Set name
                    rotateNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.537, 0.71, 0.569) # Set color

                elif node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "TriPlanar":
                    scaleID = 10005
                    offsetID = 10006
                    rotateID = 10007

                    scaleNode[c4d.ID_BASELIST_NAME] = "SCALE" # Set name
                    scaleNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                    scaleNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    scaleNode[c4d.GV_CONST_VALUE] = c4d.Vector(0.01, 0.01, 0.01) # Set default values
                    scaleNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set values
                    offsetNode[c4d.ID_BASELIST_NAME] = "OFFSET" # Set name
                    offsetNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                    offsetNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    rotateNode[c4d.ID_BASELIST_NAME] = "ROTATE" # Set name
                    rotateNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    rotateNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color

            if node.AddPortIsOK(c4d.GV_PORT_INPUT, scaleID):
                scaleInPort = node.AddPort(c4d.GV_PORT_INPUT, scaleID) # Scale port
            else:
                scaleInPort = node.GetInPort(GetPortIndex(node, scaleID))

            if node.AddPortIsOK(c4d.GV_PORT_INPUT, offsetID):
                offsetInPort = node.AddPort(c4d.GV_PORT_INPUT, offsetID) # Offset port
            else:
                offsetInPort = node.GetInPort(GetPortIndex(node, offsetID))

            if node.AddPortIsOK(c4d.GV_PORT_INPUT, rotateID):
                rotateInPort = node.AddPort(c4d.GV_PORT_INPUT, rotateID) # Rotate port
            else:
                rotateInPort = node.GetInPort(GetPortIndex(node, rotateID))

            #scaleNode
            scaleOutPort = scaleNode.GetOutPort(0)
            offsetOutPort = offsetNode.GetOutPort(0)
            rotateOutPort = rotateNode.GetOutPort(0)

            # Connect nodes
            scaleOutPort.Connect(scaleInPort)
            offsetOutPort.Connect(offsetInPort)
            rotateOutPort.Connect(rotateInPort)

        for i in range(0, len(newNodes)):
            bc  = newNodes[i].GetDataInstance() # Get base container
            bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
            bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
            px = firstNode.px - 200
            py = firstNode.py + (50 * i)
            bcd.SetReal(100, px) # Set x position
            bcd.SetReal(101, py) # Set y position

def main():
    """
    The main function.

    Args:
    """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    try: # Try to execute following script
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                AddControllers(rsnm) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()