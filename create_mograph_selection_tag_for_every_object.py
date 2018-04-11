import c4d
from c4d import gui
from c4d.modules import mograph as mo

def main():
    obj = doc.GetSelection()
    if obj:
        md = mo.GeGetMoData(obj[0])
        cnt = md.GetCount()
        for i in reversed(xrange(0, cnt)):
            tag = c4d.BaseTag(1021338)
            tag[c4d.ID_BASELIST_NAME] = "ms_"+str(i)
            s = c4d.BaseSelect()
            obj[0].InsertTag(tag)
            s.Select(i)
            mo.GeSetMoDataSelection(tag, s)    
    c4d.EventAdd()

if __name__=='__main__':
    main()