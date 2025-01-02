from sympy import symbols, simplify, Derivative, factor

class Projection:
    def __init__(self):
        self.x, self.y, self.w = symbols('x y w', real=True)
        self.z = symbols('z', positive=True)
        self.x1, self.y1, self.w1 = symbols('x_1 y_1 w_1', real=True)
        self.constant = {}
        self.define_projection()
    
    def add_constant(self, symbol):
        self.constant[symbol] = symbol
        pass

    def define_projection(self):
        raise NotImplementedError

    def get_jacobian(self):
        pass

    def cov_projection(self):
        pass


class PerspectiveProjection(Projection):
    def __init__(self):
        pass

    def define_projection(self):
        pass

class EqudistantFisheyeProjection(Projection):
    def __init__(self):
        pass

    def define_projection(self):
        self.add_constant('fx')
        self.add_constant('fy')
        self.add_constant('cx')
        self.add_constant('cy')
        self.w = 1

        
        pass

class OpenCVFisheyeProjection(Projection):
    def __init__(self):
        pass

class PanoramaProjection(Projection):
    def __init__(self):
        pass

