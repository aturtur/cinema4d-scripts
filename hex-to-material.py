import c4d
from c4d import gui

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def main():
    doc.StartUndo()
    hexcolor = c4d.gui.InputDialog("HEX-color")
    rgb = hex_to_rgb(hexcolor)
    color = c4d.Vector(float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255)
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat[c4d.MATERIAL_COLOR_COLOR] = color
    mat.Message(c4d.MSG_UPDATE)
    mat.Update(True, True)
    mat.SetName(str(hexcolor))
    doc.InsertMaterial(mat)
    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)

    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()