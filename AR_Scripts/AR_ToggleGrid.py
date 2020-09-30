"""
AR_ToggleGrid

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ToggleGrid
Version: 1.0
Description-US: Toggle grid visibility in viewport

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    bd = doc.GetActiveBaseDraw() # Get active basedraw
    bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] = not bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] # Toggle grid

# Execute main()
if __name__=='__main__':
    main()
    c4d.EventAdd()