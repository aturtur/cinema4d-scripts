# rename selected materials from n to n(selected items)
import c4d

def main():
    n = 1
    s = doc.GetActiveMaterials()
    for x in s:
        x.SetName(n)
        n=n+1

if __name__=='__main__':
    main()
