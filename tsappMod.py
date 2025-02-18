import tsapp;
import pygame;
import utilities;

class GraphicsWindow(tsapp.GraphicsWindow):
    def __init__(self, width=1018, height=573, background_color=tsapp.WHITE):
        super().__init__(width=width, height=height,background_color=background_color)
    
    def add_polygonal_object(self, drawable_polygon: utilities.PolygonalObject):
        self._draw_list.append(drawable_polygon)

    # def finish_frame(self):
    #     """
    #     Intended to be called once a frame while GraphicsWindow.is_running
    #     Performs all the most common end-of-frame actions, including:
    #      - tracking time
    #      - updating the position and image of graphical objects
    #      - removing destroyed objects
    #      - flipping the screen
    #      - checking for the "QUIT" event
    #     """

    #     # Track timing
    #     self._clock.tick(self.framerate)

    #     # Draw frame
    #     destroyed_items = []
    #     self._surface.fill(self.background_color)
    #     for drawable_item in self._draw_list:
    #         if not drawable_item.destroyed:
    #             drawable_item._draw()
    #         drawable_item._update(self._clock.get_time())

    #         if drawable_item.destroyed:
    #             destroyed_items.append(drawable_item)
    #     pygame.display.flip()

    #     # Remove destroyed elements
    #     for drawable_item in destroyed_items:
    #         self._draw_list.remove(drawable_item)

    #     # Capture events from the current frame
    #     global _current_frame_event_list
    #     _current_frame_event_list = pygame.event.get()

    #     # Check for QUIT
    #     for event in _current_frame_event_list:
    #         if event.type == pygame.QUIT:
    #             self.is_running = False
