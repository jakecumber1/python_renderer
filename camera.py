"""TODO: a camera which we can manipulate to view the cube"""
import vecs as vc
import math
class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        #camera's starting position is 0,0,0
        self.position = vc.vec3(0, 0, 0)
        #near plane to stop rendering to prevent weird rendering behavior
        self.near = 0.1
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

    #move the world AROUND the camera
    def world_to_camera (self, vec : vc.vec3):
        return (vec - self.position)
    def project(self, vertex: vc.vec3):
        if vertex.z <= self.near:
            return None #behind camera or too close to render
        return vc.vec3(vertex.x/vertex.z, vertex.y/vertex.z, vertex.z)
    def convert_coordinates(self, coor : vc.vec3):
        #adding 1 brings it to (0,...,2), dividing by 2 brings it to (0,...,1) multiplying it by width/height gives us (0,...,width/height)
        return ((coor.x + 1) / 2 * self.width, (1 - (coor.y + 1) / 2) * self.height)
    
    #Clip any lines behind the near plane to the plane instead of trying to render behind the camera
    def clip_line_near(self, a, b):
        za = a.z
        zb = b.z
        #both behind
        if (za < self.near and zb < self.near):
            return None
        
        #both in front, no need to clip
        if (za >= self.near and zb >= self.near):
            return a, b
        
        #avoid divide by 0
        if za == zb:
            return None
        
        #calculate intersection with near plane, use interpolation!
        t = (self.near - za) / (zb - za)
        ix = a.x + t * (b.x - a.x)
        iy = a.y + t * (b.y - a.y)
        i = vc.vec3(ix, iy, self.near)
        #return the clipped line, ordering depending on which side is behind the cam
        if za < self.near:
            return i, b
        else:
            return a, i

    def render(self, vec : vc.vec3):
        v = self.world_to_camera(vec)
        v = self.project(v)
        if v is None:
            return None
        return self.convert_coordinates(v)