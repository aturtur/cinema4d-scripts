"""
Utility funktion: Get keyboard modifiers
"""
import c4d
from c4d import gui

# Main function
def main():
        doc = c4d.documents.GetActiveDocument() # Get active document
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
                
        # Now you can use keyMod variable to get status what keymodifiers are pressed
        if keyMod == "Ctrl":
            gui.MessageDialog('Ctrl pressed')

# Execute main()
if __name__=='__main__':
    main()