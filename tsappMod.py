"""
    MADE BY ZEPHYROS1938 (zephyros@zephyros1938.org)
    FREE TO USE, WITH CREDIT.
"""
import tsapp
import pygame
import math

# Keys
try:
    if(pygame.get_init()==False): pygame.init()
except:
    print("Could not get pygame initialization state.")

# Tsapp Overrides

class Surface(tsapp.GraphicsWindow):
    """
    A class to represent a graphical window surface; Modifies Tsapp's GraphicsWindow.

    Attributes:
    width : int
        The width of the window.
    height : int
        The height of the window.
    background_color : tuple
        The background color of the window.
    """
    def __init__(self, width=1018, height=573, background_color=tsapp.WHITE, title="tsapp window"):
        super().__init__(width, height, background_color)
        try:
            pygame.display.set_caption(title)
        except:
            print("Could not set display name.")
    
    def finish_frame(self):
        super().finish_frame()
    
    def seconds_passed(self, seconds):
        return self.deltatime * seconds
    
    @property
    def deltatime(self):
        return self._clock.get_time() / 1000

# Missing Tsapp Objects

class PolygonalObject(tsapp.GraphicalObject):
    """
    A class to represent a polygonal graphical object.

    Attributes:
    points : list
        List of points defining the polygon.
    center : list
        The center coordinates of the polygon.
    color : tuple
        The color of the polygon.
        (R,G,B)
    linewidth : int
        The width of the polygon lines.
    show_center : bool
        Flag to show the center of the polygon.
    show_speed : bool
        Flag to show the speed vector of the polygon.
    """
    _world_coord_list = []
    current_angle_rad = 0
    
    def __init__(self, points=[[0,0],[1,0],[0,1]], center=[0,0], color=(255,255,255), linewidth=0, show_center=False, show_speed=False, show_direction = False):
        super().__init__()
        if not (isinstance(points, list) and all(isinstance(item, list) for item in points)):   # checks if the 'points' variable is a list, 
                                                                                                # and that it contains only tuples
            raise TypeError("Points must be a list of 2x length lists.")
        self.points = [v for v in points]
        #print(len(points))
        self.local_center_x = sum(v[0] for v in self.points) / len(points)
        self.local_center_y = sum(v[1] for v in self.points) / len(points)
        #self.local_center = (self.local_center_x, self.local_center_y)
        self.color = color
        self.color_inverse = (255-color[0], 255-color[1], 255-color[2])
        self.linewidth = linewidth
        self.center_x = center[0]
        self.center_y = center[1]
        self.show_center = show_center
        self.show_speed = show_speed
        self.show_direction = show_direction
        self._world_coord_list = [(0,0)] * len(points)
        self._update_world_coords()
    
    def _draw(self):
        surface = tsapp._get_window()._surface
        if(self.visible):
            pygame.draw.polygon(surface, self.color, self._world_coord_list, self.linewidth)
        if(self.show_center):
            pygame.draw.circle(surface, self.color_inverse, (self.center_x, self.center_y), 4)
        if(self.show_speed):
            pygame.draw.line(surface=surface, color=(255,255,0), start_pos=(self.center_x,self.center_y), end_pos=(self.center_x + self.x_speed,self.center_y + self.y_speed), width=2)
        if(self.show_direction):
            pygame.draw.line(
                surface=surface,
                color=(0,255,255),
                start_pos=self.center,
                end_pos=Math.rotate_point_rad((self.center_x-250, self.center_y), self.center, self.current_angle_rad),
                width=2
            )
            pygame.draw.line(
                surface=surface,
                color=(0,255,0),
                start_pos=self.center,
                end_pos=Math.rotate_point_rad((self.center_x-250, self.center_y), self.center, self.right),
                width=2
            )
        

    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.center_x += (x_speed / 1000) * delta_time
        self.center_y += (y_speed / 1000) * delta_time
        self._update_world_coords()
    
    def _update_world_coords(self):
        for i in range(len(self.points)):
            self._world_coord_list[i] = (self.points[i][0] + self.center_x - self.local_center_x, self.points[i][1] + self.center_y - self.local_center_y)
        #print(self.world_coord_list)
    
    def rotate_rad(self, radians):
        for i in range(len(self.points)):
            self.points[i] = Math.rotate_point_rad_compact(self.points[i], self.local_center, radians - self.current_angle_rad)
        self.current_angle_rad = radians
    
    def rotate_to(self, target):
        self.rotate_rad(Math.get_direction_towards_point(target, self.center))
    
    def move_towards(self, target, speed):
        target_direction = Math.get_direction_towards_point(target, self.center)
        sx, sy = Math.vector_from_rad(target_direction)
        self.x_speed -= sx * speed
        self.y_speed -= sy * speed
    
    def move_forward(self, speed):
        sx, sy = Math.vector_from_rad(self.current_angle_rad)
        self.x_speed -= sx * speed
        self.y_speed -= sy * speed
    
    def move_backward(self, speed):
        sx, sy = Math.vector_from_rad(self.current_angle_rad)
        self.x_speed += sx * speed
        self.y_speed += sy * speed
    
    def move_right(self, speed):
        sx, sy = Math.vector_from_rad(self.right)
        self.x_speed -= sx * speed
        self.y_speed -= sy * speed
    
    def move_left(self, speed):
        sx, sy = Math.vector_from_rad(self.right)
        self.x_speed += sx * speed
        self.y_speed += sy * speed

    
    @property
    def is_colliding_polygon(self, other_polygon):
        pass
    @property
    def center(self):
        return (self.center_x, self.center_y)
    @property
    def local_center(self):
        return(self.local_center_x, self.local_center_y)
    @property
    def right(self):
        return self.current_angle_rad + Math.half_pi

class Math:
    @staticmethod
    def get_direction_towards_point(current,target):
        return math.atan2(target[1] - current[1], target[0] - current[0])
    @staticmethod
    def rotate_point_rad(p1, pivot, radians):
        s = math.sin(radians)
        c = math.cos(radians)
        p = p1
        p = (p[0] - pivot[0], p[1] - pivot[1])
        xnew = p[0] * c - p[1] * s
        ynew = p[0] * s + p[1] * c
        return (xnew + pivot[0], ynew + pivot[1])
    @staticmethod
    def rotate_point_rad_compact(p,a,r):
        return (
            (
                (p[0]-a[0])
                *math.cos(r)
                -(p[1]-a[1])
                *math.sin(r)
            ) + a[0],
            (
                (p[0]-a[0])
                *math.sin(r)
                +(p[1]-a[1])
                *math.cos(r)
            ) + a[1]
            )
    @staticmethod
    def vector_from_rad(radians):
        return (math.cos(radians), math.sin(radians))
    
    @staticmethod
    def magnitude(p1,p2):
        return math.sqrt(
            (
                (p2[0]-p1[0])
                **2
            ) + 
            (
                (p2[1]-p1[1])
                **2
            )
        )
    
    half_pi = math.pi/2

def is_mouse_down(mouse_button):
    return pygame.mouse.get_pressed()[mouse_button]

class Builtins:
    """
        List of all missing key and mouse constants from tsapp.
    """
    class Special:
        """
            Contains all special keys. 
        """
        
        K_TAB = pygame.K_TAB
        K_ESCAPE = pygame.K_ESCAPE
        K_BACKSPACE = pygame.K_BACKSPACE
        K_CAPSLOCK = pygame.K_CAPSLOCK

    class Function:
        """
            Contains all function keys.
        """
        K_F1 = pygame.K_F1
        K_F2 = pygame.K_F2
        K_F3 = pygame.K_F3
        K_F4 = pygame.K_F4
        K_F5 = pygame.K_F5
        K_F6 = pygame.K_F6
        K_F7 = pygame.K_F7
        K_F8 = pygame.K_F8
        K_F9 = pygame.K_F9
        K_F10 = pygame.K_F10
        K_F11 = pygame.K_F11
        K_F12 = pygame.K_F12

    class Command:
        """
            Contains all command keys.
        """
        K_LSHIFT = pygame.K_LSHIFT
        K_RSHIFT = pygame.K_RSHIFT
        K_LCTRL = pygame.K_LCTRL
        K_RCTRL = pygame.K_RCTRL
        K_LALT = pygame.K_LALT
        K_RALT = pygame.K_RALT
        K_LMETA = pygame.K_LMETA
        K_RMETA = pygame.K_RMETA

    class Symbols:
        """
            Contains all symbol keys.
        """
        K_MINUS = pygame.K_MINUS
        K_EQUALS = pygame.K_EQUALS
        K_LEFTBRACKET = pygame.K_LEFTBRACKET
        K_RIGHTBRACKET = pygame.K_RIGHTBRACKET
        K_BACKSLASH = pygame.K_BACKSLASH
        K_SEMICOLON = pygame.K_SEMICOLON
        K_QUOTE = pygame.K_QUOTE
        K_COMMA = pygame.K_COMMA
        K_PERIOD = pygame.K_PERIOD
        K_SLASH = pygame.K_SLASH
        K_BACKQUOTE = pygame.K_BACKQUOTE

    class Mouse:
        """
            Contains all mouse buttons.
        """
        M_LEFT = 0
        M_MIDDLE = 1
        M_RIGHT = 2
        WHEEL_UP = 3
        WHEEL_DOWN = 4