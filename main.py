import tsapp, tsappMod, math
from tsappMod import Builtins as TSMConst

display = tsappMod.Surface(width=1080 ,height=1080,background_color=(0,0,0))

q = 32

l=q * (display.width / display.height)
l2 = l / 2

p = tsappMod.PolygonalObject(
    points=[
        [l2,-l2],
        [-((l*(math.sqrt(3)/10))-l2),0],
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
    show_direction=True,
    center=[display.width,display.height])

p2.center_x = display.width / 2
p2.center_y = display.height / 2

tl = tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "EMPTY", (255, 255, 255))
fps_meter =tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width ,"FPS_METER", (255, 255, 255))
fps_meter.align = "right"
display.framerate = -1

display.add_object(tl)
display.add_object(fps_meter)
display.add_object(p2)
display.add_object(p)

gui_update_tick = 0
deceleration_tick = 0

move_speed = 200
moving = False
enemy_move_speed = 200

while display.is_running:
    deltatime = display.deltatime
    mouse_pos = tsapp.get_mouse_position()

    if(tsapp.is_key_down(TSMConst.Special.K_ESCAPE)): exit()
    if(p.center_x>display.width): p.center_x=0
    if(p.center_x<0): p.center_x = display.width
    if(p.center_y<0): p.center_y = display.height
    if(p.center_y>display.height): p.center_y = 0

    if(p2.center_x>display.width+20): p2.center_x=0
    if(p2.center_x<-20): p2.center_x = display.width
    if(p2.center_y<-20): p2.center_y = display.height
    if(p2.center_y>display.height+20): p2.center_y = 0
    
    if(tsapp.is_key_down(tsapp.K_w)): p.move_forward(move_speed * deltatime)
    if(tsapp.is_key_down(tsapp.K_s)): p.move_backward(move_speed * deltatime)
    if(tsapp.is_key_down(tsapp.K_a)): p.move_left(move_speed * deltatime)
    if(tsapp.is_key_down(tsapp.K_d)): p.move_right(move_speed * deltatime)
    if(tsappMod.is_mouse_down(TSMConst.Mouse.M_RIGHT)): p.rotate_to(mouse_pos)

    if(gui_update_tick>=display.seconds_passed(seconds=1)):
        tl.text = "X :" + str(int(p.center_x)) + " Y :" + str(int(p.center_y)) + " D :" + str(tsappMod.Math.magnitude(p.center, p2.center))
        fps_meter.text = "FPS: " + str(display._clock.get_fps())
        gui_update_tick=0
    if(deceleration_tick>=display.seconds_passed(600)):
        if(
            not (
                tsapp.is_key_down(tsapp.K_w) or
                tsapp.is_key_down(tsapp.K_s) or
                tsapp.is_key_down(tsapp.K_a) or
                tsapp.is_key_down(tsapp.K_d)
            ) and p.speed != (0,0)):
            p.x_speed *= 0.75
            p.y_speed *= 0.75
            if(tsapp.is_key_down(tsapp.K_e)):
                p.x_speed *= 0.8
                p.y_speed *= 0.8
            if(abs(p.x_speed)<=1 and abs(p.y_speed)<=1):
                p.x_speed = 0
                p.y_speed = 0
        if(p2.speed!=(0,0)):
            p2.x_speed *= 0.75
            p2.y_speed *= 0.75
            if(abs(p2.x_speed)<=1 and abs(p2.y_speed)<=1):
                p2.x_speed = 0
                p2.y_speed = 0
        deceleration_tick=0
    if(tsappMod.Math.magnitude(p2.center, p.center)<500):
        p2.rotate_to(p.center)
        p2.move_forward(enemy_move_speed * deltatime)

    gui_update_tick+=1 * deltatime
    deceleration_tick+=1 * deltatime
    display.finish_frame()