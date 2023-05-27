"""
AR_AlignNullToPolygon

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AlignNullToPolygon
Version: 1.1.0
Description-US: Creates a null object(s) which is aligned to selected polygon(s)

Written for Maxon Cinema 4D 2023.2.1
Python version 3.10.8

Change log:
1.1.0 (27.05.2023) - Support for multiple object selections and polygon selections
1.0.0 (25.05.2023) - Initial realease
"""

# Libraries
import c4d

def AlignNullToPolygon(obj):
    nulls = [] # Initialize list for nulls
    polys = obj.GetPolygonS() # Get polygons
    polyCount = obj.GetPolygonCount() # Get object's polygon count
    for i in range(0, polyCount): # Iterate through polygons
        if polys.IsSelected(i): # Polygon is selected
            polyIndex = i # Set polygon index
            null = CreateNullSetup(obj, polyIndex) # Create align null to polygon rig
            nulls.append(null) # Add rigged null to list
    return nulls # Return nulls

def CreateNullSetup(obj, polyIndex):

    # Null setup
    locator = c4d.BaseObject(c4d.Onull) # Initialize a null
    locator.SetName("Null_"+obj.GetName()+"_Poly"+str(polyIndex)) # Set name
    locator[c4d.NULLOBJECT_DISPLAY] = 6 # Set 'Shape' to 'Pentagon'
    locator[c4d.ID_BASELIST_ICON_FILE] = "1058517" # Set 'Icon' to pentagon
    locator[c4d.NULLOBJECT_ORIENTATION] = 1 # Set orientation to Z

    locator.InsertBefore(obj) # Insert null object to the document
    # Important to insert it before creating object nodes in xpresso tag!

    # Priority data setup
    prioritydata = c4d.PriorityData() # Initialize a priority data
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 10) # Set priority value
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false

    # Xpresso tag setup
    xpTag = c4d.BaseTag(c4d.Texpresso) # Initialize xpresso tag
    xpTag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set prioritydata
    locator.InsertTag(xpTag) # Insert xpresso tag to locator
    nodeMaster = xpTag.GetNodeMaster() # Get xpresso tag's nodemaster
    root = nodeMaster.GetRoot() # Get xpresso root

    # Create Xpresso nodes

    # Source object node
    objectNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=0, y=0) # Create the node
    objectNode[c4d.GV_OBJECT_OBJECT_ID] = obj # Reference object
    objectOutPort = objectNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_OBJECT_OUT, message=True)

    # Polygon node
    polygonNode = nodeMaster.CreateNode(root, 400001140, None, x=150, y=0) # Create Polygon node
    polygonNode[c4d.GV_POLY_MODE] = 100 # Global
    polygonNode[c4d.GV_POLY_USE_DEFORMED] = True # Use deformed points
    polygonNode[c4d.GV_POLY_INPUT_POLY] = polyIndex # Polygon index
    polyCenterPort = polygonNode.AddPort(c4d.GV_PORT_OUTPUT, 3005, True) # Add port polygon center
    polyPointAPort = polygonNode.AddPort(c4d.GV_PORT_OUTPUT, 3001, True) # Add port Index Point 1
    polyPointBPort = polygonNode.AddPort(c4d.GV_PORT_OUTPUT, 3002, True) # Add port Index Point 2
    polyPointCPort = polygonNode.AddPort(c4d.GV_PORT_OUTPUT, 3003, True) # Add port Index Point 3
    objectOutPort.Connect(polygonNode.GetInPort(0)) # Connect Object node to Point node

    # Point nodes
    pointNodeA = nodeMaster.CreateNode(root, 400001112, None, x=400, y=100) # Create Point node
    pointNodeA[c4d.GV_POINT_USE_DEFORMED] = False
    pointNodeA[c4d.GV_POINT_INPUT_POINT] = 0
    objectOutPort.Connect(pointNodeA.GetInPort(0)) # Connect Object node to Point node
    polyPointAPort.Connect(pointNodeA.GetInPort(1)) # Connect Polygon node to Point node

    pointNodeB = nodeMaster.CreateNode(root, 400001112, None, x=400, y=200) # Create Point node
    pointNodeB[c4d.GV_POINT_USE_DEFORMED] = False
    pointNodeB[c4d.GV_POINT_INPUT_POINT] = 0
    objectOutPort.Connect(pointNodeB.GetInPort(0)) # Connect Object node to Point node
    polyPointBPort.Connect(pointNodeB.GetInPort(1)) # Connect Polygon node to Point node

    pointNodeC = nodeMaster.CreateNode(root, 400001112, None, x=400, y=300) # Create Point node
    pointNodeC[c4d.GV_POINT_USE_DEFORMED] = False
    pointNodeC[c4d.GV_POINT_INPUT_POINT] = 0
    objectOutPort.Connect(pointNodeC.GetInPort(0)) # Connect Object node to Point node
    polyPointCPort.Connect(pointNodeC.GetInPort(1)) # Connect Polygon node to Point node

    # Python node
    pythonNode = nodeMaster.CreateNode(root, 1022471, None, x=600, y=0) # Create Python node
    # Remove default ports
    defaultPythonInPorts = pythonNode.GetInPorts()
    pythonNode.RemovePort(defaultPythonInPorts[0])
    pythonNode.RemovePort(defaultPythonInPorts[1])
    defaultPythonOutPorts = pythonNode.GetOutPorts()
    pythonNode.RemovePort(defaultPythonOutPorts[0])
    # Add new ports and rename those
    pyInPosPort = pythonNode.AddPort(c4d.GV_PORT_INPUT, (4007, 400007004, 1022471)) # Vector Input
    pyInPosPort.SetName("Position")
    pyInPointAPort = pythonNode.AddPort(c4d.GV_PORT_INPUT, (4007, 400007004, 1022471)) # Vector Input
    pyInPointAPort.SetName("Point0")
    pyInPointBPort = pythonNode.AddPort(c4d.GV_PORT_INPUT, (4007, 400007004, 1022471)) # Vector Input
    pyInPointBPort.SetName("Point1")
    pyInPointCPort = pythonNode.AddPort(c4d.GV_PORT_INPUT, (4007, 400007004, 1022471)) # Vector Input
    pyInPointCPort.SetName("Point2")
    pyOutMatrixPort = pythonNode.AddPort(c4d.GV_PORT_OUTPUT, (4016, 400007006, 1022471)) # Matrix Output
    # Connect ports
    polyCenterPort.Connect(pyInPosPort)
    pointNodeA.GetOutPort(1).Connect(pyInPointAPort)
    pointNodeB.GetOutPort(1).Connect(pyInPointBPort)
    pointNodeC.GetOutPort(1).Connect(pyInPointCPort)
    # Python script
    pythonNode[c4d.GV_PYTHON_CODE] = "import c4d\n\
import math\n\
def main():\n\
    global Matrix\n\
    v1 = Point1 - Point0 # Generate first vector from two point positions\n\
    v2 = Point2 - Point0 # Generate second vector from two point positions\n\
    m = c4d.Matrix() # Initialize a matrix\n\
    m.v1 = v1.GetNormalized()\n\
    m.v3 = v1.Cross(v2).GetNormalized()\n\
    m.v2 = m.v3.Cross(v1).GetNormalized()\n\
    m.off = Position # Set position\n\
    Matrix = m # Output"

    # Target object node
    nullNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=800, y=0) # Create the node
    nullNode[c4d.GV_OBJECT_OBJECT_ID] = locator # Reference object
    nullInPort = nullNode.AddPort(c4d.GV_PORT_INPUT, 30000001) # Global Matrix input
    nullInPort.Connect(pyOutMatrixPort)

    #
    c4d.modules.graphview.RedrawMaster(nodeMaster) # Update xpresso
    return locator

def main():
    objs = doc.GetActiveObjects(1) # Get active objects
    nulls = [] # Initialize list for nulls
    for obj in objs: # Iterate through selected objects
        nulls.extend(AlignNullToPolygon(obj)) # Get nulls
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo step for deselecting obj
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect object
    for null in nulls: # Iterate through nulls
        null.SetBit(c4d.BIT_ACTIVE) # Select null
    doc.SetMode(c4d.Mmodel) # Set editor mode to model
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main
if __name__ == '__main__':
    main()