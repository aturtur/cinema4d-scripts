"""
AR_NodesAddTriplanar

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesAddTriplanar
Version: 1.0
Description-US: Adds triplanar node between selected nodes. Only for Redshift

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
def GetKeyMod():
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
        return keyMod

def GetPort(ports):
    for i, port in enumerate(ports):
        if port.GetNrOfConnections() == 0:
            return port
    return ports[0]

def GetLastPort(ports):
    for i, port in enumerate(reversed(ports)):
        if port.GetNrOfConnections() == 0:
            return port
    return ports[-1]

def CheckConnection(nodeA, nodeB):
    a = []

    outPorts = nodeA.GetOutPorts() # Get outports
    for outPort in outPorts: # Iterate through outPorts
        destPorts = outPort.GetDestination() # Get destination ports
        for destPort in destPorts: # Iterate through destination ports
            destNode = destPort.GetNode() # Get destination node
            if destNode == nodeB: # If nodes are connected
                a.append([outPort, destPort])
    return a


def AddTriplanar(nodeMaster, keyMod):


    #if c[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] in rsNodes: # Check if node found in rsNodes dictionary
    #c[c4d.ID_GVBASE_COLOR] = rsNodes[c[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME]]
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
        firstNode = min(nodes, key=attrgetter('px')) # Get the node with the minimum x position value
        lastNode = max(nodes, key=attrgetter('px')) # Get the node with the maximum x position value

        firstNode.node.DelBit(c4d.BIT_ACTIVE) # Deselect node
        lastNode.node.DelBit(c4d.BIT_ACTIVE) # Deselect node

        connections = CheckConnection(firstNode.node, lastNode.node) # Check if these nodes are connected

        if len(connections) == 0: return False

        portCount = lastNode.node.GetInPortCount()        

        # Add and setup the triplanar node
        #triplanarNode = nodeMaster.CreateNode(root, 1036227, firstNode.node, x = -1, y = -1) # Create a constant node (RS)
        triplanarNode = nodeMaster.CreateNode(root, 1036227, None, x = -1, y = -1) # Create a redshift node (RS)
        triplanarNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "TriPlanar" # Set to triplanar node
        triplanarNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.424, 0.392, 0.541) # Set node color
        imageXPort = triplanarNode.AddPort(c4d.GV_PORT_INPUT, 10000) # Add Image X port
        triplanarOut = triplanarNode.GetOutPort(0)
        triplanarNode.SetBit(c4d.BIT_ACTIVE) # Select node

        # rampNode = nodeMaster.CreateNode(root, 1036227, None, x = -1, y = -1) # Create a redshift node (RS)
        # rampNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSRamp" # Set to ramp node
        # rampNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.663, 0.624, 0.424) # Set node color
        # 10002 (in port)

        # ccNode = nodeMaster.CreateNode(root, 1036227, None, x = -1, y = -1) # Create a redshift node (RS)
        # ccNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSColorCorrection" # Set to color correction node
        # ccNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.788, 0.557, 0.537) # Set node color
        # 10000 (in port)

        # crNode = nodeMaster.CreateNode(root, 1036227, None, x = -1, y = -1) # Create a redshift node (RS)
        # crNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSColorRange" # Set to color change range node
        # ccNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.788, 0.557, 0.537) # Set node color
        # 10000 (in port)
        


        # Position
        bc  = triplanarNode.GetDataInstance() # Get base container
        bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
        bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
        sx  = bcd.GetReal(108) # Get x scale
        sy  = bcd.GetReal(109) # Get y scale

        px = u.MixNum(firstNode.px, lastNode.px, 0.5)
        py = u.MixNum(firstNode.py, lastNode.py, 0.5)
        bcd.SetReal(100, px) # Set x position
        bcd.SetReal(101, py) # Set y position
        
        # Connect ports
        if len(connections) > 1:
            conNum = int(c4d.gui.InputDialog("Connection ID", 0))
            connections[conNum][0].Connect(imageXPort)
            triplanarOut.Connect(connections[conNum][1])
        else:
            connections[0][0].Connect(imageXPort)
            triplanarOut.Connect(connections[0][1])

def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = GetKeyMod() # Get keymodifier
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    #try: # Try to execute following script
    # Redshift
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
            rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
            AddTriplanar(rsnm, keyMod) # Run the main function
    #except: # Otherwise
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()