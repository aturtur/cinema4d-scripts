"""
AR_TglEnable

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TglEnable
Version: 1.0.8
Description-US: Enables or disables generator. Shift: Toggle next parent generator. Ctrl: Toggle root generator. Alt: Toggle generator family

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Similar to Cinema 4D's own Toggle Parent Generator script, but just a lot better ;)

DEFAULT: Toggle selected
SHIFT: Toggle next parent generator from common list
CTRL: Toggle root parent generator from common list
ALT: Toggle all parent generators from common list
ALT+SHIFT: Force disable
ALT+CTRL: Force enable
CTRL+SHIFT: Toggle from custom list.
ALT+CTRL+SHIFT: Open textfile to modify custom. You can use hashtag '#' separating comments. Put each generator to own line!

Change log:
1.0.8 (23.09.2022) - Added Insydium NeXus stuff.
1.0.7 (29.03.2022) - Instead of carrying txt-file for options along with the script, it will create options file to C4D's preference folder.
1.0.6 (23.03.2022) - Added support Insydium stuff.
1.0.5 (20.10.2021) - Updated for R25.
1.0.4 (21.11.2020) - Added support for many different generators that were missed.
1.0.3 (13.11.2020) - Support for alembic generators.
1.0.2 (08.11.2020) - Added Alt+Shift and Alt+Ctrl shortcuts to force disable and enable.
                     Added also Ctrl+Shift and Alt+Ctrl+Shift for toggling generators based on custom list and for editing custom list.
1.0.1 (04.11.2020) - Support for Redshift objects (lights, proxy, sky, environment)
"""

import c4d
import os
import sys
from c4d import storage

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

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_TglEnable.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.close()
    return filePath

def ToggleEnable(op):
    status = op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, op)
    op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = not op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] # Toggle generator
    if status is not op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]: return True
    else: return False

def Enable(op):
    status = op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, op)
    op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = True
    if status is not op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]: return True
    else: return False

def Disable(op):
    status = op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, op)
    op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = False
    if status is not op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]: return True
    else: return False

def GetRoot(obj):
    while obj: # Infinite loop
        if obj.GetUp() == None: # If object has no parent
            return obj # Return object
            break # Break the loop
        obj = obj.GetUp() # Object is object's parent

# Main function
def main():
    deformers = [431000028, # Bevel 0
                5149,       # Wind 0
                1019768,    # Morph 0
                5146,       # Formula 0
                1018685,    # Displacer 0
                1019221,    # Spline Wrap 0
                1008796,    # Spline Rail 0
                1008982,    # Spline 0
                5143,       # Wrap 0
                1024552,    # Surface 0
                1024529,    # Smoothing 0
                1001003,    # Spherify 0
                1019774,    # Shrink Wrap 0
                1024544,    # Collision 0
                1021280,    # Squash & Stretch 0
                1021284,    # Jiggle 0
                5148,       # Shatter 0
                5147,       # Melt 0
                1002603,    # Explosion FX 0
                5145,       # Explosion 0
                1024543,    # Mesh 0
                5108,       # FFD 0
                1024542,    # Correction 0
                1024476,    # Camera 0
                5134,       # Twist 0
                5133,       # Taper 0
                5131,       # Shear 0
                5129,       # Bulge 0
                5128,       # Bend 0
                1035447]    # Delta Mush 0

    objects = [1027657,     # Guide 0
                5120,       # Bezier 0
                5169,       # Landscape 0
                5166,       # Figure 0
                5161,       # Platonic 0
                5167,       # Pyramid 0
                5165,       # Tube 0
                5172,       # Oil Tank 0
                5171,       # Capsule 0
                5163,       # Torus 0
                5160,       # Sphere 0
                5174,       # Polygon 0
                5168,       # Plane 0
                5164,       # Disc 0
                5170,       # Cylinder 0
                5162,       # Cone 0
                5159]       # Cube 0

    splines = [5188,        # Cogwheel 0
                5186,       # Rectangle 0
                5175,       # Profile 0
                5183,       # Cissoid 0
                5179,       # n-Side 0
                5176,       # Flower 0
                5180,       # 4-Side 0
                5185,       # Helix 0
                5177,       # Formula 0
                5178,       # Text 0
                5181,       # Circle 0
                5184,       # Cycloid 0
                5187,       # Star 0
                5182,       # Arc 0
                5101]       # Spline 0

    generators = [5142,     # Symmetry 0
                1001002,    # Atom Array 1
                5125,       # Metaball 1
                5150,       # Array 1
                465002101,  # Polygon Reduction 1
                5126,       # LOD Instance 1
                431000174,  # LOD 1
                1011010,    # Connect 1
                100004007,  # Cloth Surface 1
                1023866,    # Python Generator 0
                1010865,    # Boole 1
                1007455,    # Subdivision Surface 1
                5118,       # Sweep 1
                5107,       # Loft 1
                5189,       # Vectorizer 0
                5117,       # Lathe 1
                1019396,    # Spline Mask 1
                5116,       # Extrude 1
                1057899,    # Vector Import 0
                1054750]    # Remesh 1

    mggenerators = [1018957, # MoInstance 1
                1019268,     # MoText 0
                440000054,   # MoSpline 0
                1018655,     # Tracer 0
                1018791,     # Fracture
                1036557,     # Voronoi Fracture 1
                1018545,     # Matrix 0
                1018544]     # Cloner 1

    mgeffectors = [1019351, # Group 0
                1021287,    # Volume 0
                1018935,    # Time 0
                1018889,    # Target 0
                1018881,    # Step 0
                1018774,    # Spline 0
                440000255,  # Sound 0
                1018561,    # Shader 0
                440000234,  # ReEffector 0
                1018643,    # Random 0
                1025800,    # Python 0
                440000219,  # Push Apart 0
                1018775,    # Inheritance 0
                1018883,    # Formula 0
                1019234,    # Delay 0
                1021337,    # Plain 0
                1019222,    # PolyFX 0
                1019358]    # MoExtrude 0

    fields = [440000277,   # Python Field 0
                440000268, # Cylinder Field 0
                440000280, # Formula Field 0
                1040449,   # Group Field 0
                440000267, # Box Field 0
                440000283, # Sound Field 0
                440000272, # Torus Field 0
                440000243, # Spherical Field 0
                440000282, # Shader Field 0
                440000274, # Capsule Field 0
                1040448,   # Radial Field 0
                440000281, # Random Field 0
                440000269, # Cone Field 0
                440000266] # Linear Field 0

    particles = [5109,     # Emitter
                 5119,     # Attractor
                 5110,     # Deflector
                 5124,     # Destructor
                 1041451,  # Field Force
                 5114,     # Friction
                 5111,     # Gravity
                 5112,     # Rotation
                 5115,     # Turbulence
                 5113,     # Wind
                 1001414]  # TP Geometry

    connectors = [180000011, # Connector
                  180000010, # Spring
                  180000103, # Force
                  180000012] # Motor

    others = [5102,      # Light 0
                1011196, # Cloud 1
                1011194, # Cloud Group 0
                1011146, # Physical Sky 0
                1039862, # Vector Smooth 0
                1039862, # Fog Smooth 0
                1039862, # SDF Smooth 0
                1039861, # Volume Mesher 1
                1039859, # Volume Builder 1
                1039866, # Volume Loader 0
                1025766, # XRef 0
                1021824, # CMotion 0
                1021433, # Character 0
                1021283, # Cluster 0
                1026352, # MSkin 0
                1026224, # Muscle 0
                1019363, # Skin 0
                5136,    # Stage
                1028083, # Alembic
                1017305, # Hair
                1018958, # Fur
                1018396] # Feather

    scenenodes = [180420400] # Scene Nodes Deformer 0

    redshift = [1036751, # RS Light
                1036754, # RS Sky
                1038649, # RS Proxy
                1038655, # RS Volume
                1036757] # RS Environment

    thirdparty = [1023131, # TurbulenceFD Container
                  1035497, # Forester Tree
                  1035502, # Forester Rock
                  1035500, # Forester MultiCloner
                  1034620] # Forester MultiFlora

    insydium = [1027397, # xpSystem                 X-Particles Systems
                1032129, # Dynamics Null
                1029010, # Groups Null
                1028885, # Emitter Null
                1027133, # xpEmitter
                1028886, # Generators Null
                1033749, # Utilities Null
                1027937, # Modifiers Null
                1027928, # Questions Null
                1027320, # Actions Null
                1028775, # xpCache
                1041714, # xpWave                    Dynamics
                1050919, # xpSplash
                1052656, # xpSheeter
                1033823, # xpPPCollisions
                1039948, # xpFoam
                1033824, # xpFluidPBD
                1039102, # xpFluidFX
                1033595, # xpFluidFLIP
                1037389, # xpFluidField
                1054110, # xpFlock
                1039162, # xpExplosiaFX
                1033777, # xpConstraints
                1056267, # xpBulletConstraints
                1039394, # xpSurface
                1037196, # xpClothModifier
                1037952, # xpClothDeformer
                1027501, # xpTrail                  Generators
                1027664, # xpSprite
                1032145, # xpSplineMesher
                1051457, # xpShatter
                1053645, # xpScatter
                1037247, # xpPlanarMesher
                1036829, # xpOpenVDBMesher
                1054871, # xpOcean
                1027654, # xpGenerator
                1031138, # xpFragmenter
                1032188, # xpElektrix
                1050472, # xpDisplayRender
                1036792, # xpCellAuto
                1032041, # xpTendril                Modifiers
                1036512, # xpMultiSpawn
                1027705, # xpSpawn
                1029117, # xpMorph
                1027711, # xpGeometry
                1033835, # xpDynamicParticles
                1031838, # xpBranch
                1029133, # xpText
                1029093, # xpSpriteShaderControl
                1028062, # xpSpriteControl
                1027988, # xpLight
                1029148, # xpWind
                1033565, # xpVortex
                1027629, # xpTurbulence
                1039337, # xpStrangeAttractors
                1053162, # xpSticky
                1039087, # xpSplineFlow
                1039972, # xSplineFlowHandle
                1027710, # xpSpin
                1027668, # xpSpeed
                1039451, # xpSoundDisplacement
                1029151, # xpRotator
                1053417, # xpPushAPart
                1031609, # xpNetwork
                1031969, # xpLimit
                1027669, # xpGravity
                1031213, # xpFollowSurface
                1029994, # xpFollowSpline
                1030775, # xpFollowPath
                1032295, # xpExplode
                1034299, # xpDrag
                1027694, # xpDirection
                1027732, # xpCover
                1032382, # xpAvoid
                1029473, # xpAttractor
                1031653, # xpWeight
                1028231, # xpUnlinkTP
                1030914, # xpTriggerAction
                1032143, # xpTransform
                1036163, # xpTrailsMod
                1035482, # xpSound
                1027708, # xpScale
                1030729, # xpPython
                1033736, # xpPhysical
                1027691, # xpLife
                1053149, # xpNegate
                1030476, # xpKill
                1033797, # xpInherit
                1041316, # xpInfectio
                1039375, # xpHistory
                1027690, # xpFreeze
                1036926, # xpCustomData
                1031808, # xpColor
                1028704, # xpChangeGroup
                1054078, # xpBlend
                1057327, # mtDualGraph              Mesh Tools
                1057180, # mtEdgeSpline
                1057181, # mtInset
                1058738, # mtPolyScale
                1057238, # mtSelect
                1057182, # mtShellGen
                1057184, # mtShortestPath
                1058644, # mtSplineSample
                1057183, # mtSubDivider
                1058821, # mtRemesh
                1054563, # tfTerrain                Terrain Tools
                1057892, # tfRoad
                1057415, # tfRock
                1054581, # tfGroup
                1054623, # tfGradient
                1055913, # tfGrid
                1054581, # tfGroup
                1054566, # tfNoise
                1054617, # tfShader
                1054654, # tfSpline
                1054574, # tfAdjustment
                1054618, # tfBlur
                1054609, # tfClamp
                1054582, # tfCurve
                1054690, # tfErosion
                1055664, # tfFold
                1058400, # tfHighpass
                1054640, # tfMirror
                1057857, # tfPath
                1056548, # tfQuantize
                1056139, # tfSharpen
                1053611, # cySpotLight              Cycles 4D
                1053083, # cyRingLight
                1053076, # cySoftBox
                1055680, # cyVolume
                1056015, # cySky
                1037688, # cyEnvironment
                1058347, # toPlant                  Taio
                1058580, # toGrass
                1058015, # toTree
                1059838, # nxWind                   NeXus
                1059907, # nxVorticity
                1059404, # nxTurbulence
                1059801, # nxSpeed
                1059802, # nxScale
                1059773, # nxPush
                1059789, # nxRotate
                1059792, # nxKill
                1059389, # nxGravity
                1059816, # nxExplode
                1059774, # nxDrag
                1059803, # nxDirection
                1059788, # nxBlend
                1059785, # nxAttract
                1059731, # nxFoam
                1059048, # nxFluids
                1059475  # nxConstraints
    ]

    default = generators + mggenerators
    allGenerators = deformers + objects + splines + generators + mggenerators + mgeffectors + fields + particles + connectors + others + scenenodes + redshift + insydium + thirdparty

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    #try:
    # Get selected objects and iterate through those
    selection = doc.GetActiveObjects(1) # Get selection
    for s in selection: # Iterate through selected objects
        x = s
        # 1. Enable/disable every possible generator
        if keyMod == "None":
            if len(selection) == 1:
                if x.GetType() in allGenerators:
                    ToggleEnable(x)
                else:
                    while(True):
                        x = x.GetUp()
                        if x is None: break
                        if x.GetType() in default:
                            success = ToggleEnable(x)
                            if success: break
            else:
                ToggleEnable(x)

        # 2. Enable/disable next parent generator from common list (SHIFT)
        elif keyMod == "Shift":
            while(True):
                x = x.GetUp()
                if x is None: break
                if x.GetType() in default:
                    success = ToggleEnable(x)
                    if success: break

        # 3. Enable/disable root parent generator from common list (CTRL)
        elif keyMod == "Ctrl":
            lastGen = None
            while(True):
                if x is None: break
                if x.GetType() in default:
                    lastGen = x
                x = x.GetUp()
            if lastGen != None:
                ToggleEnable(lastGen)

        # 4. Enable/disable all parent generators from common list (ALT)
        elif keyMod == "Alt": # Enable/disable next parent generator from common list
            while(True):
                if x is None: break
                if x.GetType() in default:
                    success = ToggleEnable(x)
                x = x.GetUp()

        # 5. Force disable (ALT + CTRL)
        elif keyMod == "Alt+Ctrl":
            Disable(x)

        # 6. Force enable (ALT + SHIFT)
        elif keyMod == "Alt+Shift":
            Enable(x)

        # 7. Toggle custom
        elif keyMod == "Ctrl+Shift":
            filePath = CheckFiles() # Check required files and folders
            customGenerators = [] # Initialize list for custom generators
            if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
                f = open(filePath)
            else: # If Python 2 version (R21)
                f = open(filePath.decode("utf-8"))
            for line in f: # Iterate through every row
                line = line.split("#") # Split by hashtag (comment)
                customGenerators.append(int(line[0])) # Add generator to the list
            if x.GetType() in customGenerators:
                ToggleEnable(x)
            else:
                while(True):
                    x = x.GetUp()
                    if x is None: break
                    if x.GetType() in customGenerators:
                        success = ToggleEnable(x)
                        if success: break

    # 8. Open textfile to modify custom
    if keyMod == "Alt+Ctrl+Shift":
        filePath = CheckFiles() # Check required files and folders
        storage.GeExecuteFile(filePath) # Open data file for editing custom generators
        pass

    #except:
        #pass

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()