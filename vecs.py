"""Object Definition"""
#Define a vec3 class which will hold our vertex position in a 3d space
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    #overload the * operator, given a single number multiply each entry by that number
    def __mul__(self, num):
        self.x = self.x * num
        self.y = self.y * num
        self.z = self.z * num
        #DO NOT FORGET TO RETURN SELF!!!!
        return self