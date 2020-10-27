"""
AR_ViewportGradients

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ViewportGradients
Version: 1.0.1
Description-US: Cycles through different background gradients for viewport. SHIFT: Default gradient (R21)
Note: Change is permanent.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.1 (23.10.2020) - Wrong version fix
"""
# Libraries
import c4d, os
from c4d import storage
from c4d import gui


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

def HexToRgb(value):
    value = value.replace(' ', '').replace('\n', '').replace('\r', '') # Remove spaces
    value = value.lstrip('#') # Strip '#' symbol from value
    lv = len(value) # Length of the input
    #print value
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():

    # Initialize colors ----------------------
    gradients = [
        [c4d.Vector(0.2196, 0.2196, 0.2196), c4d.Vector(0.298, 0.298, 0.298)], # 0 Cinema 4D
        [c4d.Vector(0.741, 0.773, 0.776), c4d.Vector(0.4, 0.494, 0.545)],      # 1 Houdini
        [c4d.Vector(0.082, 0.086, 0.09), c4d.Vector(0.525, 0.608, 0.69)],      # 2 Maya
        [c4d.Vector(0.357, 0.357, 0.357), c4d.Vector(0.525, 0.525, 0.525)],    # 3 Legacy
        [c4d.Vector(0.08, 0.08, 0.08), c4d.Vector(0, 0, 0)]]                   # 4 Dark
        
    presets = {
        'cinema 4d': gradients[0],
        'default':   gradients[0],
        'new':       gradients[0],
        'c4d':       gradients[0],
        'houdini':   gradients[1],
        'hou':       gradients[1],
        'maya':      gradients[2],
        'legacy':    gradients[3],
        'old':       gradients[3],
        'dark':      gradients[4]
    }

    keyMod = GetKeyMod() # Get keymodifier

    # Action
    if keyMod == "None": # If there is no keymodifier

        # Get current color
        cg1 = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1)
        cg2 = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2)

        # Temporary change
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, presets['houdini'][0])
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, presets['houdini'][1])

        spot = None
        last = False
        for i, grad in enumerate(gradients): # Iterate through colors
            if (cg1 == grad[0]) and (cg2 == grad[1]):
                spot = i
                if i == len(gradients)-1:
                    last = True
        if spot == None:
            c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, gradients[0][0])
            c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, gradients[0][1])
        else:
            if last == False:
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, gradients[spot+1][0])
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, gradients[spot+1][1])
            if last == True:
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, gradients[0][0])
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, gradients[0][1])
        pass


    # If shift pressed
    if keyMod == "Shift": # New Cinema 4D (Default gradient)
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, presets['default'][0])
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, presets['default'][1])

    # If control pressed
    if keyMod == "Ctrl": # Dark theme
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, presets['dark'][0])
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, presets['dark'][1])

    # If alt pressed, cycle through user gradients
    if keyMod == "Alt":
        path, fn = os.path.split(__file__) # Get path of the script
        data = os.path.join(path, 'AR_ViewportGradients.txt') # data file path
        userGradients = []
        f = open(data.decode("utf-8")) # Open the file for reading
        for line in f: # Iterate through every row
            line = line.split(",") # Split by comma
            rgbA = HexToRgb(str(line[0])) # Get first rgb
            rgbB = HexToRgb(str(line[1])) # Get last rgb
            colorA = c4d.Vector(float(rgbA[0])/255,float(rgbA[1])/255,float(rgbA[2])/255) # Convert rgb to c4d form
            colorB = c4d.Vector(float(rgbB[0])/255,float(rgbB[1])/255,float(rgbB[2])/255)
            userGradients.append([colorA, colorB]) # Add colors to the list

        # Figure out current spot, if using user gradients
        cg1 = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1)
        cg2 = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2)
        spot = None
        last = False
        for i, grad in enumerate(userGradients): # Iterate through colors
            if (cg1 == grad[0]) and (cg2 == grad[1]):
                spot = i
                if i == len(userGradients)-1:
                    last = True
        if spot == None:
            c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, userGradients[0][0])
            c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, userGradients[0][1])
        else:
            if last == False:
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, userGradients[spot+1][0])
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, userGradients[spot+1][1])
            if last == True:
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, userGradients[0][0])
                c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, userGradients[0][1])
        f.close() # Close the file
        pass

    # If alt + control + shift pressed, open dat-file
    if keyMod == "Alt+Ctrl+Shift":
        path, fn = os.path.split(__file__) # Get path of the script
        data = os.path.join(path, 'AR_ViewportGradients.txt') # data file path
        storage.GeExecuteFile(data) # Open data file for editing user gradients
        pass

    # If alt + control + shift pressed, open dat-file
    if keyMod == "Alt+Ctrl":
        name = gui.InputDialog("Prestet name", "").lower() # Input dialog
        if name is None: return
        if name is "": return

        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD1, presets[name][0])
        c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND_GRAD2, presets[name][1])
        pass


    c4d.EventAdd() # Update

# Execute main()
if __name__=='__main__':
    main()