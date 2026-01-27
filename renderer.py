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
CAM_POSITION = vc.vec3(0, 0, 0)
CAM_SPEED = 2.0
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
 

cam = Camera(WIDTH, HEIGHT, CAM_POSITION)

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
    #cube = ob.cube(vc.vec3(-0.5, -0.5, -0.5), 1)
    #cube.scale(2, axis="x")
    COLOR = (0, 255, 0)
    #vs = cube.vertices
    #edges = cube.edges

    #sphere = ob.sphere(vc.vec3(0, 0, 0), 1, segments = 12, rings = 12)
    #vs = sphere.vertices
    #edges = sphere.edges
    """

    EXAMPLE RENDER LOOP
    
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
    """
    player_ship = ob.player_ship()
    for shape in player_ship.shapes:
        vs = shape.vertices
        for edge in shape.edges:
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
    #dz += 1 * delta_time
    #2 revolutions per second EDIT: divided by 3 to slow down rotation
    angle += 2 * math.pi * (delta_time / 3)
    #Check input and handle camera movement
    #Get pressed returns a key, bool dict we can index w/ pg.key_name
    #if true a key that key is being pressed
    #determine where to move the cam based on what keys are currently pressed down
    keys = pg.key.get_pressed()
    dx = dy = dz = 0
    
    if keys[pg.K_w]: dz += CAM_SPEED * delta_time # Remember to flip signs on Z since we are moving the world AROUND the camera
    if keys[pg.K_s]: dz -= CAM_SPEED * delta_time
    if keys[pg.K_a]: dx -= CAM_SPEED * delta_time
    if keys[pg.K_d]: dx += CAM_SPEED * delta_time
    if keys[pg.K_q]: dy += CAM_SPEED * delta_time  # up
    if keys[pg.K_e]: dy -= CAM_SPEED * delta_time  # down
    if keys[pg.K_ESCAPE]: running = False # End program if user presses escape, update later to bring up a quit menu
    cam.move(dx, dy, dz)
