"""
AR_NodeTexToMat

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodeTexToMat
Version: 1.0.2
Description-US: Creates material node from selected texture nodes (Only for Redshift).

Notice: Make sure the Redshift material is selected when using the script!

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.2 (19.10.2023) - Update for Cinema 4D 2024
1.0.1 (03.04.2024) - Bug fixes
1.0.0 (19.05.2022) - First version

https://help.poliigon.com/en/articles/1712652-what-are-the-different-texture-maps-for

"""

# Libraries
import c4d
from pathlib import Path
import re
import os
import sys
try:
    import redshift
except:
    pass

from operator import attrgetter
from c4d import utils as u
from c4d import gui
from c4d.gui import GeDialog
from c4d import storage


# Variables
GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_BTNS        = 1002
GRP_VAL         = 1003
GRP_COL         = 1004

PORTNUM         = 2001
NODETYPE        = 2002

TXT_MAT         = 2999 # Material
COM_MAT         = 3000 # Combo

MAT_RSMAT       = 4000
MAT_RSSTD       = 4001

TXT_COL         = 3001 # Color
EDT_COL         = 3002

TXT_ROUGH       = 3003 # Roughness
EDT_ROUGH       = 3004

TXT_GLOSS       = 3017 # Glossiness
EDT_GLOSS       = 3018

TXT_NORM        = 3005 # Normal
EDT_NORM        = 3006

TXT_HEIGHT      = 3007 # Height
EDT_HEIGHT      = 3008

TXT_DISP        = 3009 # Displacement
EDT_DISP        = 3010

TXT_METAL       = 3011 # Metalness
EDT_METAL       = 3012

TXT_OPACITY     = 3013 # Opacity
EDT_OPACITY     = 3014

TXT_EMISSION    = 3015 # Emission
EDT_EMISSION    = 3016

BTN_OK          = 7001
BTN_CANCEL      = 7002

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
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw

        options = loadSettings() # Load settings

        self.SetTitle("Texture Lookups") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=300, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------

        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=1, groupflags=1, initw=300, inith=0)

        self.AddStaticText(TXT_MAT, c4d.BFH_LEFT, name="Material")
        self.AddComboBox(COM_MAT, c4d.BFH_LEFT, initw=250, inith=13)
        self.AddChild(COM_MAT, MAT_RSMAT, "RS Material")
        self.AddChild(COM_MAT, MAT_RSSTD, "RS Standard")

        self.AddStaticText(TXT_COL, c4d.BFH_LEFT, name="Color")
        self.AddEditText(EDT_COL, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_ROUGH, c4d.BFH_LEFT, name="Roughness")
        self.AddEditText(EDT_ROUGH, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_GLOSS, c4d.BFH_LEFT, name="Glossiness")
        self.AddEditText(EDT_GLOSS, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_NORM, c4d.BFH_LEFT, name="Normal")
        self.AddEditText(EDT_NORM, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_HEIGHT, c4d.BFH_LEFT, name="Height")
        self.AddEditText(EDT_HEIGHT, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_DISP, c4d.BFH_LEFT, name="Displacement")
        self.AddEditText(EDT_DISP, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_METAL, c4d.BFH_LEFT, name="Metalness")
        self.AddEditText(EDT_METAL, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_OPACITY, c4d.BFH_LEFT, name="Opacity")
        self.AddEditText(EDT_OPACITY, c4d.BFH_LEFT, initw=250, inith=13)

        self.AddStaticText(TXT_EMISSION, c4d.BFH_LEFT, name="Emission")
        self.AddEditText(EDT_EMISSION, c4d.BFH_LEFT, initw=250, inith=13)

        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        # Buttons
        self.GroupBegin(GRP_BTNS, c4d.BFH_CENTER)
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Save") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        self.GroupEnd()

        # ----------------------------------------------------------------------------------------
        # Set values
        self.SetInt32(COM_MAT,      int(options['material']))
        self.SetString(EDT_COL,     str(options['color']))
        self.SetString(EDT_ROUGH,   str(options['roughness']))
        self.SetString(EDT_NORM,    str(options['normal']))
        self.SetString(EDT_HEIGHT,  str(options['height']))
        self.SetString(EDT_DISP,    str(options['displacement']))
        self.SetString(EDT_METAL,   str(options['metal']))
        self.SetString(EDT_OPACITY, str(options['opacity']))
        self.SetString(EDT_GLOSS,   str(options['glossiness']))
        self.SetString(EDT_GLOSS,   str(options['emission']))

        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global options

        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw
        bc = c4d.BaseContainer() # Initialize a base container

        # Set options
        options = {}
        options['material']    = self.GetInt32(COM_MAT)
        options['color']       = self.GetString(EDT_COL)
        options['roughness']   = self.GetString(EDT_ROUGH)
        options['glossiness']  = self.GetString(EDT_GLOSS)
        options['normal']      = self.GetString(EDT_NORM)
        options['height']      = self.GetString(EDT_HEIGHT)
        options['displacement']= self.GetString(EDT_DISP)
        options['metal']       = self.GetString(EDT_METAL)
        options['opacity']     = self.GetString(EDT_OPACITY)
        options['emission']    = self.GetString(EDT_EMISSION)

        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog

        if paramid == BTN_OK: # If 'Accept' button is pressed
            # Save options
            saveSettings(options)
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            # Save options
            saveSettings(options)

            self.Close() # Close dialog
        return True # Everything is fine

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

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_NodeTexToMat.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("4000\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n") # Default settings
        f.close()
    return filePath

def loadSettings():
    optionsFile = CheckFiles()
    f = open(optionsFile) # Open the file for reading

    optionsArray = [] # Initialize an array for options
    for line in f: # Iterate through every row
        line = line.rstrip('\n') # Strip newline stuff
        optionsArray.append(line)
    f.close() # Close the file
    options = {
        'material'    : int(optionsArray[0]),
        'color'       : str(optionsArray[1]),
        'normal'      : str(optionsArray[2]),
        'height'      : str(optionsArray[3]),
        'displacement': str(optionsArray[4]),
        'roughness'   : str(optionsArray[5]),
        'glossiness'  : str(optionsArray[6]),
        'opacity'     : str(optionsArray[7]),
        'metal'       : str(optionsArray[8]),
        'emission'    : str(optionsArray[9])
    }
    return options

def saveSettings(options):
    #path, fn = os.path.split(__file__)
    #optionsFile = os.path.join(path, "AR_Folder.txt")
    optionsFile = CheckFiles() #

    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile, 'w') # Open the file for writing
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"), 'w') # Open the file for writing

    settings = [str(options['material']),
                str(options['color']),
                str(options['normal']),
                str(options['height']),
                str(options['displacement']),
                str(options['roughness']),
                str(options['glossiness']),
                str(options['opacity']),
                str(options['metal']),
                str(options['emission'])]

    settings = "\n".join(settings) # Create a string from an array
    f.write(settings+"\n") # Write settings to the file
    f.close() # Close the file
    return True # Everything is fine

def StringToMaps(string):
    if string != "" or string != " ":
        string = string.replace(" ", "") # Remove white spaces
        maps = string.split(",") # Split string to list by comma (",")
        return maps
    else:
        return None

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

def SearchMap(node, path, maps):
    if path == "":
        return None
    if len(maps) == 0 and maps == None:
        return None
    for m in maps:
        if m != "" and m != " ":
            found = re.search("(?<![^\\W_])"+m+"(?![^\\W_])", path)
            if found:
                return node
    return None

def NodeSetPosition(node, x, y):
    bc  = node.GetDataInstance() # Get base container
    bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
    bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container
    #sx  = bcd.GetReal(108) # Get x scale
    #sy  = bcd.GetReal(109) # Get y scale
    bcd.SetReal(100, x) # Set x position
    bcd.SetReal(101, y) # Set y position
    return True

def NodeAddInPort(node, portid):
    if node.AddPortIsOK(c4d.GV_PORT_INPUT, portid):
        port = node.AddPort(c4d.GV_PORT_INPUT, portid)
    else:
        ports = node.GetInPorts()
        for p in ports:
            if p.GetMainID() == portid:
                port = p
    return port

def AddPorts(material, outputNode, x, colorMap, roughMap, glossMap, normalMap, heightMap, dispMap, opacityMap, metalMap, emissionMap):

    # Port IDs
    diffusePortID     = 10000
    reflRoughPortID   = 10007

    if material[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "Material":
        matType = MAT_RSMAT
    elif material[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "StandardMaterial":
        matType = MAT_RSSTD

    if matType == MAT_RSMAT:
        bumpPortID    = 10062
        metalPortID   = 10017
        opacityPortID = 10059
        emissionPortID= 10060

    elif matType == MAT_RSSTD:
        bumpPortID    = 10046
        metalPortID   = 10004
        opacityPortID = 10044
        emissionPortID= 10042

    dispPortID        = 10001

    space = 50

    # -------------------------------------------------------------------------------------------------------
    nodeMaster = material.GetNodeMaster()
    root = nodeMaster.GetRoot() # Get node master root

    if colorMap:
        colorInPort = NodeAddInPort(material, diffusePortID)
        colorMap.node.GetOutPort(0).Connect(colorInPort)

    if glossMap:
        glossInPort = NodeAddInPort(material, reflRoughPortID)
        glossMap.node.GetOutPort(0).Connect(glossInPort)

        # Convert from glossiness to roughness
        if matType == MAT_RSSTD:
            material[c4d.REDSHIFT_SHADER_STANDARDMATERIAL_REFL_ISGLOSSINESS] = True
        elif matType == MAT_RSMAT:
            material[c4d.REDSHIFT_SHADER_MATERIAL_REFL_ISGLOSSINESS] = True

    if roughMap:
        roughInPort = NodeAddInPort(material, reflRoughPortID)
        roughMap.node.GetOutPort(0).Connect(roughInPort)

        # Convert from glossiness to roughness
        if matType == MAT_RSSTD:
            material[c4d.REDSHIFT_SHADER_STANDARDMATERIAL_REFL_ISGLOSSINESS] = False
        elif matType == MAT_RSMAT:
            material[c4d.REDSHIFT_SHADER_MATERIAL_REFL_ISGLOSSINESS] = False

    if opacityMap:
        opacityInPort = NodeAddInPort(material, opacityPortID)
        opacityMap.node.GetOutPort(0).Connect(opacityInPort)

    if normalMap:
        normalInPort = NodeAddInPort(material, bumpPortID)
        bumpMap = nodeMaster.CreateNode(root, 1036227, normalMap.node, x = -1, y = -1)
        bumpMap[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "BumpMap"
        bumpMap[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.345, 0.31, 0.459)
        bumpMap[c4d.REDSHIFT_SHADER_BUMPMAP_INPUTTYPE] = 1 # Tangent-Space Normal
        bumpMapInPort = bumpMap.AddPort(c4d.GV_PORT_INPUT, 10000)
        normalMap.node.GetOutPort(0).Connect(bumpMapInPort)
        bumpMap.GetOutPort(0).Connect(normalInPort)

        NodeSetPosition(bumpMap,normalMap.px + normalMap.sx + space, normalMap.py)

    if heightMap:
        heightInPort = NodeAddInPort(material, bumpPortID)
        bumpMap = nodeMaster.CreateNode(root, 1036227, heightMap.node, x = -1, y = -1)
        bumpMap[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "BumpMap"
        bumpMap[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.345, 0.31, 0.459)
        bumpMap[c4d.REDSHIFT_SHADER_BUMPMAP_INPUTTYPE] = 0 # Height Field
        bumpMapInPort = bumpMap.AddPort(c4d.GV_PORT_INPUT, 10000)
        heightMap.node.GetOutPort(0).Connect(bumpMapInPort)
        bumpMap.GetOutPort(0).Connect(heightInPort)

        NodeSetPosition(bumpMap, heightMap.px + heightMap.sx + space, heightMap.py)

    if metalMap:
        if matType == MAT_RSMAT:
            material[c4d.REDSHIFT_SHADER_MATERIAL_REFL_FRESNEL_MODE] = 2 # Set 'Fresnel Type' to 'Metalness'
        metalInPort = NodeAddInPort(material, metalPortID)
        metalMap.node.GetOutPort(0).Connect(metalInPort)

    if dispMap:
        if outputNode:
            dispInPort = NodeAddInPort(outputNode, dispPortID)
            dispMapN = nodeMaster.CreateNode(root, 1036227, dispMap.node, x = -1, y = -1)
            dispMapN[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "Displacement"
            dispMapN[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.345, 0.31, 0.459)
            dispMapN[c4d.REDSHIFT_SHADER_BUMPMAP_INPUTTYPE] = 0 # Height Field
            dispMapInPort = dispMapN.AddPort(c4d.GV_PORT_INPUT, 10000)
            dispMap.node.GetOutPort(0).Connect(dispMapInPort)
            dispMapN.GetOutPort(0).Connect(dispInPort)

        NodeSetPosition(dispMapN, dispMap.px + dispMap.sx + space, dispMap.py)

    if emissionMap:
        emissionInPort = NodeAddInPort(material, emissionPortID)

        if matType == MAT_RSMAT:
            material[c4d.REDSHIFT_SHADER_MATERIAL_EMISSION_WEIGHT] = 1.0
        elif matType == MAT_RSSTD:
            material[c4d.REDSHIFT_SHADER_STANDARDMATERIAL_EMISSION_WEIGHT] = 1.0
        emissionMap.node.GetOutPort(0).Connect(emissionInPort)

    # -----------------------------------------------------------------------------------------------------------

def CreateTexToMat(nodeMaster):
    global options

    nodes = [] # Initialize a list
    materialNodes = [] # Initialize a list for material nodes
    root = nodeMaster.GetRoot() # Get node master root
    nodeMaster.AddUndo() # Add undo for changing nodes
    outputNode = None

    for node in root.GetChildren(): # Iterate through nodes

        if node.GetOperatorID() == 1036746: # If output node
            outputNode = node

        if node.GetBit(c4d.BIT_ACTIVE): # If node is selected
            bc  = node.GetDataInstance() # Get copy of base container
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER) # Get copy of shape container
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER) # Get copy of operator container
            px  = bcd.GetReal(100) # Get x position
            py  = bcd.GetReal(101) # Get y position
            sx  = bcd.GetReal(108) # Get x scale
            sy  = bcd.GetReal(109) # Get y scale
            nodes.append(nodeObject(node, px, py, sx, sy)) # Create nodeObject and add it to a list

            if node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "Material" or node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "StandardMaterial": # Node is a material
                materialNodes.append(nodeObject(node, px, py, sx, sy))

    if nodes: # If there are nodes
        firstNode = min(nodes, key=attrgetter('py')) # Get the node with the minimum y position value
        lastNode  = max(nodes, key=attrgetter('py')) # Get the node with the maximum y position value

        # Arrays
        colors    = StringToMaps(options['color'])
        normals   = StringToMaps(options['normal'])
        heights   = StringToMaps(options['height'])
        disps     = StringToMaps(options['displacement'])
        roughs    = StringToMaps(options['roughness'])
        glosses   = StringToMaps(options['glossiness'])
        opacities = StringToMaps(options['opacity'])
        metals    = StringToMaps(options['metal'])
        emissions = StringToMaps(options['emission'])

        # Maps
        colorMap   = None
        roughMap   = None
        glossMap   = None
        normalMap  = None
        heightMap  = None
        dispMap    = None
        opacityMap = None
        metalMap   = None
        emissionMap= None

        for n in nodes: # Iterate through collected nodes
            if n.node.GetOperatorID() == 1036227:
                if n.node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "TextureSampler": # Node is a texture node
                    path = n.node[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0, c4d.REDSHIFT_FILE_PATH] # Get file path
                    name = Path(path).stem

                    if not colorMap:
                        colorMap   = SearchMap(n, path, colors)

                    if not normalMap:
                        normalMap  = SearchMap(n, path, normals)

                    if not heightMap:
                        heightMap  = SearchMap(n, path, heights)

                    if not dispMap:
                        dispMap    = SearchMap(n, path, disps)

                    if not opacityMap:
                        opacityMap = SearchMap(n, path, opacities)

                    if not roughMap:
                        roughMap   = SearchMap(n, path, roughs)

                    if not glossMap:
                        glossMap   = SearchMap(n, path, glosses)

                    if not metalMap:
                        metalMap   = SearchMap(n, path, metals)

                    if not metalMap:
                        metalMap   = SearchMap(n, path, metals)

                    if not emissionMap:
                        emissionMap= SearchMap(n, path, emissions)

        # Checking stuff
        allMaps = [colorMap,
                   roughMap,
                   glossMap,
                   normalMap,
                   heightMap,
                   dispMap,
                   opacityMap,
                   dispMap,
                   opacityMap,
                   metalMap,
                   emissionMap]
        dontCreateMat = not any(allMaps)
        if dontCreateMat: return None

        x = firstNode.px + firstNode.sx + 250
        # -----------------------------------------------------------------------------------------------------------
        if len(materialNodes) > 0: # If selected material nodes found
            for matNode in materialNodes: # Iterate through material nodes
                m = matNode.node
                AddPorts(m, outputNode, x, colorMap, roughMap, glossMap, normalMap, heightMap, dispMap, opacityMap, metalMap, emissionMap)
        # -----------------------------------------------------------------------------------------------------------
        else: # No selected material nodes found, create new material
            material = nodeMaster.CreateNode(root, 1036227, x = -1, y = -1)
            if options['material'] == MAT_RSMAT: # If RS Material
                material[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "Material"
            elif options['material'] == MAT_RSSTD: # If RS Standard
                material[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "StandardMaterial"
            material[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.529, 0.345, 0.333)
            # -----------------------------------------------------------------------------------------------------------
            AddPorts(material, outputNode, x, colorMap, roughMap, glossMap, normalMap, heightMap, dispMap, opacityMap, metalMap, emissionMap)
            NodeSetPosition(material, x, u.MixNum(firstNode.py, lastNode.py, 0.5))
            # -----------------------------------------------------------------------------------------------------------

def main():
    global options
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    #try: # Try to execute following script
    # Redshift
    if keyMod == "None":
        options = loadSettings() # Load settings
        for m in materials: # Iterate through materials
            if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                CreateTexToMat(rsnm) # Run the main function
    elif keyMod == "Alt+Ctrl+Shift":
        dlg = Dialog() # Create dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog

    #except: # Otherwise
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()