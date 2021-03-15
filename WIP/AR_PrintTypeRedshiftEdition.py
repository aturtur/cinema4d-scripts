"""
AR_PrintTypeRedshiftEdition

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_PrintTypeRedshiftEdition
Version: 1.0
Description-US: Prints selected object(s) type (ID)

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
import redshift

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document

    selection = doc.GetSelection() # Get active selection (objects, tags)
    for s in selection: # Iterate through selection

        print (s.GetName(), "\""+type(s).__name__+"\"", s.GetType()) # Print: name, class and type id

        if type(s).__name__ == "XPressoTag": # If operator is xpresso tag
            nodeMaster = s.GetNodeMaster() # Get node master
            root = nodeMaster.GetRoot() # Get xpresso root
            for c in root.GetChildren(): # Loop through nodes
                if c.GetBit(c4d.BIT_ACTIVE): # If node is selected
                    print ("Node: "+c.GetName()+", "+str(c.GetOperatorID())) # Print node info
                    inPorts = c.GetInPorts() # Get input ports
                    outPorts = c.GetOutPorts() # Get output ports
                    for p in range(0, len(inPorts)): # Loop through input ports
                        print ("    In port: "+inPorts[p].GetName(c)+", "+str(inPorts[p].GetMainID()))   # Print inPort info
                    for p in range(0, len(outPorts)): # Loop through output ports
                        print ("    Out port: "+outPorts[p].GetName(c)+", "+str(outPorts[p].GetMainID()))# Print outPort info

    materials = doc.GetMaterials() # Get materials
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
            print (m.GetName(), "\""+type(m).__name__+"\"", m.GetType()) # Print: name, class and type id

            if m.GetType() == 1036224: # If Redshift material
                rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
                root = rsnm.GetRoot() # Get node master root
                for c in root.GetChildren(): # Loop through nodes
                    if c.GetBit(c4d.BIT_ACTIVE): # If node is selected
                        print ("Node: "+c.GetName()+", "+str(c.GetOperatorID())) # Print node info
                        inPorts = c.GetInPorts() # Get input ports
                        outPorts = c.GetOutPorts() # Get output ports
                        for p in range(0, len(inPorts)): # Loop through input ports
                            print ("    In port: "+inPorts[p].GetName(c)+", "+str(inPorts[p].GetMainID()))   # Print inPort info
                        for p in range(0, len(outPorts)): # Loop through output ports
                            print ("    Out port: "+outPorts[p].GetName(c)+", "+str(outPorts[p].GetMainID()))# Print outPort info

    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()