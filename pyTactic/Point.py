#Нахождение координат точки B, которая повернулась на угол angle, относительно
#точки A на радиусе r:
#xB = xA + r * Cos(angle)
#yB = yA + r * Sin(angle)
import numbers
import math

class Point(tuple):
    def __init__(self, point=tuple()):
        self.point = [point[0],  point[1]]

    @staticmethod
    def prd_vect(u,  v):
        return u.x*v.y - u.y*v.x;

    @staticmethod
    def angle(u, v):
        return (-1 if Point.prd_vect(u,v)<0 else 1)* math.acos(u*v / (u.length()*v.length()))

    @staticmethod
    def get_rotated(point, angle, radius):
        x = point.x +  radius * math.cos(angle)
        y = point.y +  radius * math.sin(angle)      
        return Point((x,y))
    
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def normalize(self):
        return self / self.length()

    def __truediv__(self, other):
        if other == 0:
            return Point((0,0))
        if isinstance(other, numbers.Number): 
            return Point((self.x / other,self.y / other))

    def __mul__(self, value):
        if value == 0:
            return Point((0,0))
        if isinstance(value, numbers.Number): 
            return Point((self.x * value,self.y * value))
        if isinstance(value, Point): # scalarproduct
            return self.x*value.x + self.y*value.y

    def __add__(self, v2): 
        return Point((self[0] + v2[0], v2[1] + self[1]))

    def __sub__(self, v2):
        return Point((self[0] - v2[0], self[1] - v2[1]))

    def dist(self,  v2):
        return ((self[0] - v2[0]) ** 2 + (self[1] - v2[1]) ** 2) ** 0.5


    def __getitem__(self, key):
       return self.point[key]
    def __setitem__(self, key, value):
       self.point[key] = value


    def get_x(self):           
        return self.point[0]
    def set_x(self, value):         
        self.point[0] = value
    def del_x(self):            
        pass
    x = property(get_x, set_x, del_x, 'x')

    def get_y(self):          
        return self.point[1]
    def set_y(self, value):     
        self.point[1] = value
    def del_y(self):            
        pass
    y = property(get_y, set_y, del_y, 'y')

