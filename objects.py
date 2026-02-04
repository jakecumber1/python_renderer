import vecs as vc
import math
"""Python file containing object definitions such as cubes and spheres"""

#a parent class for universal shape functions (scale, translation, rotation, printing)
class Object():
    def __init__(self):
        self.vertices = []
        self.edges = []
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
    #bounding definition for collision
    def get_bounds(self):
        xs = []
        ys = []
        zs = []
        for v in self.vertices:
            xs.append(v.x)
            ys.append(v.y)
            zs.append(v.z)
        return (
            min(xs), max(xs),
            min(ys), max(ys),
            min(zs), max(zs)
        )





#A cube class for quickly creating an rendering cubes given a starting coordinate and length, work in progress.
#UPDATE, the cube now renders from the center NOT the the bottom left vertex of the closest face, this is to keep sanity
#when creating objects with BOTH spheres and cubes
class Cube(Object):
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

"""How should we implement spheres?
To keep the wireframe approach we have for the cube
we should split the sphere edge into line segments, more segments, a smoother looking sphere
we'll do a latitude and longitude line to give the sphere a globe look"""

#A sphere class implementation. Builds from the center, currently creates multiple redundant points on the poles of the sphere
class Sphere(Object):
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
class Playership:
    def __init__(self):
        self.shapes = []
        #ship will be made of 3 components, the left wing & right wing (which are stretched boxes) which connect to a cockpit (a sphere)
        left_wing = Cube(vc.vec3(-2, 0, 1), 1)
        right_wing = Cube(vc.vec3(2, 0, 1), 1)
        cockpit = Sphere(vc.vec3(0, 0, 0), 1, 12, 12)
        #scale the wings on the z axis so they are stretched
        left_wing.scale(2, axis = "z")
        left_wing.scale(0.75)
        right_wing.scale(2, axis = "z")
        right_wing.scale(0.75)
        self.shapes.append(left_wing)
        self.shapes.append(right_wing)
        self.shapes.append(cockpit)
    def print(self):
        i = 0
        for shape in self.shapes:
            print(f"Shape {i}:")
            shape.print()
            i = i + 1

#Laser class for player projectiles
class Laser:
    def __init__(self, start : vc.vec2, target : vc.vec2, speed=2000, color = (0, 255, 255), thickness = 2, length = 60):
        self.start = start
        self.target = target
        self.color = color
        self.thickness = thickness
        self.speed = speed
        
        #compute direction from start to target
        self.direction = (target - start).unit_vector()
        self.head = start
        self.tail = start - self.direction * length

        #total length from start to target
        self.total_length = (target - start).length()
        self.traveled = 0 #distance traveled, for deleting the line later

        self.finished = False
    def update(self, delta_time):
        #animate the laser moving towards the target
        if self.finished:
            return

        movement = self.direction * self.speed * delta_time

        # Move both head and tail forward
        self.head = self.head + movement
        self.tail = self.tail + movement

        # Kill laser when head reaches target
        if (self.head - self.target).length() <= self.speed * delta_time:
            self.finished = True
    def is_finished(self):
        #return true if the target point is reached
        return self.finished

"""Collision section """
#We're checking collision after the object has been converted to 2d screen coordinates
def laser_hits_object(laser, vertices_2d, obj_edges):
    p1 = laser.tail
    p2 = laser.head
    for i, j in obj_edges:
        q1 = vertices_2d[i]
        q2 = vertices_2d[j]
        if vc.lines_intersect(p1, p2, q1, q2):
            return True
    return False
    


if __name__ == "__main__":
    cube1 = Cube(vc.vec3(0, 0, 1), 1)
    cube1.print()
    cube1.scale(0.5)
    cube1.print()
    cube1.scale(2)
    cube1.scale(0.5, axis="x")
    cube1.print()
    sphere = Sphere(vc.vec3(0, 0, 0), 1, 12, 12)
    sphere.print()
    sphere.scale(2)
    sphere.print()
    player = Playership()
    player.print()