import tsapp, tsappMod, pygame
import random

display = tsappMod.Surface(width=1280,height=720,background_color=(255,0,0))

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
        [128,128],
        [-128,128]
    ],
    color=(255,255,0),
    linewidth=0,
    show_center=True,
    show_speed=True)

tl = tsapp.TextLabel("Arial.ttf", 25, 0, 25, 1280, "EMPTY")
fps_meter =tsapp.TextLabel("Arial.ttf", 25, 0, 25, 1280 ,"FPS_METER", (0,255,0))
fps_meter.align = "right"
display.framerate = 120

display.add_object(p)
display.add_object(p2)
display.add_object(tl)
display.add_object(fps_meter)

gui_update_increment = 0

while display.is_running:
    if(tsapp.is_key_down(tsapp.K_p)): exit()
    if(tsapp.is_key_down(tsapp.K_LEFT) or tsapp.is_key_down(tsapp.K_a)): p.x_speed -= 20
    if(tsapp.is_key_down(tsapp.K_RIGHT) or tsapp.is_key_down(tsapp.K_d)): p.x_speed += 20
    if(tsapp.is_key_down(tsapp.K_UP) or tsapp.is_key_down(tsapp.K_w)): p.y_speed -= 20
    if(tsapp.is_key_down(tsapp.K_DOWN) or tsapp.is_key_down(tsapp.K_s)): p.y_speed += 20
    if(gui_update_increment>=60):
        tl.text = "POS:\n.    X:" + str(int(p.center_x)) + "\n.    Y:" + str(int(p.center_y)) + "\nSPEED:\n.    X:" + str(int(p.x_speed)) + "\n.    Y:" + str(int(p.y_speed))
        fps_meter.text = "FPS: " + str(display._clock.get_fps())
        gui_update_increment=0
    p2.speed = (p.center_x - p2.center_x, p.center_y - p2.center_y)
    gui_update_increment+=1
    display.finish_frame()