"""
AR_SelectDeepest

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectDeepest
Version: 1.0.2
Description-US: Default: Select children of selected object(s) that are the most deep in hierarchy. Shift: Keep original selection.

Written for Maxon Cinema 4D 2023.1.0
Python version 3.9.1

Change log:
1.0.2 (18.11.2022) - Hotkey fix
1.0.1 (20.01.2022) - R25 update
"""

# Libraries
import c4d

# Global variables
hierarchy = {} # Initialize hierarchy dictionary
level = 0 # Initialize level variable (how deep object is in hierarchy)

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

def GetNextObject(op): # Get next object from Object Manager
    global level # Access to global variable (level)
    if op is None: # If there is no object
        return None # Return none
    if op.GetDown(): # If can go deeper in hierarchy
        level += 1 # Going deeper in levels
        return op.GetDown() # Return object
    while not op.GetNext() and op.GetUp(): # If can't go to next object, but can go up
        level -= 1 # Going up in levels
        op = op.GetUp() # Object is parent object
    return op.GetNext() # Return object

def BuildHierarchyPath(obj): # Build hierarchy path for object
    global level # Access to global variable (level)
    path = [] # Initialize empty list for path
    for i in range(0,level+1): # Iterate through levels
        path.append(obj) # Add object to path list
        if obj.GetUp() is not None: # If can go up in Object Manager
            obj = obj.GetUp() # Going up
    path.reverse() # Reverse path list 
    return path # Return hierarchy path

def BuildHierarchy(): # Build hierarchy dictionary
    global level # Access to global variable (level)
    global hierarchy # Access to global dictionary (hierarchy)
    doc = c4d.documents.GetActiveDocument()
    op = doc.GetFirstObject()
    #hierarchy = {} # Initialize empty dictionary
    i = 0 # Iteration variable
    if op is None: # If there is no object
        return # Return nothing
    while op: # While there is object
        hierarchy[i]={ # Add object information to hierarchy dictionary
            'object': op, # Object
            'level': level, # Object's level (how deep object is in Object Manager)
            'name': op.GetName(), # Object's name
            'root': FindRoot(op), # Object's root
            'path': BuildHierarchyPath(op) # Object's full path in hierarchy
        }
        op = GetNextObject(op) # Get next object from Object Manager
        i += 1 # Increase iteration variable
    return hierarchy # Return hierarchy dictionary

def FindRoot(data): # Find object's root
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        collection = [] # Initialize empty list for root object(s)
        for obj in lst: # Loop through objects in 
            while obj: # Infinite loop
                if obj.GetUp() == None: # If can't go up in hierarchy
                    collection.append(obj) # Add object to collection list
                    break # Break the loop
                obj = obj.GetUp() # Go up
        return collection # Return collection of root object(s)
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        while obj: # Infinite loop
            if obj.GetUp() == None: # If can't go up in Object Manager
                return obj # Return object
                break # Break the loop
            obj = obj.GetUp() # Get up

def FindDeepest(start): # Find deepest level item(s)
    global hierarchy # Access to global dictionary (hierarchy)
    collection = [] # Initialize empty list
    sortedcollection = [] # Initialize empty list
    for counter, item in hierarchy.items(): # Loop through hierarchy items
        for p in item['path']: # Loop through paths
            if p == start: # Starting point
                collection.append([item['level'], item['path'][-1]])

    maxlevel = []
    for x in collection:
        maxlevel.append(x[0])

    maximum = max(maxlevel) # Maximum level of the collection

    for item in collection: # Loop through collection
        if item[0] == maximum: # If object is deepest
            sortedcollection.append(item[1]) # Add object to list
    return sortedcollection # Return list of deepest children

def Select(data): # Select object(s)
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        for obj in lst: # Loop through list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
        obj.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager

def Deselect(data): # Deselect object(s)
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        for obj in lst: # Loop through list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    global hierarchy # Access to global dictionary (hierarchy)
    hierarchy = BuildHierarchy()
    keyMod = GetKeyMod() # Get keymodifier
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)   

    if (keyMod == "None") or (keyMod == "Alt"):
        for obj in selection: # Loop through selection
            Deselect(obj) # Deselect selected object
            Select(FindDeepest(obj)) # Select deepest chldren object(s)
    elif (keyMod == "Shift") or (keyMod == "Alt+Shift"):
        for obj in selection: # Loop through selection
            Select(FindDeepest(obj)) # Select deepest chldren object(s)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()