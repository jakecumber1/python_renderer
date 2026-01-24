import vecs as vc
import math
"""Python file containing object definitions such as cubes and spheres"""

"""
NoTE! This template is drawn with the top left point of each face first, our cube
definition below starts with the bottom left point of each face
example cube definition with a side length of 1
    vs = [
        vc.vec3(0.5, 0.5, 0.5),
        vc.vec3(-0.5, 0.5, 0.5),
        vc.vec3(-0.5, -0.5, 0.5),
        vc.vec3(0.5, -0.5, 0.5),
        vc.vec3(0.5, 0.5, -0.5),
        vc.vec3(-0.5, 0.5, -0.5),
        vc.vec3(-0.5, -0.5, -0.5),
        vc.vec3(0.5, -0.5, -0.5)
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)]
"""


#A cube class for quickly creating an rendering cubes given a starting coordinate and length, work in progress.
class cube:
    def __init__(self, start_vertex : vc.vec3, side_length):
        self.vertices = [start_vertex, vc.vec3(start_vertex.x + side_length, start_vertex.y, start_vertex.z),
                          vc.vec3(start_vertex.x + side_length, start_vertex.y + side_length, start_vertex.z),
                           vc.vec3(start_vertex.x, start_vertex.y + side_length, start_vertex.z),
                            vc.vec3(start_vertex.x, start_vertex.y, start_vertex.z + side_length),
                             vc.vec3(start_vertex.x + side_length, start_vertex.y, start_vertex.z + side_length),
                              vc.vec3(start_vertex.x + side_length, start_vertex.y + side_length, start_vertex.z + side_length), 
                               vc.vec3(start_vertex.x, start_vertex.y + side_length, start_vertex.z + side_length)]
        self.edges = edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                        (4, 5), (5, 6), (6, 7), (7, 4),
                        (0, 4), (1, 5), (2, 6), (3, 7)]
    #a function with scales each vertices by a specified float amount, edges remain connected
    def scale(self, ratio : float):
        if (ratio <= 0):
            print("cannot scale by a 0 or negative amount!")
            return
        i = 0
        while i < len(self.vertices):
            self.vertices[i] = self.vertices[i] * ratio
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
if __name__ == "__main__":
    cube1 = cube(vc.vec3(0, 0, 1), 1)
    cube1.print()
    cube1.scale(0.5)
    cube1.print()
