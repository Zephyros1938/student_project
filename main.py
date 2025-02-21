import tsapp, tsappMod, math
from tsappMod import Builtins as TSMConst

display = tsappMod.Surface(width=3840, height=1600, background_color=(0, 0, 0))
camera = tsappMod.Camera2D(0, 0)

q = 32
l = q * display.aspect_ratio
l2 = l / 2

p = tsappMod.PolygonalObject(
    points=[
        [l2, -l2],
        [-((l * (math.sqrt(3) / 10)) - l2), 0],
        [l2, l2],
        [-((l * (math.sqrt(3) / 2)) - l2), 0]
    ],
    color=(255, 0, 255),
    linewidth=0,
    show_center=False,
    show_speed=True,
    show_direction=True,
)

p2 = tsappMod.PolygonalObject(
    points=[
        [-l2, -l2],
        [l2, -l2],
        [l2, l2],
        [-l2, l2]
    ],
    color=(128, 0, 128),
    linewidth=0,
    show_center=False,
    show_speed=True,
    show_direction=True,
    center=[display.width, display.height],
    attraction_radius=1000 * display.aspect_ratio,
    show_attraction=True
)

# Set initial centers
p2.center_x = display.width / 2
p2.center_y = display.height / 2
p.center_x = display.width / 2
p.center_y = display.width / 4

tl = tsappMod.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "EMPTY", (255, 255, 255), True)
fps_meter = tsappMod.TextLabel("CourierNew.ttf", 25, 0, 25, display.width, "FPS_METER", (255, 255, 255))
fps_meter.align = "right"
display.framerate = -1

display.add_object(tl)
display.add_object(fps_meter)
display.add_object(p2)
display.add_object(p)

GUI_UPDATE_TICK = 0
DECELERATION_TICK = 0

P_MOVE_SPEED = 200
P2_MOVE_SPEED = 200

while display.is_running:
    dt = display.deltatime  # cache delta time
    mouse_pos = tsapp.get_mouse_position()

    if tsapp.is_key_down(TSMConst.Special.K_ESCAPE):
        exit()

    # Cache movement delta value
    move_delta = P_MOVE_SPEED * dt

    # Cache movement key states
    move_keys = (
        tsapp.is_key_down(tsapp.K_w),
        tsapp.is_key_down(tsapp.K_s),
        tsapp.is_key_down(tsapp.K_a),
        tsapp.is_key_down(tsapp.K_d)
    )
    
    if move_keys[0]:
        p.move_forward(move_delta)
    if move_keys[1]:
        p.move_backward(move_delta)
    if move_keys[2]:
        p.move_left(move_delta)
    if move_keys[3]:
        p.move_right(move_delta)
    
    if tsappMod.is_mouse_down(TSMConst.Mouse.M_RIGHT):
        p.rotate_to(mouse_pos)

    # Update camera via key input
    if tsapp.is_key_down(tsapp.K_UP):
        camera.origin_y -= move_delta
    if tsapp.is_key_down(tsapp.K_DOWN):
        camera.origin_y += move_delta
    if tsapp.is_key_down(tsapp.K_LEFT):
        camera.origin_x -= move_delta
    if tsapp.is_key_down(tsapp.K_RIGHT):
        camera.origin_x += move_delta

    # Pre-calculate camera boundaries based on display dimensions
    half_height = display.height * 0.5
    quarter_height = display.height * 0.25
    half_width = display.width * 0.5
    quarter_width = display.width * 0.25

    # Adjust camera based on player position and speed
    if p.center[1] - half_height + quarter_height < camera.origin_y:
        camera.origin_y -= abs(p.y_speed) * dt
    if p.center[1] - half_height - quarter_height > camera.origin_y:
        camera.origin_y += abs(p.y_speed) * dt
    if p.center[0] - half_width + quarter_width < camera.origin_x:
        camera.origin_x -= abs(p.x_speed) * dt
    if p.center[0] - half_width - quarter_width > camera.origin_x:
        camera.origin_x += abs(p.x_speed) * dt

    # GUI update every 60 seconds (adjust threshold as needed)
    if GUI_UPDATE_TICK >= display.seconds_passed(seconds=60):
        tl.text = f"X: {int(p.center_x)} Y: {int(p.center_y)} C: {(p.current_angle_rad / tsappMod.Math.tau) * 360}"
        fps_meter.text = f"FPS: {display._clock.get_fps()}"
        GUI_UPDATE_TICK = 0

    # Deceleration logic every 60 seconds
    if DECELERATION_TICK >= display.seconds_passed(60):
        # Decelerate p if no movement keys are pressed
        if not any(move_keys) and p.speed != (0, 0):
            p.x_speed *= 0.75
            p.y_speed *= 0.75
            if tsapp.is_key_down(tsapp.K_e):
                p.x_speed *= 0.8
                p.y_speed *= 0.8
            if abs(p.x_speed) <= 1 and abs(p.y_speed) <= 1:
                p.x_speed, p.y_speed = 0, 0

        # Decelerate p2 if outside its attraction radius
        if p2.speed != (0, 0) and tsappMod.Math.magnitude(p2.world_center, p.world_center) >= p2.attraction_radius:
            p2.x_speed *= 0.75
            p2.y_speed *= 0.75
            if abs(p2.x_speed) <= 1 and abs(p2.y_speed) <= 1:
                p2.x_speed, p2.y_speed = 0, 0

        DECELERATION_TICK = 0

    # p2 moves toward p if within attraction radius
    if tsappMod.Math.magnitude(p2.world_center, p.world_center) < p2.attraction_radius:
        p2.rotate_to(p.world_center)
        p2.move_forward(P2_MOVE_SPEED * dt)

    # Increment timers using dt
    GUI_UPDATE_TICK += dt
    DECELERATION_TICK += dt

    display.finish_frame()
