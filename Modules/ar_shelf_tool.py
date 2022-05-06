"""
Shelf Tool Script for Cinema 4D

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/

Version: 1.0.1

Installation path: C:/Users/[USER]]/AppData/Roaming/MAXON/Maxon Cinema 4D R2X_XXXXXXXX/python39/libs

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (04.05.2022) - Added support to change icon and icon color
1.0.0 (08.04.2022) - Initial release
"""

# Libraries
import c4d
from c4d import documents

# Global variables
generators = [1018544, # Cloner
              1018545, # Matrix
              1018791, # Fracture
              440000054, # MoSpline
              1018957, # MoInstance
              1036557, # Voronoi Fracture
              1019268, # MoText
              1019358, # MoExtrude
              1019222] # PolyFX

deformers = [5149, # Wind
             1021318, # Point Cache
             1019768, # Morph
             5146, # Formula
             1018685, # Displacer
             5143, # Wrap
             1024552, # Surface
             1024529, # Smoothing
             1035447, # Delta Mush
             1001003, # Spherify
             1019774, # Shrink Wrap
             1024544, # Collision
             1021280, # Squash & Stretch
             1021284, # Jiggle
             5147, # Melt
             1024543, # Mesh
             1024542, # Correction
             1024476, # Camera
             5134, # Twist
             5133, # Taper
             5131, # Shear
             5129, # Bulge
             5128] # Bend

forces = [5113, # Wind
          5115, # Turbulence
          5112, # Rotation
          5111, # Gravity
          5114, # Friction
          1041451, # Field Force
          5119] # Attractor

effectors = [1021287, #Volume
             1018935, #Time
             1018889, #Target
             1018881, #Step
             1018774, #Spline
             440000255, #Sound
             1018561, #Shader
             440000234, #ReEffector
             1018643, #Random
             1025800, #Python
             440000219, #Push Apart
             1018775, #Inheritance
             1018883, #Formula
             1019234, #Delay
             1019351, #Group
             1021337] #Plain

fields = [1040449, # Group Field
          440000277, # Python Field
          440000280, # Formula Field
          440000283, # Sound Field
          440000282, # Shader Field
          440000281, # Random Field
          440000272, # Torus Field
          440000274, # Capsule Field
          440000269, # Cone Field
          440000268, # Cylinder Field
          440000267, # Box Field
          440000243, # Spherical Field
          1040448, # Radial Field
          440000266] # Linear Field

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
    
def CheckParent(op):
    if op.GetUp() != None:
        return op.GetUp()
    else:
        return None
    
def CheckPred(op):
    if op.GetPred() != None:
        return op.GetPred()
    else:
        return None

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def GetMaterials(op):
    texTags = []
    materials = []
    if op is None:
        return
    while op:
        # Check materials
        tags = op.GetTags() # Get tags of the asset
        for tag in tags: # Iterate through tags
            if tag.GetType() == 5616: # If texture tag
                mat = tag[c4d.TEXTURETAG_MATERIAL] # Get texture tags's material
                if mat != None: # Check that tag is not missing the material
                    texTags.append(tag) # Add tag to the list
                    materials.append(mat) # Add material to the list
        op = GetNextObject(op)
    return texTags, materials

def AddToList(asset, target):
    global generators
    global deformers
    global forces
    global effectors
    global fields

    # Effectors to generators
    if asset.GetType() in effectors: # If asset is an effector
        if target.GetType() in generators:
            if target.GetType() in [1018544, 1018791, 1018545, 1018957, 1019358, 1019222]: # Basic MoGraph generators
                effectorsList = target[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
                effectorsList.InsertObject(asset, 1)
                target[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = effectorsList
            elif target.GetType() == 440000054: # MoSpline
                effectorsList = target[c4d.MGMOSPLINEOBJECT_EFFECTORLIST]
                effectorsList.InsertObject(asset, 1)
                target[c4d.MGMOSPLINEOBJECT_EFFECTORLIST] = effectorsList
            elif target.GetType() == 1036557: # Voronoi Fracture
                effectorsList = target[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST]
                effectorsList.InsertObject(asset, 1)
                target[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST] = effectorsList
            elif target.GetType() == 1019268: # MoText
                effectorsList = target[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR]
                effectorsList.InsertObject(asset, 1)
                target[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR] = effectorsList
            else:
                pass

    # Fields to effectors, deformers and forces
    elif asset.GetType() in fields: # If asset is a field
        if (target.GetType() in effectors) or (target.GetType() in deformers): # If target is a effector
            fieldLayer = c4d.modules.mograph.FieldLayer(c4d.FLfield)
            fieldLayer.SetLinkedObject(asset)
            fieldLayer.SetBlendingMode(c4d.ID_FIELDLAYER_BLENDINGMODE_LIGHTEN) # Blending: 'Max'
            fieldList = target[c4d.FIELDS]
            fieldList.InsertLayer(fieldLayer)
            target[c4d.FIELDS] = fieldList
        elif target.GetType() in forces:
            if target.GetType() == 1041451: # If field force
                fieldLayer = c4d.modules.mograph.FieldLayer(c4d.FLfield)
                fieldLayer.SetLinkedObject(asset)
                fieldLayer.SetBlendingMode(c4d.ID_FIELDLAYER_BLENDINGMODE_LIGHTEN) # Blending: 'Max'
                fieldList = target[c4d.ID_FIELDFORCE_FIELDLIST]
                fieldList.InsertLayer(fieldLayer)
                target[c4d.FIELDS] = fieldList
            else:
                fieldLayer = c4d.modules.mograph.FieldLayer(c4d.FLfield)
                fieldLayer.SetLinkedObject(asset)
                fieldLayer.SetBlendingMode(c4d.ID_FIELDLAYER_BLENDINGMODE_LIGHTEN) # Blending: 'Max'
                fieldList = target[c4d.FIELDS]
                fieldList.InsertLayer(fieldLayer)
                target[c4d.FIELDS] = fieldList
    return

def GetIconPath(scriptPath):
    # Parsing the file path for the icon
    iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    return iconPath

def Import(path=None, icon=None, color=None, matsOnly=False):

    # Check path
    if path == None:
        print("No path found!")
        return False

    doc = documents.GetActiveDocument() # Get active document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE) # Get active objects

    # Import the asset
    tempDoc = documents.BaseDocument() # Create temp doc
    flags = c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS | c4d.SCENEFILTER_MERGESCENE # Merge objects and materials
    c4d.documents.MergeDocument(tempDoc, path, flags) # Merge asset to active project
    asset = tempDoc.GetFirstObject() # Get the imported asset
    texTags, materials = GetMaterials(asset) # Get all materials

    # Set the icon and the color for the asset
    if icon != None:
        icon = GetIconPath(icon) # Get icon path
        asset[c4d.ID_BASELIST_ICON_FILE] = icon # Set icon path
    if color != None:
        asset[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Set Icon Color to 'Custom'
        asset[c4d.ID_BASELIST_ICON_COLOR] = color # Set icon color

    for m in materials: # Iterate through collected materials
        doc.InsertMaterial(m, checknames=True)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, m)

    if not matsOnly:
        if len(selection) != 0:
            if keyMod != "None":
                for s in selection: # Iterate through selected objects
                    clone = asset.GetClone()
                    if keyMod == "Shift": # Insert to child
                        doc.AddUndo(c4d.UNDOTYPE_BITS, s)
                        if s.GetNBit(c4d.NBIT_OM1_FOLD) == False:
                                s.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE)
                        doc.InsertObject(clone, parent=s, checknames=True)
                        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)
                    elif keyMod == "Alt": # Insert to parent
                        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                        mat = s.GetMg()
                        parent = CheckParent(s)
                        pred = CheckPred(s)
                        doc.InsertObject(clone, parent=parent, pred=pred, checknames=True)
                        clone.SetMg(mat)
                        s.InsertUnder(clone)
                        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)
                        s.SetMg(mat)
                    elif keyMod == "Ctrl": # Insert next
                        doc.InsertObject(clone, pred=s, checknames=True)
                        clone.SetMg(s.GetMg())
                    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)
                    AddToList(clone, s) # Try to add asset to generator
                asset.Remove() # Delete original
            else:
                doc.InsertObject(asset, checknames=True)
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, asset)
                for s in selection: # Iterate through selected objects
                    AddToList(asset, s) # Try to add asset to generator
        else:
            doc.InsertObject(asset, checknames=True)
            doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, asset)
        
        for s in selection:
            s.DelBit(c4d.BIT_ACTIVE)
            doc.AddUndo(c4d.UNDOTYPE_BITS, s)
    
    documents.KillDocument(tempDoc) # Kill the temp document
    c4d.EventAdd() # Refresh Cinema 4D
    doc.EndUndo() # Stop recording undos

    return True # All good