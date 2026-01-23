import vecs as vc
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
        i = 0
        while i < len(self.vertices):
            self.vertices[i] = self.vertices[i] * 0.5
            i = i + 1

    def print(self):
        i = 0
        for vec in self.vertices:
            print(f"(point {i}: {vec.x}, {vec.y}, {vec.z})")
            i = i + 1
        print(self.edges)


cube1 = cube(vc.vec3(0, 0, 1), 1)
cube1.print()
cube1.scale(0.5)
cube1.print()
