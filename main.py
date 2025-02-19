import tsapp, tsappMod, pygame, math
import random

display = tsappMod.Surface(width=1280 ,height=720,background_color=(0,0,0))

l=256

p = tsappMod.PolygonalObject(
    points=[
        [0-l/2,0-l/2],
        [l/2,0-l/2],
        [0,(l*(math.sqrt(3)/2))-l/2]
    ],
    color=(255,0,255),
    linewidth=0,
    show_center=True,
    show_speed=True,
    show_direction=True)

p2 = tsappMod.PolygonalObject(
    points=[
        [-128,-128],
        [128,-128],
        [128,128],
        [-128,128]
    ],
    color=(128,0,128),
    linewidth=0,
    show_center=True,
    show_speed=True,
    show_direction=True)

tl = tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "EMPTY", (255, 255, 255))
fps_meter =tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width ,"FPS_METER", (255, 255, 255))
fps_meter.align = "right"
display.framerate = 60

display.add_object(tl)
display.add_object(fps_meter)
display.add_object(p)
display.add_object(p2)

gui_update_increment = 0
box_move_step = 0

while display.is_running:
    if(tsapp.is_key_down(tsappMod.K_ESCAPE)): exit()
    if(tsapp.is_key_down(tsapp.K_LEFT) or tsapp.is_key_down(tsapp.K_a)): p.x_speed -= 20
    if(tsapp.is_key_down(tsapp.K_RIGHT) or tsapp.is_key_down(tsapp.K_d)): p.x_speed += 20
    if(tsapp.is_key_down(tsapp.K_UP) or tsapp.is_key_down(tsapp.K_w)): p.y_speed -= 20
    if(tsapp.is_key_down(tsapp.K_DOWN) or tsapp.is_key_down(tsapp.K_s)): p.y_speed += 20
    if(p.center_x>=display.width+20): p.center_x=0
    if(p.center_x<=-20): p.center_x = display.width
    if(p.center_y<=-20): p.center_y = display.height
    if(p.center_y>=display.height+20): p.center_y = 0

    if(gui_update_increment>=display.framerate):
        tl.text = "X :" + str(int(p.center_x)) + " Y :" + str(int(p.center_y))
        fps_meter.text = "FPS: " + str(display._clock.get_fps())
        gui_update_increment=0
    if(box_move_step>=display.framerate):
        box_move_step=0
        p2.speed = ((p.center_x - p2.center_x), (p.center_y - p2.center_y))
    p2.rotate_to(p.center)
    p.rotate_to(tsapp.get_mouse_position())

    gui_update_increment+=1
    box_move_step+=1
    display.finish_frame()