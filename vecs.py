"""Vector classes and testing suite
If you see odd behavior, such as how we handle (0,0,0) for unit vector calculation
recall that the intended use case is as a vector for graphics and game engine rendering."""
#Define a vec3 class which will hold our vertex position in a 3d space
class vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    #overload the * operator
    #if other is a vec, do element wise mult, otherwise do scalar mult
    def __mul__(self, other):
        
        if isinstance(other, vec3):
            return vec3(self.x * other.x,
            self.y * other.y,
            self.z * other.z)
        elif isinstance(other, (int, float)):
            return vec3(self.x * other,
            self.y * other,
            self.z * other)
        else:
            return NotImplemented
    def __rmul__(self, other):
        return self * other
    def __add__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x + other.x,
            self.y + other.y,
            self.z + other.z)
        elif isinstance(other, (int, float)):
            return vec3(self.x + other,
            self.y + other,
            self.z + other)
        else:
            return NotImplemented
    def __sub__(self, other):
        if isinstance(other, vec3):
            return vec3(self.x - other.x,
            self.y - other.y,
            self.z - other.z)
        elif isinstance(other, (int, float)):
            return vec3(self.x - other,
            self.y - other,
            self.z - other)
        else:
            return NotImplemented
    def __truediv__(self, num):
        if not isinstance(num, (int, float)):
            return NotImplemented
        if num == 0:
            raise ZeroDivisionError
        return vec3(
            self.x/num,
            self.y/num,
            self.z/num
        )
    #can't operator overload len, because len MUST return an int, but the length of our vector can be a float.
    def length(self):
        return (self.x * self.x + self.y * self.y + self.z * self.z)**(1/2)
    def vec_add(self, vec):
        return vec3(
            self.x + vec.x,
            self.y + vec.y,
            self.z + vec.z
        )
    #dot and cross products
    def dot(self, vec):
        return (self.x * vec.x + self.y * vec.y + self.z * vec.z)
    def __matmul__(self, vec):
        return self.dot(vec)
    def cross(self, vec):
        return vec3(
            self.y * vec.z - self.z * vec.y,
            self.z * vec.x - self.x * vec.z,
            self.x * vec.y - self.y * vec.x
        )
    #unit vector calculation
    def unit_vector(self):
        length = self.length()
        #handle 0,0,0 case
        if length == 0:
            #return a zero vector
            return vec3(0,0,0)
        return self / length

class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __mul__(self, other):
    
        if isinstance(other, vec2):
            return vec2(self.x * other.x,
            self.y * other.y)
        elif isinstance(other, (int, float)):
            return vec2(self.x * other,
            self.y * other)
        else:
            return NotImplemented
    def __rmul__(self, other):
        return self * other
    def __add__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x + other.x,
            self.y + other.y)
        elif isinstance(other, (int, float)):
            return vec2(self.x + other,
            self.y + other)
        else:
            return NotImplemented
    def __sub__(self, other):
        if isinstance(other, vec2):
            return vec2(self.x - other.x,
            self.y - other.y)
        elif isinstance(other, (int, float)):
            return vec2(self.x - other,
            self.y - other)
        else:
            return NotImplemented
    def __truediv__(self, num):
        if not isinstance(num, (int, float)):
            return NotImplemented
        if num == 0:
            raise ZeroDivisionError
        return vec2(
            self.x/num,
            self.y/num
        )

    def length(self):
        return (self.x * self.x + self.y * self.y) ** (1/2)
    def unit_vector(self):
        length = self.length()
        if length == 0:
            return vec2(0, 0)
        return self / length
    

    
#vec3 testing suite
if __name__ == "__main__":
    vec1 = vec3(1, 1, 1)
    vec2 = vec3(2, 2, 2)
    print("Vec 1: ", vec1)
    print("Vec 2: ", vec2)
    print(f"Length of vec 1 {vec1.length()}")
    print(f"Length of vec 2 {vec2.length()}")
    print("Vec 1 + vec 2 ", vec1 + vec2)
    print("Vec 1 + 4 ", vec1 + 4)
    print("Vec 1 - vec 2 ", vec1 - vec2)
    print("Vec 1 - 4 ", vec1 - 4)
    print("Vec 1 element wise mult vec 2 ", vec1 * vec2)
    print("Vec 1 element wise mult 4 ", vec1 * 4)
    print("4 mult vec1 ", 4 * vec1)
    print("Vec 2 divided by 2 (should be 1,1,1) ", vec2 / 2)
    print(f"Dot product of vec 1 & 2 {vec1 @ vec2}")
    print("Cross product of vec 1 & vec 2 ", vec1.cross(vec2))
    print(f"Vec 2 as a unit vector ", vec2.unit_vector())