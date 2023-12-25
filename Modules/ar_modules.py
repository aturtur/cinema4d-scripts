"""
AR_Modules

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/

Version: 1.4.0

Installation path: C:/Users/[USER]]/AppData/Roaming/MAXON/Maxon Cinema 4D [VERSION]/python311/libs

Written for Maxon Cinema 4D 2024.2.0
Python version 3.11.4

Change log:
1.4.0 (17.12.2023) - Merged with ar_template
1.3.0 (25.09.2022) - Alt+Ctrl+Shift keymodifier opens the asset document
1.2.1 (16.09.2022) - Bug fixes and code improvements
1.2.0 (06.05.2022) - Added icon parsing here
1.1.0 (04.05.2022) - Added support to change icon and icon color
1.0.0 (08.04.2022) - Initial release
"""

# Libraries
import random
import c4d
from c4d import documents
from c4d import storage

# -----------------------------------------------------------------------------------------------------------------------------------------
# Asset
# -----------------------------------------------------------------------------------------------------------------------------------------

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
             5128, # Bend
             1060422] # Projection

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
 
def GetAssetsMaterials(op):
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
    try:
        iconPath = scriptPath.rsplit('.', 1)[0]+".tif"
    except:
        return ""
    return iconPath

def ImportAsset(path=None, icon=None, color=None, matsOnly=False):

    # Check path
    if path == None:
        print("No path found!")
        return False

    doc = documents.GetActiveDocument() # Get active document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_NONE) # Get active objects

    if keyMod == "Alt+Ctrl+Shift":
        storage.GeExecuteFile(path) # Open the asset
    else:
        # Import the asset
        tempDoc = documents.BaseDocument() # Create temp doc
        flags = c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS | c4d.SCENEFILTER_MERGESCENE # Merge objects and materials
        c4d.documents.MergeDocument(tempDoc, path, flags) # Merge asset to active project
        asset = tempDoc.GetFirstObject() # Get the imported asset
        #texTags, materials = GetAssetsMaterials(asset) # Get all materials
        materials = tempDoc.GetMaterials() # Get all materials

        # Set the icon and the color for the asset
        if asset != None:
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
            doc.InsertObject(asset, checknames=True)
            assetName = asset.GetName() # Get asset's original name
            asset.SetName(random.randint(100000,999999))
            if len(selection) != 0:
                if keyMod != "None":
                    for s in selection: # Iterate through selected objects
                        clone = asset.GetClone()
                        clone.SetName(assetName)
                        if keyMod == "Shift": # Insert to child
                            doc.AddUndo(c4d.UNDOTYPE_BITS, s)
                            if s.GetNBit(c4d.NBIT_OM1_FOLD) == False:
                                    s.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_TOGGLE)
                            doc.InsertObject(clone, parent=s, checknames=True)
                        elif keyMod == "Alt": # Insert to parent
                            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s)
                            mat = s.GetMg()
                            parent = CheckParent(s)
                            pred = CheckPred(s)
                            doc.InsertObject(clone, parent=parent, pred=pred, checknames=True)
                            clone.SetMg(mat)
                            s.InsertUnder(clone)
                            s.SetMg(mat)
                        elif keyMod == "Ctrl": # Insert next
                            doc.InsertObject(clone, pred=s, checknames=True)
                            clone.SetMg(s.GetMg())
                        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)
                        AddToList(clone, s) # Try to add asset to generator
                    asset.Remove() # Delete original
                else:
                    clone = asset.GetClone()
                    clone.SetName(assetName)
                    doc.InsertObject(clone, checknames=True)
                    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, clone)
                    for s in selection: # Iterate through selected objects
                        AddToList(clone, s) # Try to add asset to generator
            else:
                clone = asset.GetClone()
                clone.SetName(assetName)
                doc.InsertObject(clone, checknames=True)
                doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, asset)            
            for s in selection:
                s.DelBit(c4d.BIT_ACTIVE)
                doc.AddUndo(c4d.UNDOTYPE_BITS, s)
            asset.Remove() # Delete asset    
        documents.KillDocument(tempDoc) # Kill the temp document

    c4d.EventAdd() # Refresh Cinema 4D
    doc.EndUndo() # Stop recording undos

    return True # All good


# -----------------------------------------------------------------------------------------------------------------------------------------
# Template
# -----------------------------------------------------------------------------------------------------------------------------------------

# Functions
def CollectRenderData(document):
    """ Collect all render data of the document """

    renderDataList = []
    renderData = document.GetFirstRenderData()
    while renderData:
        renderDataList.append(renderData)
        renderData = renderData.GetNext()
    return renderDataList

def CopyDocumentSettings(source, target):
    """ Copies document settings from source document to target document """

    target.SetMode(source.GetMode()) # Copy the main mode of the editor

    # Project
    target[c4d.DOCUMENT_DOCUNIT]               = source[c4d.DOCUMENT_DOCUNIT] # Project Scale

    target[c4d.DOCUMENT_FPS]                   = source[c4d.DOCUMENT_FPS] # FPS
    target[c4d.DOCUMENT_TIME]                  = source[c4d.DOCUMENT_TIME] # Project Time
    target[c4d.DOCUMENT_MINTIME]               = source[c4d.DOCUMENT_MINTIME] # Time Min
    target[c4d.DOCUMENT_MAXTIME]               = source[c4d.DOCUMENT_MAXTIME] # Time Max
    target[c4d.DOCUMENT_LOOPMINTIME]           = source[c4d.DOCUMENT_LOOPMINTIME] # Preview Min
    target[c4d.DOCUMENT_LOOPMAXTIME]           = source[c4d.DOCUMENT_LOOPMAXTIME] # Preview Max

    target[c4d.DOCUMENT_USEANIMATION]          = source[c4d.DOCUMENT_USEANIMATION]
    target[c4d.DOCUMENT_USEEXPRESSIONS]        = source[c4d.DOCUMENT_USEEXPRESSIONS]
    target[c4d.DOCUMENT_USEGENERATORS]         = source[c4d.DOCUMENT_USEGENERATORS]
    target[c4d.DOCUMENT_USEDEFORMERS]          = source[c4d.DOCUMENT_USEDEFORMERS]
    target[c4d.DOCUMENT_USEMOTIONSYSTEM]       = source[c4d.DOCUMENT_USEMOTIONSYSTEM]
    target[c4d.DOCUMENT_MOUNTWATCHFOLDER]      = source[c4d.DOCUMENT_MOUNTWATCHFOLDER]
    target[c4d.DOCUMENT_RELATIVEWATCHFOLDER]   = source[c4d.DOCUMENT_RELATIVEWATCHFOLDER]
    target[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR] = source[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR]
    target[c4d.DOCUMENT_CLIPPING_PRESET]       = source[c4d.DOCUMENT_CLIPPING_PRESET]
    target[c4d.DOCUMENT_LOD]                   = source[c4d.DOCUMENT_LOD]
    target[c4d.DOCUMENT_COLOR_MANAGEMENT]      = source[c4d.DOCUMENT_COLOR_MANAGEMENT]
    target[c4d.DOCUMENT_LINEARWORKFLOW]        = source[c4d.DOCUMENT_LINEARWORKFLOW]
    target[c4d.DOCUMENT_COLORPROFILE]          = source[c4d.DOCUMENT_COLORPROFILE]

    # Info
    target[c4d.DOCUMENT_INFO_AUTHOR]           = source[c4d.DOCUMENT_INFO_AUTHOR] # Author
    target[c4d.DOCUMENT_INFO_COPYRIGHT]        = source[c4d.DOCUMENT_INFO_COPYRIGHT] # Copyright
    target[c4d.DOCUMENT_INFO_README]           = source[c4d.DOCUMENT_INFO_README] # Info

    # Animation
    animSource = source.FindSceneHook(465001535) # Animation scene hook
    animTarget = target.FindSceneHook(465001535) # Animation scene hook
    animTarget[c4d.TLWORLD_OVERDUB]         = animSource[c4d.TLWORLD_OVERDUB] # Overdub
    animTarget[c4d.TLWORLD_INTER]           = animSource[c4d.TLWORLD_INTER] # Type
    animTarget[c4d.TLWORLD_QUATINTER]       = animSource[c4d.TLWORLD_QUATINTER] # Quaternion Interpolation
    animTarget[c4d.TLWORLD_LOCKT]           = animSource[c4d.TLWORLD_LOCKT] # Lock Time
    animTarget[c4d.TLWORLD_LOCKV]           = animSource[c4d.TLWORLD_LOCKV] # Lock Value
    animTarget[c4d.TLWORLD_BREAKDOWN]       = animSource[c4d.TLWORLD_BREAKDOWN] # Breakdown
    animTarget[c4d.TLWORLD_BREAKDOWNCOLOR]  = animSource[c4d.TLWORLD_BREAKDOWNCOLOR] # Breakdown Color
    animTarget[c4d.TLWORLD_PRESET]          = animSource[c4d.TLWORLD_PRESET] # Tangent Preset
    animTarget[c4d.TLWORLD_AUTO]            = animSource[c4d.TLWORLD_AUTO] # Auto Tangents
    animTarget[c4d.TLWORLD_CLAMP]           = animSource[c4d.TLWORLD_CLAMP] # Clamp
    animTarget[c4d.TLWORLD_AUTOTYPE]        = animSource[c4d.TLWORLD_AUTOTYPE] # Angle
    animTarget[c4d.TLWORLD_REMOVEOVERSHOOT] = animSource[c4d.TLWORLD_REMOVEOVERSHOOT] # Remove Overshooting
    animTarget[c4d.TLWORLD_WEIGHTEDTANGENT] = animSource[c4d.TLWORLD_WEIGHTEDTANGENT] # Weighted Tangents
    animTarget[c4d.TLWORLD_AUTOWEIGHT]      = animSource[c4d.TLWORLD_AUTOWEIGHT] # Automatic Weighting
    animTarget[c4d.TLWORLD_LOCKTA]          = animSource[c4d.TLWORLD_LOCKTA] # Lock Tangent Angles
    animTarget[c4d.TLWORLD_LOCKTL]          = animSource[c4d.TLWORLD_LOCKTL] # Lock Tangent Lengths
    animTarget[c4d.TLWORLD_BREAK]           = animSource[c4d.TLWORLD_BREAK] # Creak Tangents
    animTarget[c4d.TLWORLD_KEEPVISUALANGLE] = animSource[c4d.TLWORLD_KEEPVISUALANGLE] # Keep Visual Angle
    animTarget[c4d.TLWORLD_TRACKEVALMODE]   = animSource[c4d.TLWORLD_TRACKEVALMODE] # R23 Track Evaluation
    
    # Bullet
    bulletSource = source.FindSceneHook(180000100) # Bullet scene hook
    bulletTarget = target.FindSceneHook(180000100) # Bullet scene hook

    # General
    bulletTarget[c4d.WORLD_ENABLED]                      = bulletSource[c4d.WORLD_ENABLED] # Enabled
    bulletTarget[c4d.WORLD_DISABLE_DURING_LEAP]          = bulletSource[c4d.WORLD_DISABLE_DURING_LEAP] # Disable on Skip Frame
    bulletTarget[c4d.WORLD_TIMESCALE]                    = bulletSource[c4d.WORLD_TIMESCALE] # Time Scale
    bulletTarget[c4d.WORLD_GRAVITY]                      = bulletSource[c4d.WORLD_GRAVITY] # Gravity
    bulletTarget[c4d.WORLD_DENSITY]                      = bulletSource[c4d.WORLD_DENSITY] # Density
    bulletTarget[c4d.WORLD_AIR_DENSITY]                  = bulletSource[c4d.WORLD_AIR_DENSITY] # Air Density
    # Cache
    bulletTarget[c4d.WORLD_CACHE_USE]                    = bulletSource[c4d.WORLD_CACHE_USE] # Use Cached Data
    bulletTarget[c4d.WORLD_CACHE_DISABLE_BAKED_OBJECTS]  = bulletSource[c4d.WORLD_CACHE_DISABLE_BAKED_OBJECTS] # Disable Cached Objects for Simulation
    bulletTarget[c4d.WORLD_CACHE_USE_TIME]               = bulletSource[c4d.WORLD_CACHE_USE_TIME] # Use
    bulletTarget[c4d.WORLD_CACHE_TIME]                   = bulletSource[c4d.WORLD_CACHE_TIME] # Playback Time
    # Expert
    bulletTarget[c4d.WORLD_MARGIN]                       = bulletSource[c4d.WORLD_MARGIN] # Collision Margin
    bulletTarget[c4d.WORLD_SCALE]                        = bulletSource[c4d.WORLD_SCALE] # Scale
    bulletTarget[c4d.WORLD_CONTACT_RESTITUTION_LIFETIME] = bulletSource[c4d.WORLD_CONTACT_RESTITUTION_LIFETIME] # Restitution Lifetime for Resting Contact
    bulletTarget[c4d.WORLD_SEED]                         = bulletSource[c4d.WORLD_SEED] # Random Seed
    bulletTarget[c4d.WORLD_SUBSTEPS]                     = bulletSource[c4d.WORLD_SUBSTEPS] # Steps for Frame
    bulletTarget[c4d.WORLD_ITERATIONS]                   = bulletSource[c4d.WORLD_ITERATIONS] # Maximum Solver Iterations per Step
    bulletTarget[c4d.WORLD_ERROR_THRESHOLD]              = bulletSource[c4d.WORLD_ERROR_THRESHOLD] # Error Threshold
    # Visualization
    bulletTarget[c4d.WORLD_VISUALIZE]                    = bulletSource[c4d.WORLD_VISUALIZE] # Enable
    bulletTarget[c4d.WORLD_VISUALIZE_SHAPES]             = bulletSource[c4d.WORLD_VISUALIZE_SHAPES] # Collision Shapes
    bulletTarget[c4d.WORLD_VISUALIZE_AABBS]              = bulletSource[c4d.WORLD_VISUALIZE_AABBS] # Bounding Boxes
    bulletTarget[c4d.WORLD_VISUALIZE_CONTACT_POINTS]     = bulletSource[c4d.WORLD_VISUALIZE_CONTACT_POINTS] # Contact Points
    bulletTarget[c4d.WORLD_VISUALIZE_CONSTRAINTS]        = bulletSource[c4d.WORLD_VISUALIZE_CONSTRAINTS] # Connections

    # Simulation
    simSource = source.FindSceneHook(1057220) # Simulation scene hook
    simTarget = target.FindSceneHook(1057220) # Simulation scene hook

    # Scene
    simTarget[c4d.PBDSCENE_DEVICE]                   = simSource[c4d.PBDSCENE_DEVICE]
    simTarget[c4d.PBDSCENE_COMPUTE_DEVICE_GPU]       = simSource[c4d.PBDSCENE_COMPUTE_DEVICE_GPU]
    simTarget[c4d.PBDSCENE_DEFAULTGRAVITY]           = simSource[c4d.PBDSCENE_DEFAULTGRAVITY]
    simTarget[c4d.PBDSCENE_TIMESCALE]                = simSource[c4d.PBDSCENE_TIMESCALE]
    simTarget[c4d.PBDSCENE_SCENESCALE]               = simSource[c4d.PBDSCENE_SCENESCALE]
    simTarget[c4d.PBDSCENE_EVALUATEBEFOREGENERATORS] = simSource[c4d.PBDSCENE_EVALUATEBEFOREGENERATORS]
    simTarget[c4d.PBDSCENE_USEDOCUMENT_RANGE]        = simSource[c4d.PBDSCENE_USEDOCUMENT_RANGE]
    simTarget[c4d.PBDSCENE_SIMULATION_FROM]          = simSource[c4d.PBDSCENE_SIMULATION_FROM]
    simTarget[c4d.PBDSCENE_SIMULATION_TO]            = simSource[c4d.PBDSCENE_SIMULATION_TO]
    simTarget[c4d.PBDSCENE_ELEMENTS]                 = simSource[c4d.PBDSCENE_ELEMENTS]
    simTarget[c4d.PBDSCENE_FORCES]                   = simSource[c4d.PBDSCENE_FORCES]
    # Simulation
    simTarget[c4d.PBDSCENE_SUBSTEPS]                = simSource[c4d.PBDSCENE_SUBSTEPS]
    simTarget[c4d.PBDSCENE_ITERATIONS]              = simSource[c4d.PBDSCENE_ITERATIONS]
    simTarget[c4d.PBDSCENE_SMOOTHINGITERATIONS]     = simSource[c4d.PBDSCENE_SMOOTHINGITERATIONS]
    simTarget[c4d.PBDSCENE_DAMPING]                 = simSource[c4d.PBDSCENE_DAMPING]
    simTarget[c4d.PBDSCENE_VELOCITYCLAMP]           = simSource[c4d.PBDSCENE_VELOCITYCLAMP]
    simTarget[c4d.PBDSCENE_ACCELERATIONCLAMP]       = simSource[c4d.PBDSCENE_ACCELERATIONCLAMP]
    simTarget[c4d.PBDSCENE_COLLISIONPASSES]         = simSource[c4d.PBDSCENE_COLLISIONPASSES]
    simTarget[c4d.PBDSCENE_POLISHITERATIONS]        = simSource[c4d.PBDSCENE_POLISHITERATIONS]
    simTarget[c4d.PBDSCENE_POSTCOLLISIONPASSES]     = simSource[c4d.PBDSCENE_POSTCOLLISIONPASSES]
    simTarget[c4d.PBDSCENE_DRAW]                    = simSource[c4d.PBDSCENE_DRAW]
    simTarget[c4d.PBDSCENE_DRAW_PARTICLES]          = simSource[c4d.PBDSCENE_DRAW_PARTICLES]
    simTarget[c4d.PBDSCENE_DRAW_COLLISIONRADIUS]    = simSource[c4d.PBDSCENE_DRAW_COLLISIONRADIUS]
    simTarget[c4d.PBDSCENE_DRAW_EDGES]              = simSource[c4d.PBDSCENE_DRAW_EDGES] # Stretch Constraints
    simTarget[c4d.PBDSCENE_DRAW_TRIANGLEBEND]       = simSource[c4d.PBDSCENE_DRAW_TRIANGLEBEND] # Bend Constraints
    simTarget[c4d.PBDSCENE_DRAW_STRUTS]             = simSource[c4d.PBDSCENE_DRAW_STRUTS] # Pole Constraints
    simTarget[c4d.PBDSCENE_DRAW_CONNECTORS]         = simSource[c4d.PBDSCENE_DRAW_CONNECTORS]
    simTarget[c4d.PBDSCENE_DRAW_RIGIDBODY_CENTERS]  = simSource[c4d.PBDSCENE_DRAW_RIGIDBODY_CENTERS]
    simTarget[c4d.PBDSCENE_DRAW_RIGIDBODY_SHAPES]   = simSource[c4d.PBDSCENE_DRAW_RIGIDBODY_SHAPES]
    # Pyro
    simTarget[c4d.PBDSCENE_PYRO_VOXELSIZE]                              = simSource[c4d.PBDSCENE_PYRO_VOXELSIZE]
    simTarget[c4d.PBDSCENE_PYRO_MASS]                                   = simSource[c4d.PBDSCENE_PYRO_MASS]
    simTarget[c4d.PBDSCENE_PYRO_SUBSTEPS]                               = simSource[c4d.PBDSCENE_PYRO_SUBSTEPS]
    simTarget[c4d.PBDSCENE_PYRO_FORCE_SAMPLES]                          = simSource[c4d.PBDSCENE_PYRO_FORCE_SAMPLES]
    simTarget[c4d.PBDSCENE_PYRO_FIELD_FORCE_SAMPLES]                    = simSource[c4d.PBDSCENE_PYRO_FIELD_FORCE_SAMPLES]
    simTarget[c4d.PBDSCENE_PYRO_INIT_VOLUME_SET]                        = simSource[c4d.PBDSCENE_PYRO_INIT_VOLUME_SET]
    simTarget[c4d.PBDSCENE_PYRO_PADDINGRADIUS]                          = simSource[c4d.PBDSCENE_PYRO_PADDINGRADIUS]
    simTarget[c4d.PBDSCENE_PYRO_TREESETTINGS_VOXELCOUNT]                = simSource[c4d.PBDSCENE_PYRO_TREESETTINGS_VOXELCOUNT]
    simTarget[c4d.PBDSCENE_PYRO_DENSITYBUOYANCY]                        = simSource[c4d.PBDSCENE_PYRO_DENSITYBUOYANCY]
    simTarget[c4d.PBDSCENE_PYRO_TEMPERATUREBUOYANCY]                    = simSource[c4d.PBDSCENE_PYRO_TEMPERATUREBUOYANCY]
    simTarget[c4d.PBDSCENE_PYRO_FUELBUOYANCY]                           = simSource[c4d.PBDSCENE_PYRO_FUELBUOYANCY]
    simTarget[c4d.PBDSCENE_PYRO_VORTICITYSTRENGTH]                      = simSource[c4d.PBDSCENE_PYRO_VORTICITYSTRENGTH]
    simTarget[c4d.PBDSCENE_PYRO_VORTICITY_SOURCE]                       = simSource[c4d.PBDSCENE_PYRO_VORTICITY_SOURCE]
    simTarget[c4d.PBDSCENE_PYRO_VORTICITY_SOURCE_STRENGTH]              = simSource[c4d.PBDSCENE_PYRO_VORTICITY_SOURCE_STRENGTH]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SMOOTH]                      = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SMOOTH]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_STRENGTH]                    = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_STRENGTH]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE]                      = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE_STRENGTH]             = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE_STRENGTH]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE_SCALE_VELOCITY]       = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE_SCALE_VELOCITY]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE_SCALE_VELOCITY_FACTOR]= simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SOURCE_SCALE_VELOCITY_FACTOR]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_TIME_FREQUENCY]              = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_TIME_FREQUENCY]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_OCTAVES]                     = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_OCTAVES]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SPACE_FREQUENCY]             = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SPACE_FREQUENCY]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_SPACE_SCALE]                 = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_SPACE_SCALE]
    simTarget[c4d.PBDSCENE_PYRO_TURBULENCE_STRENGTH_SCALE]              = simSource[c4d.PBDSCENE_PYRO_TURBULENCE_STRENGTH_SCALE]
    simTarget[c4d.PBDSCENE_PYRO_FUELBURNINGRATE]                        = simSource[c4d.PBDSCENE_PYRO_FUELBURNINGRATE]
    simTarget[c4d.PBDSCENE_PYRO_TEMPERATUREIGNITION]                    = simSource[c4d.PBDSCENE_PYRO_TEMPERATUREIGNITION]
    simTarget[c4d.PBDSCENE_PYRO_DENSITYADDPERFUEL]                      = simSource[c4d.PBDSCENE_PYRO_DENSITYADDPERFUEL]
    simTarget[c4d.PBDSCENE_PYRO_TEMPERTUREADDPERFUEL]                   = simSource[c4d.PBDSCENE_PYRO_TEMPERTUREADDPERFUEL]
    simTarget[c4d.PBDSCENE_PYRO_PRESSUREADDPERFUEL]                     = simSource[c4d.PBDSCENE_PYRO_PRESSUREADDPERFUEL]
    simTarget[c4d.PBDSCENE_PYRO_RESTGRID_ENABLED]                       = simSource[c4d.PBDSCENE_PYRO_RESTGRID_ENABLED]
    simTarget[c4d.PBDSCENE_PYRO_RESTGRID_RESET_FPS_CYCLE]               = simSource[c4d.PBDSCENE_PYRO_RESTGRID_RESET_FPS_CYCLE]
    simTarget[c4d.PBDSCENE_PYRO_RESTGRID_TIMESCALE]                     = simSource[c4d.PBDSCENE_PYRO_RESTGRID_TIMESCALE]
    simTarget[c4d.PBDSCENE_PYRO_DENSITYDISSIPATION]                     = simSource[c4d.PBDSCENE_PYRO_DENSITYDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_LINEARDENSITYDISSIPATION]               = simSource[c4d.PBDSCENE_PYRO_LINEARDENSITYDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_BLUR_FACTOR_DENSITY]                    = simSource[c4d.PBDSCENE_PYRO_BLUR_FACTOR_DENSITY]
    simTarget[c4d.PBDSCENE_PYRO_TREE_DENSITY_THRESHOLD]                 = simSource[c4d.PBDSCENE_PYRO_TREE_DENSITY_THRESHOLD]
    simTarget[c4d.PBDSCENE_PYRO_DENSITY_TIMESCALE]                      = simSource[c4d.PBDSCENE_PYRO_DENSITY_TIMESCALE]
    simTarget[c4d.PBDSCENE_PYRO_COLOR_DISSIPATION]                      = simSource[c4d.PBDSCENE_PYRO_COLOR_DISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_COLOR_LINEARDISSIPATION]                = simSource[c4d.PBDSCENE_PYRO_COLOR_LINEARDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_BLUR_FACTOR_COLOR]                      = simSource[c4d.PBDSCENE_PYRO_BLUR_FACTOR_COLOR]
    simTarget[c4d.PBDSCENE_PYRO_COLOR_TIMESCALE]                        = simSource[c4d.PBDSCENE_PYRO_COLOR_TIMESCALE]
    simTarget[c4d.PBDSCENE_PYRO_TEMPERATUREDISSIPATION]                 = simSource[c4d.PBDSCENE_PYRO_TEMPERATUREDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_LINEARTEMPERATUREDISSIPATION]           = simSource[c4d.PBDSCENE_PYRO_LINEARTEMPERATUREDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_BLUR_FACTOR_TEMPERATURE]                = simSource[c4d.PBDSCENE_PYRO_BLUR_FACTOR_TEMPERATURE]
    simTarget[c4d.PBDSCENE_PYRO_TREE_TEMPERATURE_THRESHOLD]             = simSource[c4d.PBDSCENE_PYRO_TREE_TEMPERATURE_THRESHOLD]
    simTarget[c4d.PBDSCENE_PYRO_TEMPERATURE_TIMESCALE]                  = simSource[c4d.PBDSCENE_PYRO_TEMPERATURE_TIMESCALE]
    simTarget[c4d.PBDSCENE_PYRO_FUELDISSIPATION]                        = simSource[c4d.PBDSCENE_PYRO_FUELDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_LINEARFUELDISSIPATION]                  = simSource[c4d.PBDSCENE_PYRO_LINEARFUELDISSIPATION]
    simTarget[c4d.PBDSCENE_PYRO_BLUR_FACTOR_FUEL]                       = simSource[c4d.PBDSCENE_PYRO_BLUR_FACTOR_FUEL]
    simTarget[c4d.PBDSCENE_PYRO_TREE_FUEL_THRESHOLD]                    = simSource[c4d.PBDSCENE_PYRO_TREE_FUEL_THRESHOLD]
    simTarget[c4d.PBDSCENE_PYRO_FUEL_TIMESCALE]                         = simSource[c4d.PBDSCENE_PYRO_FUEL_TIMESCALE]
    simTarget[c4d.PBDSCENE_PYRO_VELOCITY_DAMPING_UNIFORM]               = simSource[c4d.PBDSCENE_PYRO_VELOCITY_DAMPING_UNIFORM]
    simTarget[c4d.PBDSCENE_PYRO_VELOCITY_DAMPING_UNIFORM_ENABLED]       = simSource[c4d.PBDSCENE_PYRO_VELOCITY_DAMPING_UNIFORM_ENABLED]
    simTarget[c4d.PBDSCENE_PYRO_BLUR_FACTOR_VELOCITY]                   = simSource[c4d.PBDSCENE_PYRO_BLUR_FACTOR_VELOCITY]
    simTarget[c4d.PBDSCENE_PYRO_TREE_VELOCITY_THRESHOLD]                = simSource[c4d.PBDSCENE_PYRO_TREE_VELOCITY_THRESHOLD]
    simTarget[c4d.PBDSCENE_PYRO_FLOATPRECISION]                         = simSource[c4d.PBDSCENE_PYRO_FLOATPRECISION]
    simTarget[c4d.PBDSCENE_PYRO_ADVECT_FUEL]                            = simSource[c4d.PBDSCENE_PYRO_ADVECT_FUEL]
    simTarget[c4d.PBDSCENE_PYRO_MACVELOCITIY_ENABLED]                   = simSource[c4d.PBDSCENE_PYRO_MACVELOCITIY_ENABLED]
    simTarget[c4d.PBDSCENE_PYRO_ADVECTIONMODE]                          = simSource[c4d.PBDSCENE_PYRO_ADVECTIONMODE]
    simTarget[c4d.PBDSCENE_PYRO_ADVECTIONMODE_VELOCITIES]               = simSource[c4d.PBDSCENE_PYRO_ADVECTIONMODE_VELOCITIES]
    simTarget[c4d.PBDSCENE_PYRO_ADVECTION_CLAMPING]                     = simSource[c4d.PBDSCENE_PYRO_ADVECTION_CLAMPING]
    simTarget[c4d.PBDSCENE_PYRO_MACCORMACKCORRECT]                      = simSource[c4d.PBDSCENE_PYRO_MACCORMACKCORRECT]
    simTarget[c4d.PBDSCENE_PYRO_PRESSURESOLVER_TYPE]                    = simSource[c4d.PBDSCENE_PYRO_PRESSURESOLVER_TYPE]
    simTarget[c4d.PBDSCENE_PYRO_PRESSURESOLVER_ITERATIONS]              = simSource[c4d.PBDSCENE_PYRO_PRESSURESOLVER_ITERATIONS]
    simTarget[c4d.PBDSCENE_PYRO_PRESSURESOLVER_SMOOTHINGITERATIONS]     = simSource[c4d.PBDSCENE_PYRO_PRESSURESOLVER_SMOOTHINGITERATIONS]
    simTarget[c4d.PBDSCENE_PYRO_PRESSURESOLVER_SMOOTHINGITERATIONSFINAL]= simSource[c4d.PBDSCENE_PYRO_PRESSURESOLVER_SMOOTHINGITERATIONSFINAL]
    simTarget[c4d.PBDSCENE_PYRO_PRESSURESOLVER_MAXIMUMMULTIGRIDDEPTH]   = simSource[c4d.PBDSCENE_PYRO_PRESSURESOLVER_MAXIMUMMULTIGRIDDEPTH]
    simTarget[c4d.PBDSCENE_PYRO_INIT_DENSITY_VOLUME]                    = simSource[c4d.PBDSCENE_PYRO_INIT_DENSITY_VOLUME]
    simTarget[c4d.PBDSCENE_PYRO_INIT_COLOR_VOLUME]                      = simSource[c4d.PBDSCENE_PYRO_INIT_COLOR_VOLUME]
    simTarget[c4d.PBDSCENE_PYRO_INIT_TEMPERATURE_VOLUME]                = simSource[c4d.PBDSCENE_PYRO_INIT_TEMPERATURE_VOLUME]
    simTarget[c4d.PBDSCENE_PYRO_INIT_FUEL_VOLUME]                       = simSource[c4d.PBDSCENE_PYRO_INIT_FUEL_VOLUME]
    simTarget[c4d.PBDSCENE_PYRO_INIT_VELOCITY_VOLUME]                   = simSource[c4d.PBDSCENE_PYRO_INIT_VELOCITY_VOLUME]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_PYRO]                              = simSource[c4d.PBDSCENE_PYRO_DRAW_PYRO]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_GRID]                              = simSource[c4d.PBDSCENE_PYRO_DRAW_GRID]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_TREE]                              = simSource[c4d.PBDSCENE_PYRO_DRAW_TREE]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_DENSITY_SCALE]                     = simSource[c4d.PBDSCENE_PYRO_DRAW_DENSITY_SCALE]
    simTarget[c4d.PBDSCENE_PYRO_RAYMARCH_STEPSIZE]                      = simSource[c4d.PBDSCENE_PYRO_RAYMARCH_STEPSIZE]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_EMISSION_SCALE]                    = simSource[c4d.PBDSCENE_PYRO_DRAW_EMISSION_SCALE]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_TEMPERATURE]                       = simSource[c4d.PBDSCENE_PYRO_DRAW_TEMPERATURE]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_ABSORPTION]                        = simSource[c4d.PBDSCENE_PYRO_DRAW_ABSORPTION]
    simTarget[c4d.PBDSCENE_PYRO_DRAW_TEXTURE]                           = simSource[c4d.PBDSCENE_PYRO_DRAW_TEXTURE]
    simTarget[c4d.PBDSCENE_PYRO_FORCES_INEXMODE]                        = simSource[c4d.PBDSCENE_PYRO_FORCES_INEXMODE]
    simTarget[c4d.PBDSCENE_PYRO_FORCES_INEXCLUDE]                       = simSource[c4d.PBDSCENE_PYRO_FORCES_INEXCLUDE]

def CopyViewSettings(source, target):
    """ Copies viewport settings from source document to target document """
    
    sourceBd = source.GetActiveBaseDraw()
    targetBd = target.GetActiveBaseDraw()
    
    # Active Object (Shading)
    targetBd[c4d.BASEDRAW_DATA_SDISPLAYACTIVE] = sourceBd[c4d.BASEDRAW_DATA_SDISPLAYACTIVE]
    
    # Active Object (Wire)
    targetBd[c4d.BASEDRAW_DATA_WDISPLAYACTIVE] = sourceBd[c4d.BASEDRAW_DATA_WDISPLAYACTIVE]

    # Projection
    targetBd[c4d.BASEDRAW_DATA_PROJECTION] = sourceBd[c4d.BASEDRAW_DATA_PROJECTION]

    # View
    targetBd[c4d.BASEDRAW_DATA_TEXTURES]                    = sourceBd[c4d.BASEDRAW_DATA_TEXTURES]
    targetBd[c4d.BASEDRAW_DATA_USE_LAYERCOLOR]              = sourceBd[c4d.BASEDRAW_DATA_USE_LAYERCOLOR]
    targetBd[c4d.BASEDRAW_DATA_BACKCULL]                    = sourceBd[c4d.BASEDRAW_DATA_BACKCULL]
    targetBd[c4d.BASEDRAW_DATA_XRAY]                        = sourceBd[c4d.BASEDRAW_DATA_XRAY]
    targetBd[c4d.BASEDRAW_DATA_SHOWNORMALS]                 = sourceBd[c4d.BASEDRAW_DATA_SHOWNORMALS]
    targetBd[c4d.BASEDRAW_DATA_SELECTED_NORMALS]            = sourceBd[c4d.BASEDRAW_DATA_SELECTED_NORMALS]
    targetBd[c4d.BASEDRAW_DATA_SHOW_VERTEX_NORMALS]         = sourceBd[c4d.BASEDRAW_DATA_SHOW_VERTEX_NORMALS]
    targetBd[c4d.BASEDRAW_DATA_SELECTED_VERTEX_NORMALS]     = sourceBd[c4d.BASEDRAW_DATA_SELECTED_VERTEX_NORMALS]
    targetBd[c4d.BASEDRAW_DATA_SHOW_POLYGON_INDICES]        = sourceBd[c4d.BASEDRAW_DATA_SHOW_POLYGON_INDICES]
    targetBd[c4d.BASEDRAW_DATA_SHOW_VERTEX_INDICES]         = sourceBd[c4d.BASEDRAW_DATA_SHOW_VERTEX_INDICES]
    targetBd[c4d.BASEDRAW_DATA_DEFORMEDEDIT]                = sourceBd[c4d.BASEDRAW_DATA_DEFORMEDEDIT]
    targetBd[c4d.BASEDRAW_DATA_SDSEDIT]                     = sourceBd[c4d.BASEDRAW_DATA_SDSEDIT]
    targetBd[c4d.BASEDRAW_DATA_USEPROPERTIESACTIVE]         = sourceBd[c4d.BASEDRAW_DATA_USEPROPERTIESACTIVE]
    targetBd[c4d.BASEDRAW_DATA_SHADOW_HINTING]              = sourceBd[c4d.BASEDRAW_DATA_SHADOW_HINTING]

    # Filter
    targetBd[c4d.BASEDRAW_DATA_ONLY_GEOMETRY]               = sourceBd[c4d.BASEDRAW_DATA_ONLY_GEOMETRY]
    targetBd[c4d.BASEDRAW_DATA_ONLY_GEOMETRY_PLAYBACK]      = sourceBd[c4d.BASEDRAW_DATA_ONLY_GEOMETRY_PLAYBACK]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_GRID]               = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_GRID]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_BASEGRID]           = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_BASEGRID]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_WORLDAXIS]          = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_WORLDAXIS]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_HORIZON]            = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_HORIZON]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_HUD]                = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_HUD]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_NULL]               = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_NULL]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_POLYGON]            = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_POLYGON]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_SPLINE]             = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_SPLINE]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_GENERATOR]          = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_GENERATOR]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_HYPERNURBS]         = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_HYPERNURBS]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_DEFORMER]           = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_DEFORMER]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_FIELD]              = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_FIELD]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_SCENE]              = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_SCENE]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_CAMERA]             = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_CAMERA]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_LIGHT]              = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_LIGHT]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_JOINT]              = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_JOINT]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_PARTICLE]           = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_PARTICLE]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_HAIR]               = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_HAIR]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_GUIDELINES]         = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_GUIDELINES]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_OTHER]              = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_OTHER]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_OBJECTHANDLES]      = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_OBJECTHANDLES]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_MULTIAXIS]          = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_MULTIAXIS]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_HANDLES]            = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_HANDLES]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_OBJECTHIGHLIGHTING] = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_OBJECTHIGHLIGHTING]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_HIGHLIGHTING]       = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_HIGHLIGHTING]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_SDS]                = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_SDS]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_SDSCAGE]            = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_SDSCAGE]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_NGONLINES]          = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_NGONLINES]
    targetBd[c4d.BASEDRAW_DATA_SHOWPATH]                    = sourceBd[c4d.BASEDRAW_DATA_SHOWPATH]
    targetBd[c4d.BASEDRAW_DISPLAYFILTER_ONION]              = sourceBd[c4d.BASEDRAW_DISPLAYFILTER_ONION]

    # Safe Frames
    targetBd[c4d.BASEDRAW_DATA_SHOWSAFEFRAME]               = sourceBd[c4d.BASEDRAW_DATA_SHOWSAFEFRAME]
    targetBd[c4d.BASEDRAW_DATA_TITLESAFE]                   = sourceBd[c4d.BASEDRAW_DATA_TITLESAFE]
    targetBd[c4d.BASEDRAW_DATA_TITLESAFE_SIZE]              = sourceBd[c4d.BASEDRAW_DATA_TITLESAFE_SIZE]
    targetBd[c4d.BASEDRAW_DATA_ACTIONSAFE]                  = sourceBd[c4d.BASEDRAW_DATA_ACTIONSAFE]
    targetBd[c4d.BASEDRAW_DATA_ACTIONSAFE_SIZE]             = sourceBd[c4d.BASEDRAW_DATA_ACTIONSAFE_SIZE]
    targetBd[c4d.BASEDRAW_DATA_RENDERSAFE]                  = sourceBd[c4d.BASEDRAW_DATA_RENDERSAFE]
    targetBd[c4d.BASEDRAW_DATA_TINTBORDER]                  = sourceBd[c4d.BASEDRAW_DATA_TINTBORDER]
    targetBd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY]          = sourceBd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY]
    targetBd[c4d.BASEDRAW_DATA_TINTBORDER_COLOR]            = sourceBd[c4d.BASEDRAW_DATA_TINTBORDER_COLOR]

    # HUD
    targetBd[c4d.BASEDRAW_HUD_CAMERA_NAME]                  = sourceBd[c4d.BASEDRAW_HUD_CAMERA_NAME]
    targetBd[c4d.BASEDRAW_HUD_CAMERADISTANCE]               = sourceBd[c4d.BASEDRAW_HUD_CAMERADISTANCE]
    targetBd[c4d.BASEDRAW_HUD_PROJECTION_NAME]              = sourceBd[c4d.BASEDRAW_HUD_PROJECTION_NAME]
    targetBd[c4d.BASEDRAW_HUD_FPS]                          = sourceBd[c4d.BASEDRAW_HUD_FPS]
    targetBd[c4d.BASEDRAW_HUD_FRAME]                        = sourceBd[c4d.BASEDRAW_HUD_FRAME]
    targetBd[c4d.BASEDRAW_HUD_FRAMETIME]                    = sourceBd[c4d.BASEDRAW_HUD_FRAMETIME]
    targetBd[c4d.BASEDRAW_HUD_TIMELINE_MARKERS]             = sourceBd[c4d.BASEDRAW_HUD_TIMELINE_MARKERS]
    targetBd[c4d.BASEDRAW_HUD_ACTIVE_OBJECT]                = sourceBd[c4d.BASEDRAW_HUD_ACTIVE_OBJECT]
    targetBd[c4d.BASEDRAW_HUD_ROOT_OBJECT]                  = sourceBd[c4d.BASEDRAW_HUD_ROOT_OBJECT]
    targetBd[c4d.BASEDRAW_HUD_PARENT_OBJECT]                = sourceBd[c4d.BASEDRAW_HUD_PARENT_OBJECT]
    targetBd[c4d.BASEDRAW_HUD_TOTAL_OBJECTS]                = sourceBd[c4d.BASEDRAW_HUD_TOTAL_OBJECTS]
    targetBd[c4d.BASEDRAW_HUD_SELECTED_OBJECTS]             = sourceBd[c4d.BASEDRAW_HUD_SELECTED_OBJECTS]
    targetBd[c4d.BASEDRAW_HUD_TOTAL_POINTS]                 = sourceBd[c4d.BASEDRAW_HUD_TOTAL_POINTS]
    targetBd[c4d.BASEDRAW_HUD_SELECTED_POINTS]              = sourceBd[c4d.BASEDRAW_HUD_SELECTED_POINTS]
    targetBd[c4d.BASEDRAW_HUD_TOTAL_EDGES]                  = sourceBd[c4d.BASEDRAW_HUD_TOTAL_EDGES]
    targetBd[c4d.BASEDRAW_HUD_SELECTED_EDGES]               = sourceBd[c4d.BASEDRAW_HUD_SELECTED_EDGES]
    targetBd[c4d.BASEDRAW_HUD_TOTAL_POLYGONS]               = sourceBd[c4d.BASEDRAW_HUD_TOTAL_POLYGONS]
    targetBd[c4d.BASEDRAW_HUD_SELECTED_POLYGONS]            = sourceBd[c4d.BASEDRAW_HUD_SELECTED_POLYGONS]
    targetBd[c4d.BASEDRAW_HUD_TOTAL_NGONS]                  = sourceBd[c4d.BASEDRAW_HUD_TOTAL_NGONS]
    targetBd[c4d.BASEDRAW_HUD_SELECTED_NGONS]               = sourceBd[c4d.BASEDRAW_HUD_SELECTED_NGONS]
    targetBd[c4d.BASEDRAW_HUD_DRAW_STATISTICS]              = sourceBd[c4d.BASEDRAW_HUD_DRAW_STATISTICS]
    targetBd[c4d.BASEDRAW_HUD_SCULPT_STATISTICS]            = sourceBd[c4d.BASEDRAW_HUD_SCULPT_STATISTICS]
    targetBd[c4d.BASEDRAW_HUD_TAKE]                         = sourceBd[c4d.BASEDRAW_HUD_TAKE]
    targetBd[c4d.BASEDRAW_HUD_RENDERSETTINGS]               = sourceBd[c4d.BASEDRAW_HUD_RENDERSETTINGS]
    targetBd[c4d.BASEDRAW_HUD_TOOL]                         = sourceBd[c4d.BASEDRAW_HUD_TOOL]
    targetBd[c4d.BASEDRAW_HUD_WORKPLANE_STATISTICS]         = sourceBd[c4d.BASEDRAW_HUD_WORKPLANE_STATISTICS]
    targetBd[c4d.BASEDRAW_HUD_VIEW_COLORSPACE]              = sourceBd[c4d.BASEDRAW_HUD_VIEW_COLORSPACE]
    targetBd[c4d.BASEDRAW_HUD_BACKCOLOR]                    = sourceBd[c4d.BASEDRAW_HUD_BACKCOLOR]
    targetBd[c4d.BASEDRAW_HUD_BACKOPACITY]                  = sourceBd[c4d.BASEDRAW_HUD_BACKOPACITY]
    targetBd[c4d.BASEDRAW_HUD_TEXTCOLOR]                    = sourceBd[c4d.BASEDRAW_HUD_TEXTCOLOR]
    targetBd[c4d.BASEDRAW_HUD_TEXTOPACITY]                  = sourceBd[c4d.BASEDRAW_HUD_TEXTOPACITY]
    targetBd[c4d.BASEDRAW_HUD_SELECTCOLOR]                  = sourceBd[c4d.BASEDRAW_HUD_SELECTCOLOR]
    targetBd[c4d.BASEDRAW_HUD_ALWAYSACTIVE]                 = sourceBd[c4d.BASEDRAW_HUD_ALWAYSACTIVE]

    # Effects
    targetBd[c4d.BASEDRAW_DATA_HQ_VIEWPORT]                        = sourceBd[c4d.BASEDRAW_DATA_HQ_VIEWPORT]
    targetBd[c4d.BASEDRAW_DATA_HQ_NOISES]                          = sourceBd[c4d.BASEDRAW_DATA_HQ_NOISES]
    targetBd[c4d.BASEDRAW_DATA_HQ_TRANSPARENCY]                    = sourceBd[c4d.BASEDRAW_DATA_HQ_TRANSPARENCY]
    targetBd[c4d.BASEDRAW_DATA_COMPLETE_MATERIAL_TRANSPARENCY]     = sourceBd[c4d.BASEDRAW_DATA_COMPLETE_MATERIAL_TRANSPARENCY]
    targetBd[c4d.BASEDRAW_DATA_HQ_SHADOWS]                         = sourceBd[c4d.BASEDRAW_DATA_HQ_SHADOWS]
    targetBd[c4d.BASEDRAW_DATA_SHADOW_SOFTSHADOW_ATTENUATION]      = sourceBd[c4d.BASEDRAW_DATA_SHADOW_SOFTSHADOW_ATTENUATION]
    targetBd[c4d.BASEDRAW_DATA_SHADOW_TYPE]                        = sourceBd[c4d.BASEDRAW_DATA_SHADOW_TYPE]
    targetBd[c4d.BASEDRAW_DATA_SHADOW_MAP_SIZE]                    = sourceBd[c4d.BASEDRAW_DATA_SHADOW_MAP_SIZE]
    targetBd[c4d.BASEDRAW_DATA_SHADOW_PCF]                         = sourceBd[c4d.BASEDRAW_DATA_SHADOW_PCF]
    targetBd[c4d.BASEDRAW_DATA_HQ_REFLECTIONS]                     = sourceBd[c4d.BASEDRAW_DATA_HQ_REFLECTIONS]
    targetBd[c4d.BASEDRAW_DATA_REFLECTIONS_ENV_OVERRIDE]           = sourceBd[c4d.BASEDRAW_DATA_REFLECTIONS_ENV_OVERRIDE]
    targetBd[c4d.BASEDRAW_DATA_REFLECTIONS_ENV_ROTATION]           = sourceBd[c4d.BASEDRAW_DATA_REFLECTIONS_ENV_ROTATION]
    targetBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR]                    = sourceBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR]
    targetBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR_ITERATIONS]         = sourceBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR_ITERATIONS]
    targetBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR_GEOMETRY_THICKNESS] = sourceBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR_GEOMETRY_THICKNESS]
    targetBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR_HALF_RES]           = sourceBd[c4d.BASEDRAW_DATA_REFLECTIONS_SSR_HALF_RES]
    targetBd[c4d.BASEDRAW_DATA_HQ_POST_EFFECTS]                    = sourceBd[c4d.BASEDRAW_DATA_HQ_POST_EFFECTS]
    targetBd[c4d.BASEDRAW_DATA_HQ_MAGICBULLETLOOKS]                = sourceBd[c4d.BASEDRAW_DATA_HQ_MAGICBULLETLOOKS]
    targetBd[c4d.BASEDRAW_DATA_HQ_SSAO]                            = sourceBd[c4d.BASEDRAW_DATA_HQ_SSAO]
    targetBd[c4d.BASEDRAW_DATA_SSAO_RADIUS]                        = sourceBd[c4d.BASEDRAW_DATA_SSAO_RADIUS]
    targetBd[c4d.BASEDRAW_DATA_SSAO_THRESHOLD]                     = sourceBd[c4d.BASEDRAW_DATA_SSAO_THRESHOLD]
    targetBd[c4d.BASEDRAW_DATA_SSAO_POWER]                         = sourceBd[c4d.BASEDRAW_DATA_SSAO_POWER]
    targetBd[c4d.BASEDRAW_DATA_SSAO_SAMPLES]                       = sourceBd[c4d.BASEDRAW_DATA_SSAO_SAMPLES]
    targetBd[c4d.BASEDRAW_DATA_SSAO_FINEDETAIL]                    = sourceBd[c4d.BASEDRAW_DATA_SSAO_FINEDETAIL]
    targetBd[c4d.BASEDRAW_DATA_SSAO_BLUR]                          = sourceBd[c4d.BASEDRAW_DATA_SSAO_BLUR]
    targetBd[c4d.BASEDRAW_DATA_SSAO_MODE]                          = sourceBd[c4d.BASEDRAW_DATA_SSAO_MODE]
    targetBd[c4d.BASEDRAW_DATA_HQ_TESSELLATION]                    = sourceBd[c4d.BASEDRAW_DATA_HQ_TESSELLATION]
    targetBd[c4d.BASEDRAW_DATA_HQ_DEPTHOFFIELD]                    = sourceBd[c4d.BASEDRAW_DATA_HQ_DEPTHOFFIELD]
    targetBd[c4d.BASEDRAW_DATA_DEPTHOFFIELD_MAXRADIUS]             = sourceBd[c4d.BASEDRAW_DATA_DEPTHOFFIELD_MAXRADIUS]
    targetBd[c4d.BASEDRAW_DATA_DEPTHOFFIELD_ANTIALIASED]           = sourceBd[c4d.BASEDRAW_DATA_DEPTHOFFIELD_ANTIALIASED]
    targetBd[c4d.BASEDRAW_DATA_SUPERSAMPLING]                      = sourceBd[c4d.BASEDRAW_DATA_SUPERSAMPLING]
    targetBd[c4d.BASEDRAW_DATA_VIEWPORT_CONTENT_SCALE]             = sourceBd[c4d.BASEDRAW_DATA_VIEWPORT_CONTENT_SCALE]

def CopyRenderSettings(source, target):
    """ Copies render settings from source document to target document """

    renderDataList = CollectRenderData(source)
    for renderData in reversed(renderDataList):
        target.InsertRenderData(renderData.GetClone(), None, None)

def GetRenderSettings(document):
    """ Get render settings of the document """

    renderDataList = CollectRenderData(source)
    for renderData in renderDataList:
        target.InsertRenderData(renderData, None, None)

def DeleteRenderSettings(document, renderDataList):
    """ Delete render settings"""

    for renderData in renderDataList:
        renderData.Remove()

def GetActiveCameraName(document):
    """ Get active camera's name """

    bd = document.GetActiveBaseDraw() # Get active base draw
    activeCam = bd.GetSceneCamera(document) # Get active camera
    return activeCam.GetName() # Get active camera's name

def SetActiveRenderSettingsByName(document, name):
    """ Set active render settings by name """

    renderDataList = CollectRenderData(document)
    for renderData in renderDataList:
        if renderData.GetName() == name:
            document.SetActiveRenderData(renderData)

def MergeDocument(path, objects = True, materials = True, documentSettings = True, renderSettings = True, viewportSettings = True, camera = True):
    """ Merge document """

    newDoc = documents.BaseDocument() # Initialize a new document
    if newDoc is None: return None # If no document, return 'None'
    
    # Flags
    if (objects == True) and (materials == True): # If import objects and materials is true
        flags = c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS # Flags
    elif (objects == True): # If import objects is true
        flags = c4d.SCENEFILTER_OBJECTS # Flags
    elif (materials == True): # If import materials is true
        flags = c4d.SCENEFILTER_MATERIALS # Flags
    
    # Documents
    tempDoc = documents.LoadDocument(path, flags, None) # Load the document
    documents.MergeDocument(newDoc, path, flags, None) # Merge document

    documents.InsertBaseDocument(newDoc) # Insert new document
    documents.SetActiveDocument(newDoc) # Set active document

    # Document settings
    if documentSettings == True: # If import document settings is true
        CopyDocumentSettings(tempDoc, newDoc) # Copy project settings

    # Viewport settings
    if viewportSettings == True: # If import viewport settings is true
        CopyViewSettings(tempDoc, newDoc) # Copy viewport settings

    # Active camera
    if camera == True: # If set camera is true
        camName = GetActiveCameraName(tempDoc) # Get active camera's name
        searchCam = newDoc.SearchObject(camName) # Search camera by name
        newBd = newDoc.GetActiveBaseDraw() # Get active base draw
        newBd.SetSceneCamera(searchCam) # Set active camera

    # Render settings
    if renderSettings == True: # If import render settings is true
        activeRenderDataName = tempDoc.GetActiveRenderData().GetName() # Get name of the active render data
        oldRenderSettings = CollectRenderData(newDoc) # Get old render settings
        CopyRenderSettings(tempDoc, newDoc) # Copy render settings
        DeleteRenderSettings(newDoc, oldRenderSettings) # Delete old render settings
        SetActiveRenderSettingsByName(newDoc, activeRenderDataName) # Set active render settings

    c4d.EventAdd() # Refresh Cinema 4D