import c4d, os
from c4d import storage as s

def main():
    doc.StartUndo()
    folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select image folder',c4d.FILESELECT_DIRECTORY,'')
    if not folder: return
    files = os.listdir(folder)

    for f in files:
        mat = c4d.BaseMaterial(c4d.Mmaterial)
        path = folder+"\\"+f
        
        # enable or disable channels
        mat[c4d.MATERIAL_USE_REFLECTION] = 0
        mat[c4d.MATERIAL_USE_LUMINANCE] = 1
        mat[c4d.MATERIAL_USE_ALPHA] = 1

        # color channel
        color = c4d.BaseShader(c4d.Xbitmap)
        color[c4d.BITMAPSHADER_FILENAME] = path
        mat[c4d.MATERIAL_COLOR_SHADER] = color

        # luminance channel
        luminance = c4d.BaseShader(c4d.Xbitmap)
        luminance[c4d.BITMAPSHADER_FILENAME] = path
        mat[c4d.MATERIAL_LUMINANCE_SHADER] = luminance

        # alpha channel
        alpha = c4d.BaseShader(c4d.Xbitmap)
        alpha[c4d.BITMAPSHADER_FILENAME] = path
        mat[c4d.MATERIAL_ALPHA_SHADER] = alpha
        
        # assign shaders to material
        mat.InsertShader(color)
        mat.InsertShader(luminance)
        mat.InsertShader(alpha)
        
        # other stuff
        mat.Message(c4d.MSG_UPDATE)
        mat.Update(True, True)
        matname = f.split(".")[0]
        mat.SetName(matname)
        doc.InsertMaterial(mat)
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
        
        c4d.EventAdd()
        doc.EndUndo()

if __name__=='__main__':
    main()