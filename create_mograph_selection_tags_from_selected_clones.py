import c4d
from c4d.modules import mograph as mo

def main():
    doc.StartUndo()    
    tag = op.GetLastTag()
    tags = op.GetTags()
    md = mo.GeGetMoData(op)
    cnt = md.GetCount()    
    selection = mo.GeGetMoDataSelection(tag)
    prefix = "ms"
    sep = "_"
    x = 0    
    for k in reversed(tags):
        if k.GetName().split("_")[0] == prefix:
            x = x+1
    for i in reversed(xrange(0,cnt)):
        if selection.IsSelected(i) == True:
            t = c4d.BaseTag(1021338)
            t[c4d.ID_BASELIST_NAME] = prefix+sep+str(x)
            s = c4d.BaseSelect()
            s.Select(i)
            op.InsertTag(t)
            doc.AddUndo(c4d.UNDOTYPE_NEW, t)
            mo.GeSetMoDataSelection(t, s)
            x = x + 1            
    tag.Remove()
    doc.AddUndo(c4d.UNDOTYPE_DELETE, tag)
    doc.EndUndo()
    c4d.EventAdd()    
if __name__=='__main__':
    main()