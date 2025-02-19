import tsapp, tsappMod, pygame
import random

display = tsappMod.Surface(width=3840 ,height=1600,background_color=(0,0,0))

p = tsappMod.PolygonalObject(
    points=[
        [-128,-128],
        [128,-128],
        [128,128],
        [-128,128]
    ],
    color=(255,0,255),
    linewidth=0,
    show_center=True,
    show_speed=True)

p2 = tsappMod.PolygonalObject(
    points=[
        [-128,-128],
        [128,-128],
        [0,128],
    ],
    color=(128,0,128),
    linewidth=0,
    show_center=True,
    show_speed=True)

text_bg = tsappMod.PolygonalObject(
    points=[
        [0,0],
        [display.width,0],
        [display.width,30],
        [0,30]
    ],
    color=(255,255,255),
    linewidth=0,
    show_center=True,
    show_speed=True)

tl = tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "EMPTY")
fps_meter =tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width ,"FPS_METER", (0,0,0))
fps_meter.align = "right"
display.framerate = 30

display.add_object(text_bg)
display.add_object(tl)
display.add_object(fps_meter)
display.add_object(p)
display.add_object(p2)

gui_update_increment = 0

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
    p2.speed = (p.center_x*1.25 - p2.center_x, p.center_y*1.25 - p2.center_y)
    gui_update_increment+=1
    display.finish_frame()