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
pg.mouse.set_visible(False)

#Load audio files
asteroid_explosion = pg.mixer.Sound("sounds/asteroid_explosion.wav")
canon_sound = pg.mixer.Sound("sounds/canon_sound.wav")
hit_sound = pg.mixer.Sound("sounds/hit_sound.wav")


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
 
#Camera definition
cam = Camera(WIDTH, HEIGHT, CAM_POSITION)

#Crosshair class definition
class Crosshair:
    def __init__(self, width, height, rgb, dot_rad, gap, line_len, thick):
        self.width = width
        self.height = height
        self.crosshair_x = width // 2
        self.crosshair_y = height // 2
        self.color = rgb
        self.dot_radius = dot_rad
        self.gap = gap
        self.line_length = line_len
        self.thickness = thick

crosshair = Crosshair(WIDTH, HEIGHT, (0, 0, 255), 1, 4, 8, 1)

#function for handling moving the cross hair across the screen
def on_mouse_move(crosshair, mouse_x, mouse_y):
    crosshair.crosshair_x = mouse_x
    crosshair.crosshair_y = mouse_y

LASER_COOLDOWN = 0.5
time_since_last_shot = 0.0
def on_mouse_left_click(crosshair, lasers):

    global time_since_last_shot

    if time_since_last_shot > LASER_COOLDOWN:
        time_since_last_shot = 0.0
        mouse_pos = vc.vec2(crosshair.crosshair_x, crosshair.crosshair_y)
        left_edge = vc.vec2(0, HEIGHT // 2)
        right_edge = vc.vec2(WIDTH, HEIGHT // 2)
        lasers.append(ob.Laser(left_edge, mouse_pos, speed = 2000))
        lasers.append(ob.Laser(right_edge, mouse_pos, speed = 2000))
        canon_sound.play()
        

def draw_crosshair(crosshair, screen):
    cx = int(crosshair.crosshair_x)
    cy = int(crosshair.crosshair_y)
    gap = crosshair.gap
    length = crosshair.line_length
    thick = crosshair.thickness
    
    #draw lines around the dot first
    #Left line
    pg.draw.line(screen, crosshair.color, (cx - gap - length, cy), (cx - gap, cy), thick)
    #right
    pg.draw.line(screen, crosshair.color, (cx + gap, cy), (cx + gap + length, cy), thick)
    #above
    pg.draw.line(screen, crosshair.color, (cx, cy - gap - length), (cx, cy - gap), thick)
    #below
    pg.draw.line(screen, crosshair.color, (cx, cy + gap), (cx, cy + gap + length), thick)

    #draw center dot
    if (crosshair.dot_radius != 0):
        pg.draw.circle(screen, crosshair.color, (cx, cy), crosshair.dot_radius)
    
def laser_draw(laser, screen):
    pg.draw.line(screen, laser.color, (laser.tail.x, laser.tail.y), (laser.head.x, laser.head.y), laser.thickness)

def handle_hit(laser, obj):
    hit_sound.play()

#Function for handling object drawing
def draw_object(obj, cam):
        vs = obj.vertices
        for edge in obj.edges:
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
            pg.draw.line(screen, COLOR, point_a.to_tuple(), point_b.to_tuple())


lasers = []
dz = 0
angle = 0
objects = [ob.Cube(vc.vec3(0, 0, 0), 4), ob.Sphere(vc.vec3(0, 4, 5), 2), ob.Cube(vc.vec3(0, -3, 2), 3)]
#main render loop
running = True
print("starting render loop")
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEMOTION:
            mouse_x = max(0, min(event.pos[0], WIDTH))
            mouse_y = max(0, min(event.pos[1], HEIGHT))
            on_mouse_move(crosshair, mouse_x, mouse_y)


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
    for obj in objects:
        draw_object(obj, cam)
    draw_crosshair(crosshair, screen)

    #Laser drawing
    #since we might remove [:] gives us a copy of the list
    for laser in lasers[:]:
        laser.update(delta_time)
        for obj in objects:
            if ob.laser_hits_object(laser, cam.project_object(obj), obj.edges):
                handle_hit(laser, obj)
                objects.remove(obj)
                lasers.remove(laser)
        if laser in lasers:
            laser_draw(laser, screen)
        if laser.is_finished():
            lasers.remove(laser)
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
    time_since_last_shot += delta_time
    keys = pg.key.get_pressed()
    dx = dy = dz = 0



    if keys[pg.K_w]: dz += CAM_SPEED * delta_time # Remember to flip signs on Z since we are moving the world AROUND the camera
    if keys[pg.K_s]: dz -= CAM_SPEED * delta_time
    if keys[pg.K_a]: dx -= CAM_SPEED * delta_time
    if keys[pg.K_d]: dx += CAM_SPEED * delta_time
    if keys[pg.K_q]: dy += CAM_SPEED * delta_time  # up
    if keys[pg.K_e]: dy -= CAM_SPEED * delta_time  # down
    if keys[pg.K_ESCAPE]: running = False # End program if user presses escape, update later to bring up a quit menu
    
    #handle clicking
    mouse_pressed = pg.mouse.get_pressed()
    if mouse_pressed[0]:
        on_mouse_left_click(crosshair, lasers)

    cam.move(dx, dy, dz)
