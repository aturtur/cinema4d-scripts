import c4d

def main():
    bd = doc.GetActiveBaseDraw()
    if bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] == 0:
        bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 0.8
    else:
        bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 0
    c4d.EventAdd()
    
if __name__=='__main__':
    main()