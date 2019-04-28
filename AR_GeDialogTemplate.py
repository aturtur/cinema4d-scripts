"""
AR_GeDialogTemplate

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_GeDialogTemplate
Description-US: Template for build GeDialog object
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
from c4d.gui import GeDialog

# Classes
class Dialog(GeDialog): 
    def __init__(self):
        super(Dialog, self).__init__()
 
    def CreateLayout(self):
        self.SetTitle("Dialog") # Set dialog title
        self.GroupBegin(1000, c4d.BFH_LEFT, 0, 0) # Add group
        self.AddColorField(1001, c4d.BFH_CENTER) # Add color field gadget
        self.GroupEnd() # End group
        return True
 
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        # Actions here
        return True
 
dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2) # Open asynchronous dialog, pluginid, center of the screen