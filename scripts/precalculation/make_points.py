from scripts.utils import point


class POINTS:

#input file - .msh
    def __init__(self, name = '../square.msh'):
        f = open(name)
        self.points = []
        self.dots = []
        logic = False
        for line in f:
            if line.split()[0] == '$Nodes':
                logic = True
               #print('start')
            if line.split()[0] == '$EndNodes':
               #print('finish')
                break
            cur = len(line.split())
            if cur == 3 and logic:
                tmp = [float(a) for a in line.split()[:2]]
                self.dots.append(point.Point(tmp[0], tmp[1]))
                self.points.append(tmp)
        f.close()
