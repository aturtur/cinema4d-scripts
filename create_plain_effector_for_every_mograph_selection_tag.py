import c4d

def main():
    doc.StartUndo()
    tags = op.GetTags()
    mstag = c4d.BaseTag(1021338)
    i = 0
    for x in tags:
        if x.GetType() == 1021338:
            plain = c4d.BaseObject(1021337)
            plain[c4d.ID_MG_BASEEFFECTOR_SELECTION] = x.GetName()
            #plain[c4d.ID_BASELIST_NAME] = plain[c4d.ID_BASELIST_NAME]+"_"+str(i)
            doc.InsertObject(plain)
            effList = c4d.InExcludeData()
            if op.GetType() == 1019268:
                effList = op[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR]
                effList.InsertObject(plain,1)
                op[c4d.MGTEXTOBJECT_EFFECTORLIST_CHAR] = effList
            elif op.GetType() == 1018544 or op.GetType() == 1018791 or op.GetType() == 1018545:
                effList = op[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]
                effList.InsertObject(plain,1)
                op[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST] = effList
            elif op.GetType() == 1036557:
                effList = op[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST]
                effList.InsertObject(plain,1)
                op[c4d.ID_MG_VF_MOTIONGENERATOR_EFFECTORLIST] = effList
            i = i + 1
            doc.AddUndo(c4d.UNDOTYPE_NEW, plain)
        doc.EndUndo()
    c4d.EventAdd()
    
if __name__=='__main__':
    main()
