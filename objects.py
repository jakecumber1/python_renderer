import vecs as vc
import math
"""Python file containing object definitions such as cubes and spheres"""


#A cube class for quickly creating an rendering cubes given a starting coordinate and length, work in progress.
#UPDATE, the cube now renders from the center NOT the the bottom left vertex of the closest face, this is to keep sanity
#when creating objects with BOTH spheres and cubes
class cube:
    def __init__(self, center : vc.vec3, side_length):
        #assuming we are starting from the center of the cube
        #the vertices will be offset from center by HALF the total side length
        h = side_length / 2

        self.vertices = [
            #Seperating by faces for readability
            vc.vec3(center.x - h, center.y - h, center.z - h),
            vc.vec3(center.x + h, center.y - h, center.z - h),
            vc.vec3(center.x + h, center.y + h, center.z - h),
            vc.vec3(center.x - h, center.y + h, center.z - h),

            vc.vec3(center.x - h, center.y - h, center.z + h),
            vc.vec3(center.x + h, center.y - h, center.z + h),
            vc.vec3(center.x + h, center.y + h, center.z + h),
            vc.vec3(center.x - h, center.y + h, center.z + h),
        ]
        #edges definition can remain the same
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)]
    #a function with scales each vertices by a specified float amount, edges remain connected
    def scale(self, ratio : float, axis = None):
        if (ratio <= 0):
            print("cannot scale by a 0 or negative amount!")
            return
        i = 0
        while i < len(self.vertices):
            if axis == None:
                self.vertices[i] = self.vertices[i] * ratio
            elif axis == "x":
                self.vertices[i].x = self.vertices[i].x * ratio
            elif axis == "y":
                self.vertices[i].y = self.vertices[i].y * ratio
            elif axis == "z":
                self.vertices[i].z = self.vertices[i].z * ratio
            else:
                print("invalid axis selected for scaling!")
                return
            i = i + 1

    def print(self):
        i = 0
        for vec in self.vertices:
            print(f"(point {i}: {vec.x}, {vec.y}, {vec.z})")
            i = i + 1
        print(self.edges)

"""How should we implement spheres?
To keep the wireframe approach we have for the cube
we should split the sphere edge into line segments, more segments, a smoother looking sphere
we'll do a latitude and longitude line to give the sphere a globe look"""

#A sphere class implementation, UNLIKE the cube which builds from the bottom left point of each face starting closer, the sphere will build from the center
class sphere:
    def __init__(self, center, radius, segments = 12, rings = 12):
        self.vertices = []
        self.edges = []
        #generate vertices of our lines
        for i in range(rings + 1):
            #0 to pi
            theta = math.pi * i / rings
            for j in range(segments):
                phi = 2 * math.pi * j / segments #0 to 2pi
                x = center.x + radius * math.sin(theta) * math.cos(phi)
                y = center.y + radius * math.cos(theta)
                z = center.z + radius * math.sin(theta) * math.sin(phi)
                self.vertices.append(vc.vec3(x, y, z))
        #edges, connect lat and long lines
        for i in range(rings + 1):
            for j in range(segments):
                idx = i * segments + j
                #connect to the next long, looping around
                next_long = i * segments + (j + 1) % segments
                self.edges.append((idx, next_long))
                #connect to next lat
                if i < rings:
                    next_lat = (i + 1) * segments + j
                    self.edges.append((idx, next_lat))

#A class meant to combine the cube and sphere classes to make a player ship
class player_ship:
    def __init__(self):
        self.shapes = []
        #ship will be made of 3 components, the left wing & right wing (which are stretched boxes) which connect to a cockpit (a sphere)
        left_wing = cube(vc.vec3(-2, 0, 1), 1)
        right_wing = cube(vc.vec3(2, 0, 1), 1)
        cockpit = sphere(vc.vec3(0, 0, 0), 1, 12, 12)
        #scale the wings on the z axis so they are stretched
        left_wing.scale(2, axis = "z")
        left_wing.scale(0.75)
        right_wing.scale(2, axis = "z")
        right_wing.scale(0.75)
        self.shapes.append(left_wing)
        self.shapes.append(right_wing)
        self.shapes.append(cockpit)


if __name__ == "__main__":
    cube1 = cube(vc.vec3(0, 0, 1), 1)
    cube1.print()
    cube1.scale(0.5)
    cube1.print()
    cube1.scale(2)
    cube1.scale(0.5, axis="x")
    cube1.print()
