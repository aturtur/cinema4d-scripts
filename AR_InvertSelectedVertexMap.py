"""
AR_InvertSelectedVertexMap

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_InvertSelectedVertexMap
Description-US: Inverts selected Vertex Maps data
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def main():    
    selection = doc.GetSelection() # Get active selection
    for s in selection: # Iterate through selected items
        if s.GetType() == 5682: # If Vertex Map Tag
            data = s.GetAllHighlevelData() # Get Vertex Map data
            for i in xrange(0, len(data)): # Loop through data values
                data[i] = 1 - data[i] # Invert value
            s.SetAllHighlevelData(data) # Set Vertex Map data
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()