"""
AR_NodesTextureControllers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesTextureControllers
Version: 1.0.1
Description-US: Creates individual scale, offset and rotate control nodes for Redshift texture and triplanar nodes.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.1 (25.02.2021) - Key modifier support: Shift add only scale, Ctrl add only offset, Alt add only rotation
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

def GetPortIndex(node, portId):
    inPorts = node.GetInPorts()
    for i, port in enumerate(inPorts):
        if port.GetMainID() == portId:
            return i

def AddControllers(nodeMaster, keyMod):
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
        newNodes = []
        if (keyMod == "None") or (keyMod == "Shift"):
            scaleNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1) # Create a constant node (RS)
            newNodes.append(scaleNode)
            scaleNode.SetBit(c4d.BIT_ACTIVE) # Select node
        
        if (keyMod == "None") or (keyMod == "Ctrl"):
            offsetNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1)
            newNodes.append(offsetNode)
            offsetNode.SetBit(c4d.BIT_ACTIVE) # Select node

        if (keyMod == "None") or (keyMod == "Alt"):
            rotateNode = nodeMaster.CreateNode(root, 400001120, firstNode.node, x = -1, y = -1)
            newNodes.append(rotateNode)
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

                    if (keyMod == "None") or (keyMod == "Shift"):
                        scaleNode[c4d.ID_BASELIST_NAME] = "SCALE" # Set name
                        scaleNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                        scaleNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                        scaleNode[c4d.GV_CONST_VALUE] = c4d.Vector(1, 1, 1) # Set default values
                    if (keyMod == "None") or (keyMod == "Ctrl"):
                        offsetNode[c4d.ID_BASELIST_NAME] = "OFFSET" # Set name
                        offsetNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                        offsetNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    if (keyMod == "None") or (keyMod == "Alt"):
                        rotateNode[c4d.ID_BASELIST_NAME] = "ROTATE" # Set name
                        rotateNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.537, 0.71, 0.569) # Set color

                elif node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "TriPlanar":
                    scaleID = 10005
                    offsetID = 10006
                    rotateID = 10007

                    if (keyMod == "None") or (keyMod == "Shift"):
                        scaleNode[c4d.ID_BASELIST_NAME] = "SCALE" # Set name
                        scaleNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                        scaleNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                        scaleNode[c4d.GV_CONST_VALUE] = c4d.Vector(0.01, 0.01, 0.01) # Set default values
                        scaleNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set values
                    if (keyMod == "None") or (keyMod == "Ctrl"):                        
                        offsetNode[c4d.ID_BASELIST_NAME] = "OFFSET" # Set name
                        offsetNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color
                        offsetNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                    if (keyMod == "None") or (keyMod == "Alt"):
                        rotateNode[c4d.ID_BASELIST_NAME] = "ROTATE" # Set name
                        rotateNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set data type to vector
                        rotateNode[c4d.ID_GVBASE_COLOR]  = c4d.Vector(0.325, 0.51, 0.357) # Set color

            if (keyMod == "None") or (keyMod == "Shift"):
                if node.AddPortIsOK(c4d.GV_PORT_INPUT, scaleID):
                    scaleInPort = node.AddPort(c4d.GV_PORT_INPUT, scaleID) # Scale port
                else:
                    scaleInPort = node.GetInPort(GetPortIndex(node, scaleID))

            if (keyMod == "None") or (keyMod == "Ctrl"):
                if node.AddPortIsOK(c4d.GV_PORT_INPUT, offsetID):
                    offsetInPort = node.AddPort(c4d.GV_PORT_INPUT, offsetID) # Offset port
                else:
                    offsetInPort = node.GetInPort(GetPortIndex(node, offsetID))

            if (keyMod == "None") or (keyMod == "Alt"):
                if node.AddPortIsOK(c4d.GV_PORT_INPUT, rotateID):
                    rotateInPort = node.AddPort(c4d.GV_PORT_INPUT, rotateID) # Rotate port
                else:
                    rotateInPort = node.GetInPort(GetPortIndex(node, rotateID))

            if (keyMod == "None") or (keyMod == "Shift"):
                scaleOutPort = scaleNode.GetOutPort(0)
                scaleOutPort.Connect(scaleInPort)
            if (keyMod == "None") or (keyMod == "Ctrl"):
                offsetOutPort = offsetNode.GetOutPort(0)
                offsetOutPort.Connect(offsetInPort)
            if (keyMod == "None") or (keyMod == "Alt"):
                rotateOutPort = rotateNode.GetOutPort(0)
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
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    keyMod = GetKeyMod() # Get key modifier
    try: # Try to execute following script
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                AddControllers(rsnm, keyMod) # Run the main function
    except: # Otherwise
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()