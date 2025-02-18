import tsapp, tsappMod
import random

#tsapp.GraphicsWindow.finish_frame = exec("print(\"test\")");

display = tsapp.GraphicsWindow(width=1280,height=720,background_color=(255,0,0))

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

tl = tsapp.TextLabel("Arial.ttf", 25, 0, 25, 1280, "EMPTY")

display.add_object(p)
display.add_object(tl)

while display.is_running:
    if(tsapp.is_key_down(tsapp.K_p)): exit()
    if(tsapp.is_key_down(tsapp.K_LEFT) or tsapp.is_key_down(tsapp.K_a)): p.x_speed -= 20
    if(tsapp.is_key_down(tsapp.K_RIGHT) or tsapp.is_key_down(tsapp.K_d)): p.x_speed += 20
    if(tsapp.is_key_down(tsapp.K_UP) or tsapp.is_key_down(tsapp.K_w)): p.y_speed -= 20
    if(tsapp.is_key_down(tsapp.K_DOWN) or tsapp.is_key_down(tsapp.K_s)): p.y_speed += 20
    tl.text = "POS:\n.    X:" + str(int(p.center_x)) + "\n.    Y:" + str(int(p.center_y)) + "\nSPEED:\n.    X:" + str(int(p.x_speed)) + "\n.    Y:" + str(int(p.y_speed))

    display.finish_frame()