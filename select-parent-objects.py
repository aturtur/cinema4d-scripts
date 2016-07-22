import c4d

def main():
    s = doc.GetSelection()    
    for x in s:                
        p = x.GetUp()
        x.DelBit(c4d.BIT_ACTIVE)
        p.SetBit(c4d.BIT_ACTIVE)
    c4d.EventAdd()
    
if __name__=='__main__':
    main()