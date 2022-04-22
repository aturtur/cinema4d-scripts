"""
AR_NodesRSQuickMatte

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodesRSQuickMatte
Version: 1.0
Description-US: Adds Redshift matte AOV to selected material(s) and object(s) and material tag(s).

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""

import c4d
import redshift
from c4d import gui

# Functions
def checkRedshiftMaterial(mat):
    if mat.GetType() == 1036224: # If Redshift material
        return mat
    else:
        return None

def CheckCustomAOV(vpRS, name):
    aovs = redshift.RendererGetAOVs(vpRS)
    for aov in aovs:
        if aov.GetParameter(c4d.REDSHIFT_AOV_TYPE) == 39:
            if aov.GetParameter(c4d.REDSHIFT_AOV_NAME) == name:
                return True
            else:
                return False
    return False

def CreateCustomAOV(vpRS, name):
    aovs = redshift.RendererGetAOVs(vpRS)
    aov = redshift.RSAOV()
    aov.SetParameter(c4d.REDSHIFT_AOV_TYPE, c4d.REDSHIFT_AOV_TYPE_CUSTOM)
    aov.SetParameter(c4d.REDSHIFT_AOV_ENABLED, True)
    aov.SetParameter(c4d.REDSHIFT_AOV_NAME, name)
    aovs.append(aov)
    return redshift.RendererSetAOVs(vpRS, aovs)

def CreateAOVNode(nodeMaster, name, outputNode):
    # Node generation
    root = nodeMaster.GetRoot() # Get node master root
    aovNode = nodeMaster.CreateNode(root, 1036227, outputNode, x = -1, y = -1) # Crete a Redshift node
    aovNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "StoreScalarToAOV" # Set Redshift node type to 'Scalar to AOV'
    aovNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.69, 0.663, 0.78) # Set node color

    beautyInput = aovNode.AddPort(c4d.GV_PORT_INPUT, 10000) # Beauty Input port
    aovInPort = aovNode.AddPort(c4d.GV_PORT_INPUT, 10001) # Aov 0 Input port
    portId = 1
    aovNode[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME0,c4d.REDSHIFT_AOVREF_NAME] = name

    return aovNode, beautyInput, aovInPort, portId

def CheckNode(node, nodeMaster, name, outputNode):
    if node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "StoreScalarToAOV":
        # check ports
        if node.AddPortIsOK(c4d.GV_PORT_INPUT, 10000) == True:
            beautyInput = node.AddPort(c4d.GV_PORT_INPUT, 10000) # Beauty Input port
        else:
            beautyInput = False

        if node.AddPortIsOK(c4d.GV_PORT_INPUT, 10001) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10001) # Aov 0 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME0,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 1
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10003) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10003) # Aov 1 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME1,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 2
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10005) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10005) # Aov 2 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME2,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 3
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10007) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10007) # Aov 3 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME3,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 4
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10009) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10009) # Aov 4 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME4,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 5
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10011) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10011) # Aov 5 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME5,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 6            
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10013) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10013) # Aov 6 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME6,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 7            
        elif node.AddPortIsOK(c4d.GV_PORT_INPUT, 10015) == True:
            aovInPort = node.AddPort(c4d.GV_PORT_INPUT, 10015) # Aov 7 Input port
            node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME7,c4d.REDSHIFT_AOVREF_NAME] = name
            portId = 8            
        else:
            node, beautyInput, aovInPort, portId = CreateAOVNode(nodeMaster, name, outputNode)
        return node, beautyInput, aovInPort, portId
    else:
        return CreateAOVNode(nodeMaster, name, outputNode)

def CheckMattes(node, name):
    if node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] == "StoreScalarToAOV":
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME0,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME1,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME2,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME3,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME4,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME5,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME6,c4d.REDSHIFT_AOVREF_NAME] == name: return None
        if node[c4d.REDSHIFT_SHADER_STORESCALARTOAOV_AOV_NAME7,c4d.REDSHIFT_AOVREF_NAME] == name: return None
    return True

def AddMatte(nodeMaster, vprs, name):
    root = nodeMaster.GetRoot() # Get node master root
    nodeMaster.AddUndo() # Add undo for changing nodes
    for node in root.GetChildren(): # Iterate through nodes
        opid = node.GetOperatorID() # Get operator ID
        if opid == 1036746: # If output
            outputNode = node # Get output node
            bc  = outputNode.GetData() # Get copy of base container
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER) # Get copy of shape container
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER) # Get copy of operator container
            px  = bcd.GetReal(100) # Get x position
            py  = bcd.GetReal(101) # Get y position
            sx  = bcd.GetReal(108) # Get x scale
            sy  = bcd.GetReal(109) # Get y scale
            outputInPort = outputNode.GetInPort(0)

    for node in root.GetChildren():
        for i in range(0, node.GetOutPortCount()):
            nodePort = node.GetOutPort(i)
            destinations = nodePort.GetDestination()
            for d in destinations:
                if d.GetNode().GetName() == "Output":
                    connectedPort = nodePort
                    connectedNode = nodePort.GetNode()

    if CheckMattes(connectedNode, name):
        aovNode, beautyInput, aovInPort, portId = CheckNode(connectedNode, nodeMaster, name, outputNode)
    else:
        return

    # Crete white color node
    constantNode = nodeMaster.CreateNode(root, 400001120, outputNode, x = -1, y = -1) # Crete a Constant node
    constantNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.537, 0.71, 0.569)# Set node color
    constantNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Set type to Vector
    constantNode[c4d.GV_CONST_VALUE] = c4d.Vector(1, 1, 1) # Set value to white

    # Connecting nodes
    if beautyInput != False:
        beautyInput.Connect(connectedPort)
    constantOutPort = constantNode.GetOutPort(0) # Get out port
    constantOutPort.Connect(aovInPort)
    aovNode.GetOutPort(0).Connect(outputInPort)

    # Check and create AOV
    checkAOV = CheckCustomAOV(vprs, name)
    if checkAOV == False:
        CreateCustomAOV(vprs, name)

def main():
    name = gui.InputDialog("Matte name", "") # Input dialog
    if name is None: return
    if name is "": return

    doc = c4d.documents.GetActiveDocument() # Get active document
    doc.StartUndo() # Start recording undos

    theList = [] # Collect all items for matte creation

    selection = doc.GetSelection() # Get active selection (objects and tags)

    for s in selection: # Loop through selected objects
        if not isinstance(s, c4d.BaseTag): # If object
            tags = s.GetTags() # Get object's tags
            for t in tags: # Loop through tags
                if isinstance(t, c4d.TextureTag): # If texture tag
                    mat = t[c4d.TEXTURETAG_MATERIAL] # Get material
                    m = checkRedshiftMaterial(mat)
                    theList.append(m)

        if isinstance(s, c4d.TextureTag): # If texture tag
            mat = s[c4d.TEXTURETAG_MATERIAL] # Get material
            m = checkRedshiftMaterial(mat)
            theList.append(m)

    materials = doc.GetMaterials() # Get materials
    for mat in materials: # Iterate through materials
        if mat.GetBit(c4d.BIT_ACTIVE): # If material is selected
            m = checkRedshiftMaterial(mat)
            theList.append(m)

    theList = [i for i in theList if i]  # Remove Nones
    finalList = [] # Init the final list for items
    names = [] # Init list for collecting material names
    for item in theList: # Iterate through the list
        if item.GetName() not in names:
            names.append(item.GetName())
            finalList.append(item)

    for item in finalList:
        renderdata = doc.GetActiveRenderData()
        vprs = redshift.FindAddVideoPost(renderdata, redshift.VPrsrenderer)
        if vprs is None:
            return
        rsnm = redshift.GetRSMaterialNodeMaster(item) # Get Redshift material node master
        AddMatte(rsnm, vprs, name) # Run the main function

    doc.EndUndo() # Stop recording undos

    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()