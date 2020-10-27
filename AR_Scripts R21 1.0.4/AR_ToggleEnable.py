"""
AR_ToggleEnable

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ToggleEnable
Version: 1.0
Description-US: Enables or disables generator. SHIFT: Toggle next parent generator. CTRL: Toggle root generator. ALT: Toggle generator family

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Similar to Cinema 4D's own Toggle Parent Generator script, but better ;)
"""
import c4d

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

def ToggleEnable(op):
    status = op[c4d.ID_BASEOBJECT_GENERATOR_FLAG]
    doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, op)
    op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] = not op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] # Toggle generator
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
    deformers = [431000028, #Bevel 0
                5149, #Wind 0
                1019768, #Morph 0
                5146, #Formula 0
                1018685, #Displacer 0
                1019221, #Spline Wrap 0
                1008796, #Spline Rail 0
                1008982, #Spline 0
                5143, #Wrap 0
                1024552, #Surface 0
                1024529, #Smoothing 0
                1001003, #Spherify 0
                1019774, #Shrink Wrap 0
                1024544, #Collision 0
                1021280, #Squash & Stretch 0
                1021284, #Jiggle 0
                5148, #Shatter 0
                5147, #Melt 0
                1002603, #Explosion FX 0
                5145, #Explosion 0
                1024543, #Mesh 0
                5108, #FFD 0
                1024542, #Correction 0
                1024476, #Camera 0
                5134, #Twist 0
                5133, #Taper 0
                5131, #Shear 0
                5129, #Bulge 0
                5128] #Bend 0

    objects = [1027657, #Guide 0
                5120, #Bezier 0
                5169, #Landscape 0
                5166, #Figure 0
                5161, #Platonic 0
                5167, #Pyramid 0
                5165, #Tube 0
                5172, #Oil Tank 0
                5171, #Capsule 0
                5163, #Torus 0
                5160, #Sphere 0
                5174, #Polygon 0
                5168, #Plane 0
                5164, #Disc 0
                5170, #Cylinder 0
                5162, #Cone 0
                5159] #Cube 0

    splines = [5188, #Cogwheel 0
                5186, #Rectangle 0
                5175, #Profile 0
                5183, #Cissoid 0
                5179, #n-Side 0
                5176, #Flower 0
                5180, #4-Side 0
                5185, #Helix 0
                5177, #Formula 0
                5178, #Text 0
                5181, #Circle 0
                5184, #Cycloid 0
                5187, #Star 0
                5182, #Arc 0
                5101] #Spline 0

    generators = [5142, #Symmetry 0
                1001002, #Atom Array 1
                5125, #Metaball 1
                5150, #Array 1
                465002101, #Polygon Reduction 1
                5126, #LOD Instance 1
                431000174, #LOD 1
                1011010, #Connect 1
                100004007, #Cloth Surface 1
                1023866, #Python Generator 0
                1010865, #Boole 1
                1007455, #Subdivision Surface
                5118, #Sweep 1
                5107, #Loft 1
                5189, #Vectorizer 0
                5117, #Lathe 1
                1019396, #Spline Mask 1
                5116] #Extrude 1

    mggenerators = [1018957, #MoInstance 1
                1019268, #MoText 0
                440000054, #MoSpline 0
                1018655, #Tracer 0
                1018791, #Fracture
                1036557, #Voronoi Fracture 1
                1018545, #Matrix 0
                1018544] #Cloner 1

    mgeffectors = [1019351, #Group 0
                1021287, #Volume 0
                1018935, #Time 0
                1018889, #Target 0
                1018881, #Step 0
                1018774, #Spline 0
                440000255, #Sound 0
                1018561, #Shader 0
                440000234, #ReEffector 0
                1018643, #Random 0
                1025800, #Python 0
                440000219, #Push Apart 0
                1018775, #Inheritance 0
                1018883, #Formula 0
                1019234, #Delay 0
                1021337, #Plain 0
                1019222, #PolyFX 0
                1019358] #MoExtrude 0

    fields = [440000277,   #Python Field 0
                440000268, #Cylinder Field 0
                440000280, #Formula Field 0
                1040449,   #Group Field 0
                440000267, #Box Field 0
                440000283, #Sound Field 0
                440000272, #Torus Field 0
                440000243, #Spherical Field 0
                440000282, #Shader Field 0
                440000274, #Capsule Field 0
                1040448,   #Radial Field 0
                440000281, #Random Field 0
                440000269, #Cone Field 0
                440000266] #Linear Field 0

    others = [5102, #Light 0
                1011196, #Cloud 1
                1011194, #Cloud Group 0
                1011146, #Physical Sky 0
                1039862, #Vector Smooth 0
                1039862, #Fog Smooth 0
                1039862, #SDF Smooth 0
                1039861, #Volume Mesher 1
                1039859, #Volume Builder 1
                1025766, #XRef 0
                1021824, #CMotion 0
                1021433, #Character 0
                1021283, #Cluster 0
                1026352, #MSkin 0
                1026224, #Muscle 0
                1019363, #Skin 0
                5136]    #Stage

    default = generators + mggenerators
    allGenerators = deformers + objects + splines + generators + mggenerators + mgeffectors + fields + others

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier

    try:
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

            # 5. ? (SHIT + CTRL)
            # 6. ? (ALT + CTRL)
            # 7. ? (ALT + SHIFT)

    except:
        pass

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()