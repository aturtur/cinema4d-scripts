import c4d
doc.StartUndo()
def main():
    if not doc.GetSelection(): return None
    obj = doc.GetSelection()[0]
    textSpline = c4d.BaseObject(5178)
    moText = c4d.BaseObject(1019268)
    array = [textSpline, moText]
    if obj.GetType() == 5178 or obj.GetType() == 1019268:
        for x in array:
            x[c4d.PRIM_TEXT_TEXT] = obj[c4d.PRIM_TEXT_TEXT]
            x[c4d.PRIM_TEXT_TEXT] = obj[c4d.PRIM_TEXT_TEXT]
            if obj[c4d.PRIM_TEXT_FONT] == None:
                pass
            else:
                x[c4d.PRIM_TEXT_FONT] = obj[c4d.PRIM_TEXT_FONT]
            x[c4d.PRIM_TEXT_ALIGN] = obj[c4d.PRIM_TEXT_ALIGN]
            x[c4d.PRIM_TEXT_HEIGHT] = obj[c4d.PRIM_TEXT_HEIGHT]
            x[c4d.PRIM_TEXT_HSPACING] = obj[c4d.PRIM_TEXT_HSPACING]
            x[c4d.PRIM_TEXT_VSPACING] = obj[c4d.PRIM_TEXT_VSPACING]
            x[c4d.SPLINEOBJECT_INTERPOLATION] = obj[c4d.SPLINEOBJECT_INTERPOLATION]
            x[c4d.SPLINEOBJECT_SUB] = obj[c4d.SPLINEOBJECT_SUB]
            x[c4d.SPLINEOBJECT_ANGLE] = obj[c4d.SPLINEOBJECT_ANGLE]
            x[c4d.SPLINEOBJECT_MAXIMUMLENGTH] = obj[c4d.SPLINEOBJECT_MAXIMUMLENGTH]
    if obj.GetType() == 5178:
        doc.AddUndo(c4d.UNDOTYPE_NEW, moText)
        doc.InsertObject(moText)
    elif obj.GetType() == 1019268:
        doc.AddUndo(c4d.UNDOTYPE_NEW, textSpline)
        doc.InsertObject(textSpline)
    c4d.EventAdd()
if __name__=='__main__':
    main()