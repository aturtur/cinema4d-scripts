"""
AR_AverageLocator

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AverageLocator
Version: 1.0.0
Description-US: Creates a null object which position is average of selected objects/points

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.0.0 (03.03.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def CollectPoints(objects):
    pointList = [] # Init a list for objects and points
    for o in objects: # Iterate through objects
        points = o.GetPointS() # Get object's points
        pointCount = o.GetPointCount() # Get point count of object
        for i in range(pointCount): # Iterate through points
            if points.IsSelected(i): # If point is selected
                pointList.append([o, i]) # Add object and point index to the point list
    return pointList

def CreateAverageLocatorPoints(pointList):
    # Locator null setup
    locator = c4d.BaseObject(c4d.Onull) # Initialize a locator null
    locator.SetName("Locator") # Set name
    locator[c4d.NULLOBJECT_DISPLAY] = 1 # Set 'Shape' to 'Locator'
    locator[c4d.ID_BASELIST_ICON_FILE] = "1058512" # Set 'Icon'

    doc.InsertObject(locator, checknames=True) # Insert locator object to the document
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


    gap = 150
    y = 0

    mathNodes = []
    pointNodes = []

    # Create Xpresso nodes
    #for i, o in enumerate(objects): # Iterate through objects
    for i in range(len(pointList)):
        o = pointList[i][0] # Object
        p = pointList[i][1] # Point index

        #Point[c4d.GV_POINT_USE_DEFORMED]
        #Point[c4d.GV_POINT_INPUT_POINT]

        x = 0

        objectNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=x, y=y) # Create the node
        objectNode[c4d.GV_OBJECT_OBJECT_ID] = o # Reference object
        objectOutPort = objectNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_OBJECT_OUT, message=True)

        x += gap

        pointNode = nodeMaster.CreateNode(root, 400001112, None, x=x, y=y) # Create Point node
        pointNode[c4d.GV_POINT_USE_DEFORMED] = True
        pointNode[c4d.GV_POINT_INPUT_POINT] = p
        objectOutPort.Connect(pointNode.GetInPort(0)) # Connect Object node to Point node
        pointNodes.append(pointNode)

        # Math:Add nodes
        if i != 0:
            mathNode = nodeMaster.CreateNode(root, 400001121, None, x=gap*(i+1), y=0) # Create Math node
            mathNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Vector
            mathNodes.append(mathNode)

        #x += 200
        y += 150

    if len(pointNodes) > 1:
        mulNode = nodeMaster.CreateNode(root, 400001121, None, x=gap*(len(pointNodes)+1), y=0) # Create Math node
        mulNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Vector
        mulNode[c4d.GV_MATH_FUNCTION_ID] = 2 # Multiply
        d = 1.0/len(pointNodes)
        # https://plugincafe.maxon.net/topic/10477/13926_changing-math-node-input-value-xpresso/3
        lv1 = c4d.DescLevel(2000, c4d.DTYPE_SUBCONTAINER, 0)
        lv2 = c4d.DescLevel(1001, c4d.DTYPE_DYNAMIC, 0)
        mulNode.SetParameter(c4d.DescID(lv1, lv2), c4d.Vector(d,d,d), c4d.DESCFLAGS_SET_0)
        
    v2mNode = nodeMaster.CreateNode(root, 400001110, None, x=gap*(len(pointNodes)+2), y=0) # Create the node
    v2mNode[c4d.GV_VECT2MATRIX_V1] = c4d.Vector(1,0,0)
    v2mNode[c4d.GV_VECT2MATRIX_V2] = c4d.Vector(0,1,0)
    v2mNode[c4d.GV_VECT2MATRIX_V3] = c4d.Vector(0,0,1)

    locatorNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=gap*(len(pointNodes)+3), y=0) # Create the node
    locatorNode[c4d.GV_OBJECT_OBJECT_ID] = locator
    locatorInPort = locatorNode.AddPort(c4d.GV_PORT_INPUT, c4d.GV_OBJECT_OPERATOR_GLOBAL_IN, message=True)

    # Connect Xpresso nodes
    if len(pointNodes) > 1:
        for i in range(len(pointNodes)): # Iterate through objects
            if i == 0:
                pointNodes[i].GetOutPort(1).Connect(mathNodes[i].GetInPort(0))
            elif i < len(mathNodes):
                pointNodes[i].GetOutPort(1).Connect(mathNodes[i-1].GetInPort(1))
                mathNodes[i-1].GetOutPort(0).Connect(mathNodes[i].GetInPort(0))
            elif i == len(mathNodes):
                pointNodes[i].GetOutPort(1).Connect(mathNodes[i-1].GetInPort(1))
        mathNodes[-1].GetOutPort(0).Connect(mulNode.GetInPort(0))
        mulNode.GetOutPort(0).Connect(v2mNode.GetInPort(0))
    else:
        pointNode.GetOutPort(1).Connect(v2mNode.GetInPort(0))
    v2mNode.GetOutPort(0).Connect(locatorInPort)

    #
    c4d.modules.graphview.RedrawMaster(nodeMaster) # Update xpresso
    
    return locator
    pass


def CreateAverageLocatorObjects(objects):

    # Locator null setup
    locator = c4d.BaseObject(c4d.Onull) # Initialize a locator null
    locator.SetName("Locator") # Set name
    locator[c4d.NULLOBJECT_DISPLAY] = 1 # Set 'Shape' to 'Locator'
    locator[c4d.ID_BASELIST_ICON_FILE] = "1058512" # Set 'Icon'

    doc.InsertObject(locator, checknames=True) # Insert locator object to the document
    # Importat to insert it before creating object nodes in xpresso tag!

    # Priority data setup
    prioritydata = c4d.PriorityData() # Initialize a priority data
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 10) # Set priority value to last possible value
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false

    # Xpresso tag setup
    xpTag = c4d.BaseTag(c4d.Texpresso) # Initialize xpresso tag
    xpTag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set prioritydata
    locator.InsertTag(xpTag) # Insert xpresso tag to locator
    nodeMaster = xpTag.GetNodeMaster() # Get xpresso tag's nodemaster
    root = nodeMaster.GetRoot() # Get xpresso root


    gap = 150
    y = 0

    mathNodes = []
    matrixNodes = []

    # Create Xpresso nodes
    for i, o in enumerate(objects): # Iterate through objects

        x = 0

        objectNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=x, y=y) # Create the node
        objectNode[c4d.GV_OBJECT_OBJECT_ID] = o # Reference object
        objectOutPort = objectNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_GLOBAL_OUT, message=True)

        x += gap

        matrixNode = nodeMaster.CreateNode(root, 400001109, None, x=x, y=y) # Create Matrix2Vectors node
        objectOutPort.Connect(matrixNode.GetInPort(0)) # Connect Object node to Matrix2Vectors node
        matrixNodes.append(matrixNode)

        # Math:Add nodes
        if i != 0:
            mathNode = nodeMaster.CreateNode(root, 400001121, None, x=gap*(i+1), y=0) # Create Math node
            mathNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Vector
            mathNodes.append(mathNode)

        #x += 200
        y += 150

    if len(objects) > 1:
        mulNode = nodeMaster.CreateNode(root, 400001121, None, x=gap*(len(objects)+1), y=0) # Create Math node
        mulNode[c4d.GV_DYNAMIC_DATATYPE] = 23 # Vector
        mulNode[c4d.GV_MATH_FUNCTION_ID] = 2 # Multiply
        d = 1.0/len(objects)
        # https://plugincafe.maxon.net/topic/10477/13926_changing-math-node-input-value-xpresso/3
        lv1 = c4d.DescLevel(2000, c4d.DTYPE_SUBCONTAINER, 0)
        lv2 = c4d.DescLevel(1001, c4d.DTYPE_DYNAMIC, 0)
        mulNode.SetParameter(c4d.DescID(lv1, lv2), c4d.Vector(d,d,d), c4d.DESCFLAGS_SET_0)
        
    v2mNode = nodeMaster.CreateNode(root, 400001110, None, x=gap*(len(objects)+2), y=0) # Create the node
    v2mNode[c4d.GV_VECT2MATRIX_V1] = c4d.Vector(1,0,0)
    v2mNode[c4d.GV_VECT2MATRIX_V2] = c4d.Vector(0,1,0)
    v2mNode[c4d.GV_VECT2MATRIX_V3] = c4d.Vector(0,0,1)

    locatorNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=gap*(len(objects)+3), y=0) # Create the node
    locatorNode[c4d.GV_OBJECT_OBJECT_ID] = locator
    locatorInPort = locatorNode.AddPort(c4d.GV_PORT_INPUT, c4d.GV_OBJECT_OPERATOR_GLOBAL_IN, message=True)

    # Connect Xpresso nodes
    if len(objects) > 1:
        for i, o in enumerate(objects): # Iterate through objects
            if i == 0:
                matrixNodes[i].GetOutPort(0).Connect(mathNodes[i].GetInPort(0))
            elif i < len(mathNodes):
                matrixNodes[i].GetOutPort(0).Connect(mathNodes[i-1].GetInPort(1))
                mathNodes[i-1].GetOutPort(0).Connect(mathNodes[i].GetInPort(0))
            elif i == len(mathNodes):
                matrixNodes[i].GetOutPort(0).Connect(mathNodes[i-1].GetInPort(1))
        mathNodes[-1].GetOutPort(0).Connect(mulNode.GetInPort(0))
        mulNode.GetOutPort(0).Connect(v2mNode.GetInPort(0))
    else:
        matrixNode.GetOutPort(0).Connect(v2mNode.GetInPort(0))
    v2mNode.GetOutPort(0).Connect(locatorInPort)

    #
    c4d.modules.graphview.RedrawMaster(nodeMaster) # Update xpresso
    
    return locator
    pass

def main():
    editorMode = doc.GetMode()

    selection = []

    if editorMode == c4d.Mpoints: # Point edit mode
        selection = doc.GetActiveObjects(0) # Get selected objects
        pointList = CollectPoints(selection)
        locator = CreateAverageLocatorPoints(pointList)
        locator.SetBit(c4d.BIT_ACTIVE)
        pass

    #elif editorMode == c4d.Mpolygons: # Polygon edit mode
    #    pass

    elif (editorMode == c4d.Mobject) or (editorMode == c4d.Mmodel): # Object mode or model mode
        selection = doc.GetActiveObjects(0) # Get selected objects
        locator = CreateAverageLocatorObjects(selection)
        locator.SetBit(c4d.BIT_ACTIVE)
        pass

    if len(selection) > 0:
        for s in selection:
            doc.AddUndo(c4d.UNDOTYPE_BITS, s)
            s.DelBit(c4d.BIT_ACTIVE)

    c4d.EventAdd()
    pass

# Execute main
if __name__ == '__main__':
    main()