# template for making xpresso nodes and connecting them
# ids can found here: http://188.166.72.248/c4d.python.id/

import c4d

def main():

    doc = c4d.documents.GetActiveDocument()
    selected = doc.GetActiveObject()

    #tag
    xpressotag = c4d.BaseTag(c4d.Texpresso)
    xpressotag.SetName("My Xpresso Tag")
    selected.InsertTag(xpressotag)

    # xpresso master
    nodemaster = xpressotag.GetNodeMaster()

    # create nodes
    mathNode = nodemaster.CreateNode(nodemaster.GetRoot(), 400001121, None, x=200, y=100)
    constantNodeA = nodemaster.CreateNode(nodemaster.GetRoot(), 400001120, None, x=100, y=100)
    constantNodeB = nodemaster.CreateNode(nodemaster.GetRoot(), 400001120, None, x=100, y=150)
    resultNode = nodemaster.CreateNode(nodemaster.GetRoot(), 400001118, None, x=350, y=100)

    # change node values
    constantNodeA[c4d.GV_CONST_VALUE] = 10
    constantNodeB[c4d.GV_CONST_VALUE] = 5
    mathNode[c4d.GV_MATH_FUNCTION_ID] = 1

    # ports
    constantPortOutA = constantNodeA.GetOutPort(0)
    constantPortOutB = constantNodeB.GetOutPort(0)
    mathPortInA = mathNode.GetInPort(0)
    mathPortInB = mathNode.GetInPort(1)
    mathPortOut = mathNode.GetOutPort(0)
    resultPortIn = resultNode.GetInPort(0)

    # connect ports
    constantPortOutA.Connect(mathPortInA)
    constantPortOutB.Connect(mathPortInB)
    mathPortOut.Connect(resultPortIn)

    # refresh
    c4d.modules.graphview.RedrawMaster(nodemaster)
    c4d.EventAdd()
    
if __name__=='__main__':
    main()