# if holding input qualifier at the time when the script is excuted
import c4d
from c4d import gui

def main():
    key = False
    
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            print "Control pressed"
            # code here
            c4d.EventAdd()
            return
        
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            print "Alt pressed"
            # code here
            c4d.EventAdd()
            return

    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            print "Shift pressed"
            # code here
            c4d.EventAdd()
            return

if __name__=='__main__':
    main()
