"""The goal is to write a simple renderer which handles window creation
and plane of projection calculations."""
#pygame for window creation
import pygame as pg
import math
import vecs as vc
"""
A cube class for quickly creating an rendering cubes given a starting coordinate and length, work in progress.
class cube:
    def __init__(self, start_vertex : vec3, side_length):
        self.vertices = [start_vertex, vec3(start_vertex.x + side_length, start_vertex.y, start_vertex.z),
                          vec3(start_vertex.x, start_vertex.y + side_length, start_vertex.z),
                           vec3(start_vertex.x + side_length, start_vertex.y + side_length, start_vertex.z),
                            vec3(start_vertex.x, start_vertex.y, start_vertex.z + side_length),
                             vec3(start_vertex.x + side_length, start_vertex.y, start_vertex.z + side_length),
                              vec3(start_vertex.x, start_vertex.y + side_length, start_vertex.z + side_length), 
                               vec3(start_vertex.x + side_length, start_vertex.y + side_length, start_vertex.z + side_length)]

cube1 = cube(vec3(0, 0, 1), 1)
"""


"""Window creation"""
#Basic constants for our scene
WIDTH = 800
HEIGHT = 600
FPS = 60
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

"""graphics calculations
we will be following this formula for 3d projection onto a 2d screen
for a point x, y, z
x' = x/z
y' = y/z
This assume a coordinates system which goes from -1,...,1 on the x and y axis
pygame has 0,0 as the top left of the screen, w, 0 as the top right, 0, h as the bottom left,
and finally w, h as the bottom right
we need to map our virtual space from -1,...,1 to 0,...,w/h to render to the pygame display
"""
def convert_coordinates(coor : vc.vec3):
    #adding 1 brings it to (0,...,2), dividing by 2 brings it to (0,...,1) multiplying it by width/height gives us (0,...,width/height)
    return ((coor.x + 1) / 2 * WIDTH, (1 - (coor.y + 1) / 2) * HEIGHT)
def project(vertex: vc.vec3):
    return vc.vec3(vertex.x/vertex.z, vertex.y/vertex.z, vertex.z)
#function which rotates around the y axis (modifying the existing x, z coordinates)
#derivation for the rotation matrix: https://en.wikipedia.org/wiki/Rotation_matrix
def rotate_xz(vertex : vc.vec3, angle):
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    x_rotated = vertex.x * cos_angle - vertex.z * sin_angle
    z_rotated = vertex.x * sin_angle + vertex.z * cos_angle
    return vc.vec3(x_rotated, vertex.y, z_rotated)

def transform(vertex : vc.vec3, dz):
    vertex.z += (2.0 + dz)
    return vertex


dz = 0
angle = 0
#main render loop
running = True
print("starting render loop")
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    #print("filling color")
    #fill the screen with a background color, we'll choose red
    screen.fill((255, 0, 0))
    #Now add a green cube
    #print("drawing cube")
    COLOR = (0, 255, 0)
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
    
    for edge in edges:
        #perform rotation, translation, then cast to plane of projection, then finally convert the coordinates to screen coordinates
        a = convert_coordinates(project(transform(rotate_xz(vs[edge[0]], angle), dz)))
        b = convert_coordinates(project(transform(rotate_xz(vs[edge[1]], angle), dz)))
        pg.draw.line(screen, COLOR, a, b)
    #print("displaying to screen")
    pg.display.flip()
    clock.tick(FPS)
    delta_time = 1/FPS
    dz += 1 * delta_time
    #2 revolutions per second EDIT: divided by 3 to slow down rotation
    angle += 2 * math.pi * (delta_time / 3)
