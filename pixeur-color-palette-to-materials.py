import c4d
from c4d import storage as s

def main():
    doc.StartUndo()
    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select pixeur palette',c4d.FILESELECT_LOAD,'')
    f = open(fn.decode("utf-8"))
    
    for line in f:
        if line.startswith("R"):
            line = line.split(" ")
            r = line[0][2:]
            g = line[1][2:]
            line = line[2].split(",")
            b = line[0][2:]
            mat = c4d.BaseMaterial(c4d.Mmaterial)
            color = c4d.Vector(float(r)/255,float(g)/255,float(b)/255)
            mat[c4d.MATERIAL_COLOR_COLOR] = color
            mat.Message(c4d.MSG_UPDATE)
            mat.Update(True, True)
            doc.InsertMaterial(mat)
            doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
                    
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()