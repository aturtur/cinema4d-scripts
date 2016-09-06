import c4d
from c4d import gui

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():
    hexcolor = c4d.gui.InputDialog("HEX-color")
    c4d.CallCommand(13015, 13015)
    rgb = hex_to_rgb(hexcolor)
    mat = doc.GetActiveMaterial()
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(rgb[0]/255,rgb[1]/255,rgb[2]/255)
    mat.Update(True, True)
     
if __name__=='__main__':
    main()
