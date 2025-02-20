"""
    MADE BY ZEPHYROS1938 (zephyros@zephyros1938.org)
    FREE TO USE, WITH CREDIT.
"""
import math

import pygame

import tsapp

# Keys
try:
    if(not pygame.get_init()): pygame.init()
except:
    print("Could not get pygame initialization state.")

_active_window = None
_active_Camera2D = None

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
        global _active_window
        _active_window = self
        tsapp._active_window = self
        try:
            pygame.display.set_caption(title)
        except:
            print("Could not set display name.")
    
    def finish_frame(self):
        """
        Intended to be called once a frame while GraphicsWindow.is_running
        Performs all the most common end-of-frame actions, including:
         - tracking time
         - updating the position and image of graphical objects
         - removing destroyed objects
         - flipping the screen
         - checking for the "QUIT" event
        """

        # Track timing
        self._clock.tick(self.framerate)

        # Draw frame
        self._surface.fill(self.background_color)
        for drawable_item in self._draw_list:
            if not drawable_item.destroyed:
                drawable_item._draw()
            else:
                self._draw_list.remove(drawable_item)
                drawable_item.destroy()
                continue
            drawable_item._update(self._clock.get_time())
                
        pygame.display.flip()

        # Capture events from the current frame
        global _current_frame_event_list
        _current_frame_event_list = pygame.event.get()

        # Check for QUIT
        if any(event.type == pygame.QUIT for event in _current_frame_event_list):
            self.is_running = False
    
    def seconds_passed(self, seconds):
        return self.deltatime * seconds
    
    
    @property
    def deltatime(self):
        return self._clock.get_time() / 1000
    @property
    def aspect_ratio(self):
        return (self.width / self.height)

def _get_window():
    return _active_window

class Camera2D:
    def __init__(self,origin_x = 0, origin_y = 0):
        self.origin_x = origin_x
        self.origin_y = origin_y
        global _active_Camera2D
        _active_Camera2D = self

    @property
    def origin(self):
        return (self.origin_x, self.origin_y)
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
    
    def __init__(self, points=[[0,0],[1,0],[0,1]], center=[0,0], color=(255,255,255), linewidth=0, show_center=False, show_speed=False, show_direction = False, attraction_radius = 200, show_attraction = False):
        super().__init__()
        if not (isinstance(points, list) and all(isinstance(item, list) for item in points)):   # checks if the 'points' variable is a list, 
                                                                                                # and that it contains only tuples
            raise TypeError("Points must be a list of 2x length lists.")
        self.points = [v for v in points]
        self.local_center_x = sum(v[0] for v in self.points) / len(points)
        self.local_center_y = sum(v[1] for v in self.points) / len(points)
        self.color = color
        self.color_inverse = (255-color[0], 255-color[1], 255-color[2])
        self.linewidth = linewidth
        self.center_x = center[0]
        self.center_y = center[1]
        self.show_center = show_center
        self.show_speed = show_speed
        self.show_direction = show_direction
        self.show_attraction = show_attraction
        self.attraction_radius = attraction_radius
        self._world_coord_list = [(0,0)] * len(points)
        self._update_world_coords()
    
    def _draw(self):
        surface = _active_window._surface
        if(self.visible):
            pygame.draw.polygon(surface, self.color, self._world_coord_list, self.linewidth)
        if(self.show_center):
            pygame.draw.circle(surface, self.color_inverse, self.world_center, 4)
        if(self.show_speed):
            pygame.draw.line(surface=surface, color=(255,255,0), start_pos=self.world_center, end_pos=(self.world_center[0] + self.x_speed,self.world_center[1] + self.y_speed), width=2)
        if(self.show_direction):
            pygame.draw.line(
                surface=surface,
                color=(0,255,255),
                start_pos=self.world_center,
                end_pos=Math.rotate_point_rad((self.world_center[0]-250, self.world_center[1]), self.world_center, self.current_angle_rad),
                width=2
            )
            pygame.draw.line(
                surface=surface,
                color=(0,255,0),
                start_pos=self.world_center,
                end_pos=Math.rotate_point_rad((self.world_center[0]-250, self.world_center[1]), self.world_center, self.right),
                width=2
            )
        if(self.show_attraction):
            pygame.draw.circle(surface=surface, color=(255,255,255), center=self.world_center, radius=self.attraction_radius, width=2)
        

    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.center_x += (x_speed / 1000) * delta_time
        self.center_y += (y_speed / 1000) * delta_time
        self._update_world_coords()
    
    def _update_world_coords(self):
        for i in range(len(self.points)):
            self._world_coord_list[i] = (self.points[i][0] + self.world_center[0] - self.local_center_x, self.points[i][1] + self.world_center[1] - self.local_center_y)
        #print(self.world_coord_list)
    
    def rotate_rad(self, radians):
        for i in range(len(self.points)):
            self.points[i] = Math.rotate_point_rad_compact(self.points[i], self.local_center, radians - self.current_angle_rad)
        self.current_angle_rad = radians
    
    def rotate_to(self, target):
        self.rotate_rad(Math.get_direction_towards_point(target, self.world_center))
    
    def move_towards(self, target, speed):
        target_direction = Math.get_direction_towards_point(target, self.world_center)
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
    def world_center(self):
        #return self.center
        return (self.center[0] - _active_Camera2D.origin_x, self.center[1] - _active_Camera2D.origin_y)
    @property
    def local_center(self):
        return(self.local_center_x, self.local_center_y)
    @property
    def right(self):
        return self.current_angle_rad + Math.half_pi

class TextLabel(tsapp.TextLabel):
    def __init__(self, font_name, font_size, x, y, width, text="", color=tsapp.BLACK, static=True):
        super().__init__(font_name, font_size, x, y, width, text, color)
        self.static = static
    
    def _draw(self):
        if not self.visible or not self.text or not self._lines:
            return
        surface = _active_window._surface
        if(not self.static):
            start_x, y = (self.x -_active_Camera2D.origin_x, self.y -_active_Camera2D.origin_y)
        else:
            start_x, y = (self.x, self.y)
        draw_bounds = self.show_bounds
        bounds_color = self.bounds_color
        for line in self._lines:
            line_width = self._font.get_rect(line).width
            if self.align == "left":
                x = start_x
            elif self.align == "right":
                x = start_x + self.width - line_width
            elif self.align == "center":
                x = start_x + (self.width - line_width) * 0.5
            else:
                raise AssertionError(
                    'Text Label alignment must be "left", "right", or "center": got "'  # noqa: E501
                    + self.align
                    + '"'
                )
            self._font.render_to(surface, (x, y), line)
            if self.show_bounds:
                pygame.draw.line(surface, bounds_color, (self.x, y), (self.x + self.width, y), width=1)
            y += self._pixel_line_height

        if draw_bounds:
            pygame.draw.rect(surface, bounds_color, self.rect, width=2)
    
    @property
    def rect(self):
        # NOTE: pygame.Rect does not support non-integer values for position
        if(not self.static):
            return pygame.Rect(int(self.x), int(self.y - self._font.get_sized_ascender()), int(self.width), int(self.height))
        return pygame.Rect(int(self.x -_active_Camera2D.origin_x), int(self.y - self._font.get_sized_ascender() -_active_Camera2D.origin_y), int(self.width), int(self.height))

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
    def rotate_point_rad_compact(p, a, r):
        cos_r = math.cos(r)
        sin_r = math.sin(r)
        dx = p[0] - a[0]
        dy = p[1] - a[1]
        
        return (
            dx * cos_r - dy * sin_r + a[0],
            dx * sin_r + dy * cos_r + a[1]
        )

    @staticmethod
    def vector_from_rad(radians):
        return math.cos(radians), math.sin(radians)
    
    @staticmethod
    def magnitude(p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    
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