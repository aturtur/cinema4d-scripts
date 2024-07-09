# Iterate hierarchy
def GetNext(op):
    if op == None: return None
    if op.GetDown(): return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectHierarchy(op):
    array = []
    if op is None:
        return
    while op:
        array.append(op)
        op = GetNext(op)
    return array