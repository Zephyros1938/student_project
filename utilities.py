import random, pygame, tsapp

class PolygonalObject(tsapp.GraphicalObject):
    points : list[(int,int)]
    color : (int, int, int)
    linewidth : int
    center_x: int
    center_y: int
    width_offset: int
    height_offset: int
    show_center = False

    def __init__(self, points: list[(int,int)], center = [0,0], color = (255,255,255), linewidth = 0, show_center = False):
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
    
    def _draw(self):
        surface = tsapp._get_window()._surface
        temp_coord_list = []
        for i in self.points:
            temp_coord_list.append((i[0] + (self.center_x - self.width_offset), i[1] + (self.center_y - self.height_offset)))
        if(self.visible):
            pygame.draw.polygon(surface, self.color, temp_coord_list, self.linewidth)
        if(self.show_center):
            pygame.draw.circle(surface=surface, color=(0,255,0), center=(self.center_x, self.center_y), radius=2)
        
    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.center_x += (x_speed / 1000) * delta_time
        self.center_y += (y_speed / 1000) * delta_time