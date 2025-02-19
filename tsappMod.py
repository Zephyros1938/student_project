"""
    MADE BY ZEPHYROS1938 (zephyros@zephyros1938.org)
    FREE TO USE, WITH CREDIT.
"""
import tsapp
import pygame

# Keys

if(pygame.get_init()==False): pygame.init()

K_TAB = pygame.K_TAB
K_ESCAPE = pygame.K_ESCAPE
K_BACKSPACE = pygame.K_BACKSPACE
K_DELETE = pygame.K_DELETE
K_INSERT = pygame.K_INSERT
K_HOME = pygame.K_HOME
K_END = pygame.K_END
K_PAGEUP = pygame.K_PAGEUP
K_PAGEDOWN = pygame.K_PAGEDOWN
K_CAPSLOCK = pygame.K_CAPSLOCK
K_PRINT = pygame.K_PRINT
K_PAUSE = pygame.K_PAUSE
K_SCROLLLOCK = pygame.K_SCROLLLOCK

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

K_LSHIFT = pygame.K_LSHIFT
K_RSHIFT = pygame.K_RSHIFT
K_LCTRL = pygame.K_LCTRL
K_RCTRL = pygame.K_RCTRL
K_LALT = pygame.K_LALT
K_RALT = pygame.K_RALT
K_LMETA = pygame.K_LMETA
K_RMETA = pygame.K_RMETA

K_KP0 = pygame.K_KP0
K_KP1 = pygame.K_KP1
K_KP2 = pygame.K_KP2
K_KP3 = pygame.K_KP3
K_KP4 = pygame.K_KP4
K_KP5 = pygame.K_KP5
K_KP6 = pygame.K_KP6
K_KP7 = pygame.K_KP7
K_KP8 = pygame.K_KP8
K_KP9 = pygame.K_KP9
K_KP_PLUS = pygame.K_KP_PLUS
K_KP_MINUS = pygame.K_KP_MINUS
K_KP_MULTIPLY = pygame.K_KP_MULTIPLY
K_KP_DIVIDE = pygame.K_KP_DIVIDE
K_KP_ENTER = pygame.K_KP_ENTER
K_KP_PERIOD = pygame.K_KP_PERIOD

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
    def __init__(self, width=1018, height=573, background_color=tsapp.WHITE):
        super().__init__(width, height, background_color) 
    
    def finish_frame(self):
        super().finish_frame()

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
    world_coord_list = []
    
    def __init__(self, points=[[0,0],[1,0],[0,1]], center=[0,0], color=(255,255,255), linewidth=0, show_center=False, show_speed=False):
        super().__init__()
        self.points = points
        temp_center_x = 0
        temp_center_y = 0
        for point in points:
            temp_center_x += point[0]
            temp_center_y += point[1]
        self.width_offset = temp_center_x / len(points)
        self.height_offset = temp_center_y / len(points)
        self.color = color
        self.linewidth = linewidth
        self.center_x = center[0]
        self.center_y = center[1]
        self.show_center = show_center
        self.show_speed = show_speed
    
    def _draw(self):
        surface = tsapp._get_window()._surface
        if(self.visible):
            self.world_coord_list = []
            for i in self.points:
                self.world_coord_list.append((i[0] + (self.center_x), i[1] + (self.center_y)))
            pygame.draw.polygon(surface, self.color, self.world_coord_list, self.linewidth)
        if(self.show_center):
            pygame.draw.circle(surface, (0,255,0), (self.center_x, self.center_y), 2)
        if(self.show_speed):
            pygame.draw.line(surface=surface, color=(255,255,0), start_pos=(self.center_x,self.center_y), end_pos=(self.center_x + self.x_speed,self.center_y + self.y_speed), width=2)
        
    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.center_x += (x_speed / 1000) * delta_time
        self.center_y += (y_speed / 1000) * delta_time
    
    def is_colliding_polygon(self, other_polygon):
        pass