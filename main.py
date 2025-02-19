import tsapp, tsappMod, pygame, math
import random

display = tsappMod.Surface(width=1280 ,height=720,background_color=(0,0,0))

l=32
l2 = l / 2

p = tsappMod.PolygonalObject(
    points=[
        [l2,-l2],
        [l2,l2],
        [-((l*(math.sqrt(3)/2))-l2),0]
    ],
    color=(255,0,255),
    linewidth=0,
    show_center=True,
    show_speed=True,
    show_direction=True)

p2 = tsappMod.PolygonalObject(
    points=[
        [-l2,-l2],
        [l2,-l2],
        [l2,l2],
        [-l2,l2]
    ],
    color=(128,0,128),
    linewidth=0,
    show_center=True,
    show_speed=True,
    show_direction=True)

tl = tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "EMPTY", (255, 255, 255))
fps_meter =tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width ,"FPS_METER", (255, 255, 255))
fps_meter.align = "right"
display.framerate = -1

display.add_object(tl)
display.add_object(fps_meter)
display.add_object(p)
display.add_object(p2)

gui_update_increment = 0
box_move_step = 0

move_speed = 200
enemy_move_speed = 200

while display.is_running:
    delta_time = display._clock.get_time() / 1000
    print(delta_time)
    mouse_pos = tsapp.get_mouse_position()
    if(tsapp.is_key_down(tsappMod.K_ESCAPE)): exit()
    if(tsapp.is_key_down(tsapp.K_LEFT) or tsapp.is_key_down(tsapp.K_a)): p.x_speed -= (move_speed * delta_time)
    if(tsapp.is_key_down(tsapp.K_RIGHT) or tsapp.is_key_down(tsapp.K_d)): p.x_speed += (move_speed * delta_time)
    if(tsapp.is_key_down(tsapp.K_UP) or tsapp.is_key_down(tsapp.K_w)): p.y_speed -= (move_speed * delta_time)
    if(tsapp.is_key_down(tsapp.K_DOWN) or tsapp.is_key_down(tsapp.K_s)): p.y_speed += (move_speed * delta_time)
    if(p.center_x>=display.width+20): p.center_x=0
    if(p.center_x<=-20): p.center_x = display.width
    if(p.center_y<=-20): p.center_y = display.height
    if(p.center_y>=display.height+20): p.center_y = 0
    if(tsapp.is_mouse_down()):
        p.rotate_to(mouse_pos)
        p.move_towards(mouse_pos, move_speed * delta_time)

    if(gui_update_increment>=display.framerate):
        tl.text = "X :" + str(int(p.center_x)) + " Y :" + str(int(p.center_y))
        fps_meter.text = "FPS: " + str(display._clock.get_fps())
        gui_update_increment=0
    if(box_move_step>=display.framerate):
        box_move_step=0
        p2.speed = (((p.center_x - p2.center_x)) * delta_time, ((p.center_y - p2.center_y)) * delta_time)
    p2.rotate_to(p.center)

    gui_update_increment+=1
    box_move_step+=1
    display.finish_frame()