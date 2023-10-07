"""
AR_MoGraphToNulls

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MoGraphToNulls
Version: 1.0.2
Description-US: Creates a Xpresso setup where null follows MoGraph items

Written for Maxon Cinema 4D 2023.2.0
Python version 3.10.8

Change log:
1.0.2 (19.06.2023) - Bug fix
1.0.1 (11.05.2023) - Warning dialog if user is going to make large amount of nulls
1.0.0 (06.04.2023) - Initial realease

"""

# Libraries
import c4d
from c4d.modules import mograph as mo
from c4d import gui as g

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

def MographToNulls(obj, numberList):
    moData = mo.GeGetMoData(obj)
    if moData is None:
        return False

    cnt = moData.GetCount()

    # If user want's to create nulls for all clones
    if len(numberList) == 0:
        for i in range(0, cnt):
            numberList.append(i)

    # Ask user if sure to generate a lot of rigs
    if len(numberList) > 200:
        confirm = g.QuestionDialog("You sure want to create rig for\n"+str(len(numberList))+" clones?")
        if not confirm:
            return None

    groupNull = c4d.BaseObject(c4d.Onull) # 
    groupNull.SetName(obj.GetName()+"_nulls") # Set name

    #doc.InsertObject(groupNull, checknames=True)
    groupNull.InsertAfter(obj)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, groupNull)
    groupNull.SetBit(c4d.BIT_ACTIVE)

    # Important to insert it before creating object nodes in xpresso tag!
    for i in numberList:
        mgNull = c4d.BaseObject(c4d.Onull) #
        mgNull.SetName("Item "+str(i)) # Set name
        mgNull.InsertUnderLast(groupNull) # Insert object under group null

        # Priority data setup
        prioritydata = c4d.PriorityData() # Initialize a priority data
        prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
        prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 5) # Set priority value
        prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false

        # Xpresso tag setup
        xpTag = c4d.BaseTag(c4d.Texpresso) # Initialize xpresso tag
        xpTag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set prioritydata
        mgNull.InsertTag(xpTag) # Insert xpresso tag to null
        nodeMaster = xpTag.GetNodeMaster() # Get xpresso tag's nodemaster
        root = nodeMaster.GetRoot() # Get xpresso root

        # Create Xpresso nodes
        generatorNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=0, y=0) # Create the node
        generatorNode[c4d.GV_OBJECT_OBJECT_ID] = obj # Reference object
        generatorOutPort = generatorNode.AddPort(c4d.GV_PORT_OUTPUT, c4d.GV_OBJECT_OPERATOR_OBJECT_OUT, message=True)

        moDataNode = nodeMaster.CreateNode(root, 1019010, None, x=100, y=0) # Create the node
        moDataInPort = moDataNode.AddPort(c4d.GV_PORT_INPUT, 1006, message=True)
        moDataOutPort = moDataNode.AddPort(c4d.GV_PORT_OUTPUT, 2006, message=True)
        moDataNode[c4d.GV_MG_DATA_INDEX] = int(i)

        nullNode = nodeMaster.CreateNode(root, c4d.ID_OPERATOR_OBJECT, None, x=300, y=0) # Create the node
        nullNode[c4d.GV_OBJECT_OBJECT_ID] = mgNull # Reference object
        nullInPort = nullNode.AddPort(c4d.GV_PORT_INPUT, 30000001, message=True)

        # Connect
        generatorOutPort.Connect(moDataNode.GetInPort(1))
        moDataOutPort.Connect(nullInPort)

    #
    c4d.modules.graphview.RedrawMaster(nodeMaster) # Update xpresso
    return groupNull

def main():
    keyMod = GetKeyMod() # Get keymodifier
    selection = []
    selection = doc.GetActiveObjects(0) # Get selected objects
    mgObjects = [1018544, 1018545, 1018791, 1036557]
    numberList = []  # Initialize empty list
    if keyMod == "Shift":
        userInput = g.InputDialog("IDs","") # User input dialog
        if userInput == "": return
        baseList = userInput.split(",") # Split user input to list
        add = [] # Initialize empty list
        for x in baseList: # Loop through list items
            rng = x.split("-") # Split range value (e.g. 5-15)
            if len(rng) > 1:
                for i in range(int(rng[0]),int(rng[1])+1):
                    add.append(i)
        fullList = baseList + add
        for f in fullList:
            if type(f) == int:
                numberList.append(int(f))
            if type(f) != int:
                if f.find("-") == -1:
                    numberList.append(int(f))
    for s in selection:
        if s.GetType() in mgObjects:
            MographToNulls(s, numberList)

    if len(selection) > 0:
        for s in selection:
            doc.AddUndo(c4d.UNDOTYPE_BITS, s)
            s.DelBit(c4d.BIT_ACTIVE)

    c4d.EventAdd()
    pass

# Execute main
if __name__ == '__main__':
    main()