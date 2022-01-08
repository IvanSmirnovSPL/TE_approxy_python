class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z


class slice_of_time:

    def __init__(self):
        pass

    def update(self, j, d):
        if j == 0:
            self.x_cart = d
        else:
            self.y_cart = d


class z_cart:

    def __init__(self, SoT, ic):
        self.x = ic.make_z(SoT.x_cart)
        self.y = ic.make_z(SoT.y_cart)


class CARTA:

    def __init__(self):
        self.x_cart = []
        self.y_cart = []
