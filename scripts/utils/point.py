class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


# for dictionary '[x, y]' -> z, x_cart - only x step, y_cart - x and y step
class slice_of_time:
    def __init__(self):
        self.x_cart = None
        self.y_cart = None


# for array z, x_cart - only x step, y_cart - x and y step
class CARTA:
    def __init__(self):
        self.x_cart = []
        self.y_cart = []


# for showing results
class residual:
    def __init__(self):
        self.e1 = Point()
        self.e1.x = []
        self.e1.y = []
        self.e2 = Point()
        self.e2.x = []
        self.e2.y = []
        self.e3 = Point()
        self.e3.x = []
        self.e3.y = []


# to make and write to file
class FILE:
    def __init__(self, path):
        self.path = path
        f = open(path, 'w')
        f.close()

    def write2file(self, string):
        f = open(self.path, 'a')
        f.write(string)
        f.close()
