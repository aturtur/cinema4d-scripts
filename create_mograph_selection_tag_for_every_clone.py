import c4d
from c4d import gui
from c4d.modules import mograph as mo

def main():
    doc.StartUndo()
    obj = doc.GetSelection()
    if obj:
        md = mo.GeGetMoData(obj[0])
        cnt = md.GetCount()
        for i in reversed(xrange(0, cnt)):
            tag = c4d.BaseTag(1021338)
            tag[c4d.ID_BASELIST_NAME] = "ms_"+str(i)
            s = c4d.BaseSelect()
            obj[0].InsertTag(tag)
            doc.AddUndo(c4d.UNDOTYPE_NEW, tag)
            s.Select(i)
            mo.GeSetMoDataSelection(tag, s)
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()