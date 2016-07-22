import c4d

def main():
    s = doc.GetSelection()
    
    for x in s:
        
        nm = x.GetNodeMaster()
        root = nm.GetRoot()    
        fn = root.GetDown()        
        fnID = fn.GetOperatorID()
        
        print fnID
    
    c4d.EventAdd()

if __name__=='__main__':
    main()