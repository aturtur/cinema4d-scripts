"""
AR_CreateControlNulls

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateControlNulls
Description-US: Create control null objects from selected points
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import utils as u

# Functions
def GetGlobalPosition(obj): # Get object's global position
    return obj.GetMg().off

def GetGlobalRotation(obj): # Get object's global rotation
    return u.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj): # Get object's global scale
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalPosition(obj, pos): # Set object's global position
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot): # Set object's global rotation
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector(m.v1.GetLength(),
                       m.v2.GetLength(),
                       m.v3.GetLength())
    m = u.HPBToMatrix(rot)
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SetGlobalScale(obj, scale): # Set object's global scale
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None): # Create User Data Link
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_DEFAULT] = link
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup  
    element = obj.AddUserData(bc)
    obj[element] = link
    return element

def CreateControlNulls(obj):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    points = obj.GetPointS() # Get object's points
    pointCount = obj.GetPointCount() # Get point count of object
    parentNull = c4d.BaseObject(c4d.Onull) # Initialize parent null object
    parentNull.SetName(str(obj.GetName()) + " Control Points") # Set parent null's name
    parentNull[c4d.NULLOBJECT_DISPLAY] = 14 # Set parent null's display mode to none
    SetGlobalPosition(parentNull,GetGlobalPosition(obj)) # Set global position, rotation and scale
    SetGlobalRotation(parentNull,GetGlobalRotation(obj))
    SetGlobalScale(parentNull,GetGlobalScale(obj))
    doc.InsertObject(parentNull) # Insert parent null to document

    for i in range(pointCount): # Loop through points
        if(points.IsSelected(i)): # If point is selected
            pointNull = c4d.BaseObject(c4d.Onull) # Initialize point null object
            pointNull.SetName("Point "+str(i)) # Set point null's name
            pointNull[c4d.NULLOBJECT_DISPLAY] = 2 # Set point null's display mode circle
            pointNull.SetAbsPos(obj.GetPoint(i)) # Set null's position
            pointNull.InsertUnderLast(parentNull) # Insert point null last object under parent null
            doc.AddUndo(c4d.UNDOTYPE_NEW, parentNull) # Add undo command for adding new object

            link1 = CreateUserDataLink(pointNull, "Target", obj) # Create user data link for target object
            link2 = CreateUserDataLink(pointNull, "Controller", pointNull) # crete user data link for controller

            xptag = c4d.BaseTag(c4d.Texpresso) # Initialize xpresso tag
            xptag.SetName("My Xpresso Tag") # Set xpresso tag name
            pointNull.InsertTag(xptag) # Insert xpresso tag to null object
            nodemaster = xptag.GetNodeMaster() # Get xpresso tag's nodemaster

            # Add nodes
            objectNode = nodemaster.CreateNode(nodemaster.GetRoot(), c4d.ID_OPERATOR_OBJECT, None, x=200, y=100)
            pointNode = nodemaster.CreateNode(nodemaster.GetRoot(), 400001112, None, x=400, y=100)
            pythonNode = nodemaster.CreateNode(nodemaster.GetRoot(), 1022471, None, x=300, y=200)

            #Remove python node's default ports
            pythonInPorts = pythonNode.GetInPorts()
            pythonOutPorts = pythonNode.GetOutPorts()
            pythonNode.RemovePort(pythonInPorts[0], True)
            pythonNode.RemovePort(pythonInPorts[1], True)
            pythonNode.RemovePort(pythonOutPorts[0], True)

            # Change node values
            pointNode[c4d.GV_POINT_INPUT_POINT] = i # Change point index

            # Add ports
            objPort1 = objectNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER, 0),c4d.DescLevel(1)), True)
            objPort2 = objectNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.DescID(c4d.DescLevel(c4d.ID_USERDATA, c4d.DTYPE_SUBCONTAINER, 0),c4d.DescLevel(2)), True)
            pyPort1 = pythonNode.AddPort(c4d.GV_PORT_INPUT, 4013, True) # Link input port
            pyPort2 = pythonNode.AddPort(c4d.GV_PORT_OUTPUT, 4006, True) # Vector output port
            pointPosPort = pointNode.AddPort(c4d.GV_PORT_INPUT, 2002)
            
            # Python code
            pythonNode[c4d.GV_PYTHON_CODE] = "import c4d\ndef main():\n\tglobal Vector\n\tVector = Link.GetMg().off"
            
            # Connect nodes
            objectNode.GetOutPort(0).Connect(pointNode.GetInPort(0))
            objectNode.GetOutPort(1).Connect(pythonNode.GetInPort(0))
            pythonNode.GetOutPort(0).Connect(pointNode.GetInPort(2))
            
            # Rest of the stuff
            c4d.modules.graphview.RedrawMaster(nodemaster) # Update xpresso

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get active selection
        for obj in selection: # Loop through selected items
            CreateControlNulls(obj) # Run CreateControlNulls function
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()