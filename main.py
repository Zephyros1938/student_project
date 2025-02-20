import tsapp, tsappMod, math

display = tsappMod.Surface(width=1080 ,height=1080,background_color=(0,0,0))

q = 32

l=q * (display.width / display.height)
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
    show_direction=True,
    center=[display.width,display.height])

tl = tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "EMPTY", (255, 255, 255))
fps_meter =tsapp.TextLabel("CourierNew.ttf", 25, 0, 25, display.width ,"FPS_METER", (255, 255, 255))
fps_meter.align = "right"
display.framerate = -1

display.add_object(tl)
display.add_object(fps_meter)
display.add_object(p2)
display.add_object(p)

gui_update_increment = 0
box_move_step = 0

move_speed = 200
enemy_move_speed = 200

while display.is_running:
    delta_time = display._clock.get_time() / 1000
    #print(delta_time)
    mouse_pos = tsapp.get_mouse_position()
    if(tsapp.is_key_down(tsappMod.K_ESCAPE)): exit()
    if(p.center_x>=display.width+20): p.center_x=0
    if(p.center_x<=-20): p.center_x = display.width
    if(p.center_y<=-20): p.center_y = display.height
    if(p.center_y>=display.height+20): p.center_y = 0
    if(tsappMod.is_mouse_down(tsappMod.M_LEFT)):
        p.move_towards(mouse_pos, move_speed * delta_time)
    if(tsappMod.is_mouse_down(tsappMod.M_LEFT) or tsappMod.is_mouse_down(tsappMod.M_RIGHT)):
        p.rotate_to(mouse_pos)

    if(gui_update_increment>=600*delta_time):
        tl.text = "X :" + str(int(p.center_x)) + " Y :" + str(int(p.center_y))
        fps_meter.text = "FPS: " + str(display._clock.get_fps())
        gui_update_increment=0
    if(box_move_step>=600*delta_time and not tsapp.is_mouse_down() and p.speed != (0,0)):
        p.x_speed *= 0.75
        p.y_speed *= 0.75
        if(abs(p.x_speed)<=1 and abs(p.y_speed)<=1):
            p.x_speed = 0
            p.y_speed = 0
        print(p.speed)
        box_move_step=0
    p2.move_towards(p.center, enemy_move_speed * delta_time)
    p2.rotate_to(p.center)

    gui_update_increment+=1 * delta_time
    box_move_step+=1 * delta_time
    display.finish_frame()