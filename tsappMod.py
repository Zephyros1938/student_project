
import tsapp;
import pygame;

class PolygonalObject(tsapp.GraphicalObject):
    def __init__(self, points = [[0,0],[1,0],[0,1]], center = [0,0], color = (255,255,255), linewidth = 0, show_center = False, show_speed = False):
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
            temp_coord_list = []
            for i in self.points:
                temp_coord_list.append((i[0] + (self.center_x), i[1] + (self.center_y)))
            pygame.draw.polygon(surface, self.color, temp_coord_list, self.linewidth)
        if(self.show_center):
            pygame.draw.circle(surface, (0,255,0), (self.center_x, self.center_y), 2)
        if(self.show_speed):
            pygame.draw.line(surface=surface, color=(255,255,0), start_pos=(self.center_x,self.center_y), end_pos=(self.center_x + self.x_speed,self.center_y + self.y_speed), width=2)
        
    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.center_x += (x_speed / 1000) * delta_time
        self.center_y += (y_speed / 1000) * delta_time