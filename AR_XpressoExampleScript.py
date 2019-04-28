"""
AR_XpressoExampleScript

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_XpressoExampleScript
Description-US: Creates xpresso setup with couple connected nodes
> Select object and run the script
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    selected = doc.GetActiveObject() # Get active object

    # Tag setup
    xpressotag = c4d.BaseTag(c4d.Texpresso) # Initialize xpresso tag
    xpressotag.SetName("My Xpresso Tag") # Set xpresso tag name
    selected.InsertTag(xpressotag) # Insert xpresso tag to selected object
    nodemaster = xpressotag.GetNodeMaster() # Get node master

    # Node creation
    mathNode = nodemaster.CreateNode(nodemaster.GetRoot(), 400001121, None, x=200, y=100)
    constantNodeA = nodemaster.CreateNode(nodemaster.GetRoot(), 400001120, None, x=100, y=100)
    constantNodeB = nodemaster.CreateNode(nodemaster.GetRoot(), 400001120, None, x=100, y=150)
    resultNode = nodemaster.CreateNode(nodemaster.GetRoot(), 400001118, None, x=350, y=100)

    # Node values
    constantNodeA[c4d.GV_CONST_VALUE] = 10
    constantNodeB[c4d.GV_CONST_VALUE] = 5
    mathNode[c4d.GV_MATH_FUNCTION_ID] = 1

    # Ports
    constantPortOutA = constantNodeA.GetOutPort(0)
    constantPortOutB = constantNodeB.GetOutPort(0)
    mathPortInA = mathNode.GetInPort(0)
    mathPortInB = mathNode.GetInPort(1)
    mathPortOut = mathNode.GetOutPort(0)
    resultPortIn = resultNode.GetInPort(0)

    # Connecting ports
    constantPortOutA.Connect(mathPortInA)
    constantPortOutB.Connect(mathPortInB)
    mathPortOut.Connect(resultPortIn)

    # Refresh
    c4d.modules.graphview.RedrawMaster(nodemaster) # Refresh xpresso graph view
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()