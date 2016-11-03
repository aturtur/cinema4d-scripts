import c4d
from c4d import storage as s
import os

def main():
    doc.StartUndo()
    folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select image folder',c4d.FILESELECT_DIRECTORY,'')
    if not folder: return
    files = os.listdir(folder)

    for f in files:
        mat = c4d.BaseMaterial(c4d.Mmaterial)
        mat[c4d.MATERIAL_USE_REFLECTION] = 0
        mat[c4d.MATERIAL_USE_ALPHA] = 1      
        shd = c4d.BaseShader(c4d.Xbitmap)
        shd[c4d.BITMAPSHADER_FILENAME] = folder+"\\"+f
        alpha = c4d.BaseShader(c4d.Xbitmap)
        alpha[c4d.BITMAPSHADER_FILENAME] = folder+"\\"+f
        mat[c4d.MATERIAL_COLOR_SHADER] = shd
        mat[c4d.MATERIAL_ALPHA_SHADER] = alpha
        mat.InsertShader(shd)
        mat.InsertShader(alpha)        
        mat.Message(c4d.MSG_UPDATE)
        mat.Update(True, True)        
        doc.InsertMaterial(mat)
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
        
        c4d.EventAdd()
        doc.EndUndo()

if __name__=='__main__':
    main()