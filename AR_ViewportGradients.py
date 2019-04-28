"""
AR_ViewportGradients

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ViewportGradients
Description-US: Cycles through different background gradients for viewport
Note: Change is permanent!
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d import plugins

# Functions
def main():

    # Initialize colors
    # Cinema 4D default
    c4dg1 = c4d.Vector(0.357, 0.357, 0.357)
    c4dg2 = c4d.Vector(0.525, 0.525, 0.525)
    # Houdini theme
    houg1 = c4d.Vector(0.741, 0.773, 0.776)
    houg2 = c4d.Vector(0.4, 0.494, 0.545)
    # Maya theme
    mayg1 = c4d.Vector(0.082, 0.086, 0.09)
    mayg2 = c4d.Vector(0.525, 0.608, 0.69)
    # Black theme
    blkg1 = c4d.Vector(0.08, 0.08, 0.08)
    blkg2 = c4d.Vector(0, 0, 0)

    # Get current color
    cg1 = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1)
    cg2 = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2)

    # Temporary change
    c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, houg1)
    c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, houg2)

    if cg1 == c4dg1:
        # Houdini background
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, houg1)
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, houg2)
    elif cg1 == houg1:
        # Maya background
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, mayg1)
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, mayg2)
    elif cg1 == mayg1:
        # Dark background
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, blkg1)
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, blkg2)
    elif cg1 == blkg1:
        # Cinema 4D background
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, c4dg1)
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, c4dg2)

    c4d.EventAdd() # Update

# Execute main()
if __name__=='__main__':
    main()