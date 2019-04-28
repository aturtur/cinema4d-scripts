"""
AR_XpressoNodeInfo

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_XpressoNodeInfo
Description-US: Print to console selected Xpresso nodes info. Select Xpresso tag and select nodes and run the script.
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selected = doc.GetSelection()[0] # Get first item of the selection
    if type(selected).__name__ == "XPressoTag": # If operator is xpresso tag
        nodeMaster = selected.GetNodeMaster() # Get node master
        root = nodeMaster.GetRoot() # Get xpresso root
        for c in root.GetChildren(): # Loop through nodes
            if c.GetBit(c4d.BIT_ACTIVE): # If node is selected
                print "Node: "+c.GetName()+", "+str(c.GetOperatorID()) # Print node info
                inPorts = c.GetInPorts() # Get input ports
                outPorts = c.GetOutPorts() # Get output ports
                for p in range(0, len(inPorts)): # Loop through input ports
                    print "    In port: "+inPorts[p].GetName(c)+", "+str(inPorts[p].GetMainID()) # Print inPort info
                for p in range(0, len(outPorts)): # Loop through output ports
                    print "    Out port: "+outPorts[p].GetName(c)+", "+str(outPorts[p].GetMainID())# Print outPort info
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()