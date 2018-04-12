import c4d
from c4d.modules import mograph as mo

def main():
    doc.StartUndo()    
    tag = op.GetLastTag()
    md = mo.GeGetMoData(op)
    cnt = md.GetCount()    
    selection = mo.GeGetMoDataSelection(tag)
    x = 0
    for i in reversed(xrange(0,cnt)):
        if selection.IsSelected(i) == True:
            t = c4d.BaseTag(1021338)
            t[c4d.ID_BASELIST_NAME] = "ms_"+str(x)
            s = c4d.BaseSelect()
            s.Select(i)
            op.InsertTag(t)
            doc.AddUndo(c4d.UNDOTYPE_NEW, t)
            mo.GeSetMoDataSelection(t, s)

            x = x + 1
            doc.AddUndo(c4d.UNDOTYPE_DELETE, tag)
    tag.Remove()
    doc.EndUndo()
    c4d.EventAdd()
    
if __name__=='__main__':
    main()