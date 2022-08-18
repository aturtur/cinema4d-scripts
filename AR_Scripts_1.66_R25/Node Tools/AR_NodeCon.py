"""
AR_NodeCon

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodeCon
Version: 1.0.1
Description-US: Connects two selected nodes, if possible. Supports Redshift and Xpresso graphs

Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (07.10.2021) - Updated for R25
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

def ConnectNodes(nodeMaster, keyMod):
    if keyMod == "Shift":
        fromPort = int(c4d.gui.InputDialog("From port number", 0))
        toPort = int(c4d.gui.InputDialog("To port number", 0))

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
        #lastNode = max(nodes, key=attrgetter('px')) # Get the node with the maximum x position value
        for nodeObj in nodes:
            if nodeObj.node != firstNode.node:
                if keyMod == "None":
                    outPort = GetPort(firstNode.node.GetOutPorts()) # Get out port
                    inPort = GetPort(nodeObj.node.GetInPorts()) # Get in port
                elif keyMod == "Shift":
                    outPortNr = fromPort
                    inPortNr = toPort
                    outPort = firstNode.node.GetOutPort(outPortNr)
                    inPort = nodeObj.node.GetInPort(inPortNr)
                elif keyMod == "Ctrl":
                    outPort = GetLastPort(firstNode.node.GetOutPorts()) # Get out port
                    inPort = GetLastPort(nodeObj.node.GetInPorts()) # Get in port                
                outPort.Connect(inPort) # Connect ports

def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = GetKeyMod() # Get keymodifier
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    #try: # Try to execute following script
    # Xpresso
    for s in selection: # Iterate through selection
        if type(s).__name__ == "XPressoTag": # If operator is xpresso tag
            xpnm = s.GetNodeMaster() # Get node master
            ConnectNodes(xpnm, keyMod) # Run the main function
    # Redshift
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
            rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
            ConnectNodes(rsnm, keyMod) # Run the main function
    #except: # Otherwise
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()