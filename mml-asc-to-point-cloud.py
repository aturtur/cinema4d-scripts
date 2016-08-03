# MML (maanmittauslaitos) [NLS (national land survey of finland)]
# https://tiedostopalvelu.maanmittauslaitos.fi/tp/kartta?lang=fi
# elevation model - asc file to point cloud
import c4d

def main():
    
    # file location on computer
    fopen = open("C:\L4212G.asc")

    points = []
    lineNb = 0
    rowNb = 0.0
    first = fopen.readline()
    size = int(first[13:])

    for line in fopen:
        if lineNb > 6:
            ptnum = 0.0
            posz = rowNb / float(size -1) * size
            line = line[1:]

            for i in line.split(" "):
                posx = ptnum / float(size - 1) * size
                posy = float(i)
                pos = c4d.Vector(posx, posy, posz)
                c4d.StatusSetBar((lineNb/30))
                points.append(pos)
                ptnum += 1 

            rowNb += 1
        lineNb += 1
    
    poly = c4d.PolygonObject(len(points),0)
    poly.SetAllPoints(points)    
    doc.InsertObject(poly)
    c4d.StatusClear()
    fopen.close

if __name__=='__main__':
    main()