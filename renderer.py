"""The goal is to write a simple renderer which handles window creation
and plane of projection calculations."""
#pygame for window creation
import pygame as pg
import math
import vecs as vc
import objects as ob
from camera import Camera

"""Window creation"""
#Basic constants for our scene
WIDTH = 800
HEIGHT = 600
FPS = 60
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

#function which rotates around the y axis (modifying the existing x, z coordinates)
#derivation for the rotation matrix: https://en.wikipedia.org/wiki/Rotation_matrix
def rotate_xz(vertex : vc.vec3, angle):
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    x_rotated = vertex.x * cos_angle - vertex.z * sin_angle
    z_rotated = vertex.x * sin_angle + vertex.z * cos_angle
    return vc.vec3(x_rotated, vertex.y, z_rotated)

def transform(vertex : vc.vec3, dz):
    vertex.z += dz
    return vertex

cam = Camera(WIDTH, HEIGHT)
cam.position.z = 2.0

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
    cube = ob.cube(vc.vec3(-0.5, -0.5, -0.5), 1)
    COLOR = (0, 255, 0)
    vs = cube.vertices
    edges = cube.edges
    
    for edge in edges:
        #perform rotation, translation, then cast to plane of projection, then finally convert the coordinates to screen coordinates
        a = transform(rotate_xz(vs[edge[0]], angle), dz)
        b = transform(rotate_xz(vs[edge[1]], angle), dz)
        #convert a and b from world space to camera space, this needs to happen before clipping, since the near plane is in cam space
        ca = cam.world_to_camera(a)
        cb = cam.world_to_camera(b)
        #clip any lines that would render behind the near plane of the cam
        clipped = cam.clip_line_near(ca, cb)
        if clipped is None:
            continue
        point_a = cam.render(clipped[0])
        point_b = cam.render(clipped[1])
        if (point_a is None or point_b is None):
            continue
        pg.draw.line(screen, COLOR, point_a, point_b)
    #print("displaying to screen")
    pg.display.flip()
    clock.tick(FPS)
    delta_time = 1/FPS
    dz += 1 * delta_time
    #2 revolutions per second EDIT: divided by 3 to slow down rotation
    angle += 2 * math.pi * (delta_time / 3)
