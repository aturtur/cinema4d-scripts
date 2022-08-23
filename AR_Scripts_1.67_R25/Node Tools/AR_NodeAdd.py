"""
AR_NodeAdd

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodeAdd
Version: 1.0.1
Description-US: Adds node between selected nodes (Only for Redshift).

Notice: Make sure the Redshift material is selected when using the script!

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (06.05.2022) - Added Change Range node
"""

# Libraries
import c4d
try:
    import redshift
except:
    pass
from operator import attrgetter
from c4d import utils as u
from c4d import gui
from c4d.gui import GeDialog

# Variables
GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_BTNS        = 1002
GRP_VAL         = 1003
GRP_COL         = 1004

PORTNUM         = 2001
NODETYPE        = 2002

NODE_RAMP         = 3001
NODE_TRIPLANAR    = 3002
NODE_COLORCORR    = 3003
NODE_SCALARRAMP   = 3004
NODE_COLORLAYER   = 3005
NODE_COLORAOV     = 3006
NODE_COLORRANGE   = 3007
NODE_BUMPMAP      = 3008
NODE_DISPLACEMENT = 3009
NODE_CHANGERANGE  = 3010

BTN_OK          = 7001
BTN_CANCEL      = 7002

ptnum = 0
options = [0, 4000, False]

# Classes
class nodeObject(object):
    def __init__(self, obj, px, py, sx, sy):
        self.node = obj # Node object
        self.px = px # X position
        self.py = py # Y position
        self.sx = sx # X scale
        self.sy = sy # Y scale

class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        global ptnum

        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw

        self.SetTitle("Add Node Between") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=300, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=1, groupflags=1, initw=300, inith=0)
        self.GroupBegin(GRP_VAL, c4d.BFH_LEFT, cols=1, rows=1, groupflags=1, initw=15, inith=0)

        self.AddComboBox(PORTNUM, c4d.BFH_LEFT, 15, 13)
        for i in range(0, ptnum):
            self.AddChild(PORTNUM, 0+i, str(i)) # Port number

        self.SetInt32(PORTNUM, 0) # Set default port number

        self.GroupEnd()

        self.GroupBegin(GRP_COL, c4d.BFH_LEFT, cols=1, rows=1, groupflags=1, initw=200, inith=0)

        self.AddComboBox(NODETYPE, c4d.BFH_LEFT, 200, 13)

        self.AddChild(NODETYPE, NODE_RAMP,         "Ramp")
        self.AddChild(NODETYPE, NODE_TRIPLANAR,    "Triplanar")
        self.AddChild(NODETYPE, NODE_COLORCORR,    "Color Correct")
        self.AddChild(NODETYPE, NODE_CHANGERANGE,  "Change Range")
        self.AddChild(NODETYPE, NODE_COLORRANGE,   "Color Range")
        self.AddChild(NODETYPE, NODE_SCALARRAMP,   "Scalar Ramp")
        self.AddChild(NODETYPE, NODE_COLORLAYER,   "Color Layer")
        self.AddChild(NODETYPE, NODE_BUMPMAP,      "Bump Map")
        self.AddChild(NODETYPE, NODE_DISPLACEMENT, "Displacement")
        self.AddChild(NODETYPE, NODE_COLORAOV,     "Store Color to AOV")

        self.SetInt32(NODETYPE, 3001) # Set default node type

        self.GroupEnd()
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        # Buttons
        self.GroupBegin(GRP_BTNS, c4d.BFH_CENTER)
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        self.GroupEnd()
        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global options

        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw
        bc = c4d.BaseContainer() # Initialize a base container
        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Accept' button is pressed
            options = [self.GetInt32(PORTNUM), self.GetInt32(NODETYPE), True]
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            options = [self.GetInt32(PORTNUM), self.GetInt32(NODETYPE), True]
            self.Close() # Close dialog
        return True # Everything is fine

# Functions
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

def AddNode(nodeMaster):
    global options
    global ptnum

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
        ptnum = len(connections)

        if len(connections) == 0: return False

        portCount = lastNode.node.GetInPortCount()

        # -- Dialog --
        dlg = Dialog() # Create dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog

        if options[2] == False: return

        newNode = nodeMaster.CreateNode(root, 1036227, None, x = -1, y = -1) # Create a redshift node (RS)

        if options[1] == NODE_TRIPLANAR: #
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "TriPlanar" # Set to Triplanar node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.424, 0.392, 0.541) # Set node color
            inputPort = newNode.AddPort(c4d.GV_PORT_INPUT, 10000) #

        elif options[1] == NODE_RAMP: #
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSRamp" # Set to Ramp node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.663, 0.624, 0.424) # Set node color
            inputPort = newNode.AddPort(c4d.GV_PORT_INPUT, 10002) # (in port)

        elif options[1] == NODE_COLORCORR: #
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSColorCorrection" # Set to Color Correction node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.788, 0.557, 0.537) # Set node color
            inputPort = newNode.GetInPort(0) # (in port)
            bc  = newNode.GetDataInstance() # Get base container
            bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
            bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
            sy  = bcd.SetReal(109, 100) # Get y scale

        elif options[1] == NODE_CHANGERANGE:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSColorRange" # Set to Color Change Range node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.788, 0.557, 0.537) # Set node color
            inputPort = newNode.GetInPort(0) # (in port)
            bc  = newNode.GetDataInstance() # Get base container
            bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
            bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
            sy  = bcd.SetReal(109, 100) # Get y scale

        elif options[1] == NODE_COLORRANGE:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSMathRange" # Set to Change Range node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.537, 0.71, 0.569) # Set node color
            inputPort = newNode.GetInPort(0) # (in port)
            bc  = newNode.GetDataInstance() # Get base container
            bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
            bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
            sy  = bcd.SetReal(109, 100) # Get y scale

        elif options[1] == NODE_SCALARRAMP:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSScalarRamp" # Set to Scalar Ramp node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.663, 0.624, 0.424) # Set node color
            inputPort = newNode.AddPort(c4d.GV_PORT_INPUT, 10002) # (in port)

        elif options[1] == NODE_COLORLAYER:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "RSColorLayer" # Set to Color Change Range node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.788, 0.557, 0.537) # Set node color
            inputPort = newNode.GetInPort(0) # (in port)
            bc  = newNode.GetDataInstance() # Get base container
            bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
            bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
            sy  = bcd.SetReal(109, 100) # Get y scale

        elif options[1] == NODE_COLORAOV:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "StoreColorToAOV" # Set to Store Color To AOV node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.69, 0.663, 0.78) # Set node color
            inputPort = newNode.AddPort(c4d.GV_PORT_INPUT, 10001) # (in port)

        elif options[1] == NODE_BUMPMAP:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "BumpMap" # Set to Bump Map node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.345, 0.31, 0.459) # Set node color
            inputPort = newNode.AddPort(c4d.GV_PORT_INPUT, 10000) # (in port)

        elif options[1] == NODE_DISPLACEMENT:
            newNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "Displacement" # Set to Displacement node
            newNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.345, 0.31, 0.459) # Set node color
            inputPort = newNode.AddPort(c4d.GV_PORT_INPUT, 10000) # (in port)

        outputPort = newNode.GetOutPort(0)
        newNode.SetBit(c4d.BIT_ACTIVE) # Select node
        
        # Connections
        connections[options[0]][0].Connect(inputPort)
        outputPort.Connect(connections[options[0]][1])
        
        # Clean up
        #newNode.RemoveUnusedPorts()
        #newNode.GetDataInstance().GetContainerInstance(1001).GetContainerInstance(1000)[109] = 45

        # Position
        bc  = newNode.GetDataInstance() # Get base container
        bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
        bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
        sx  = bcd.GetReal(108) # Get x scale
        sy  = bcd.GetReal(109) # Get y scale

        px = u.MixNum(firstNode.px+firstNode.sx-sx, lastNode.px, 0.5)
        py = u.MixNum(firstNode.py, lastNode.py, 0.5)
        bcd.SetReal(100, px) # Set x position
        bcd.SetReal(101, py) # Set y position

def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    #try: # Try to execute following script
    # Redshift
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
            rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
            AddNode(rsnm) # Run the main function
    #except: # Otherwise
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()