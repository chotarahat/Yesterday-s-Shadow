from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import sys
import random
import math
import os

# Camera-related variables from the original template

camera_pos = (0, 500, 500)

fovY = 120
GRID_LENGTH = 600
rand_var = 423

# App State Machine

APP_MAIN_MENU = 0
APP_PLAYING = 1
APP_PAUSED = 2
APP_SHOP = 3
APP_HOW_TO_PLAY = 4
APP_FAILED = 5
APP_COMPLETED = 6
app_state = APP_MAIN_MENU
menu_selection_index = 0
main_menu_selection = 0
how_to_back_hover = False
shop_selection_index = -1
failed_selection_index = 0
completed_selection_index = 0

MENU_CURSOR_STATES = (APP_MAIN_MENU,APP_PAUSED,APP_SHOP,APP_HOW_TO_PLAY,APP_FAILED,APP_COMPLETED)

# Phase 1 game state

# Player
player_x = 0
player_y = -350
player_z = 35
player_size = 35
player_speed = 25
player_rotation = 0

# Room
current_room = 1
room_width = 1000
room_depth = 800
room_wall_thickness = 40
room_wall_height = 120

# Exit / transition
exit_x_min = 380
exit_x_max = 500
exit_y_min = -80
exit_y_max = 80

# Simple game status
room_message = "Reach the eastern doorway."
game_running = False

# Phase 2 - Time-Freeze / Magic Window

GAME_NORMAL = 0
GAME_MAGIC_WINDOW = 1

game_state = GAME_NORMAL

ROOM_TIME_LIMIT = 150.0
room_time_remaining = ROOM_TIME_LIMIT

BASE_SPELL_CHARGES = 4
spell_charges = BASE_SPELL_CHARGES

BASE_MAGIC_WINDOW = 8.0
magic_window_duration = BASE_MAGIC_WINDOW
magic_window_remaining = 0.0

last_update_time = None
freeze_flash_timer = 0.0

# Phase 3 - Persistent Action Recording + Ghost Replay

GAME_NORMAL = 0
GAME_MAGIC_WINDOW = 1
game_state = GAME_NORMAL

SIMULATION_STEP = 0.016
RECORD_INTERVAL = 0.05

recording = []
recording_elapsed = 0.0
recording_active = False

ghosts = []
MAX_GHOSTS = 3

GHOST_MOVING = 0
GHOST_HOLDING = 1

ghost_message = "Press F to record your first action."

# Phase 4 - Interactive Buttons + Door Puzzle

BUTTON_RADIUS = 55

button_a_x = 80
button_a_y = 210

button_b_x = 80
button_b_y = -210

door_x = 430
door_y = 0
door_open = False

button_a_pressed = False
button_b_pressed = False

puzzle_message = "Activate both buttons to open the eastern door."


# Phase 5 - Level 1 Tutorial / First Complete Puzzle

level1_started = True
level1_completed = False
level1_step = 0

LEVEL1_STEP_A = 0
LEVEL1_STEP_B = 1
LEVEL1_STEP_EXIT = 2
LEVEL1_COMPLETE = 3

level1_message = "Step 1: create a Ghost on Button A."

# Phase 6 - Level 2 Multi-Ghost Puzzle

level2_step = 0
level2_completed = False

LEVEL2_GHOST_A = 0
LEVEL2_GHOST_B = 1
LEVEL2_PLAYER_EXIT = 2
LEVEL2_COMPLETE = 3

level2_button_a_x = -40
level2_button_a_y = 210
level2_button_b_x = -40
level2_button_b_y = -210

level2_door_x = 430
level2_door_y = 0

level2_button_a_pressed = False
level2_button_b_pressed = False
level2_door_open = False

level2_message = "Room 2: create the first Ghost on Button A."

# Phase 7 - Torch / Darkness System


TORCH_MAX_CHARGE = 180
TORCH_DRAIN_PER_STEP = 0.028

torch_charge = TORCH_MAX_CHARGE
torch_on = True

TORCH_RADIUS_NEAR = 260
TORCH_RADIUS_FAR = 390

torch_message = "Torch active."


# Minimap / Room Indicator

MINIMAP_RADIUS = 72
MINIMAP_MARGIN = 26
MINIMAP_SCAN_RADIUS = 520
MINIMAP_DOT_RADIUS = 4

# Phase 8 - Environmental Hazards: Rifts + Spikes

HAZARD_RADIUS = 42

rift_x = 180
rift_y = 0
rift_active = True

spike_x = 300
spike_y = 130
spike_active = False

hazard_hit_cooldown = 0.0

hazard_message = "Watch for rifts and spikes."

# Phase 9 - Shadow Threat System

SHADOW_START_X = 120
SHADOW_START_Y = -320

shadow_x = SHADOW_START_X
shadow_y = SHADOW_START_Y
shadow_rotation = 0
shadow_active = True
shadow_distance = 0.0

SHADOW_SPEED = 0.255
SHADOW_CHASE_RADIUS = 650
SHADOW_CONTACT_RADIUS = 52

shadow_message = "The Shadow is watching."
shadow_hit_count = 0


# Phase 10 - Final-Level Closing Walls

FINAL_BUTTON_RADIUS = 55

final_button_1_x = 260
final_button_1_y = -260

final_button_2_x = -260
final_button_2_y = -20

final_button_3_x = 260
final_button_3_y = 180

portal_x = 0
portal_y = room_depth / 2

final_button_1_pressed = False
final_button_2_pressed = False
final_button_3_pressed = False
portal_open = False

final_level_message = "Final room: leave Ghosts on Buttons 1 and 2."
final_level_complete = False

# Button 3 Final Room
final_button_3_latched = False

# Phase 11 - Closing Walls / Final Pressure

WALL_START_LEFT = -470
WALL_START_RIGHT = 470

wall_left_x = WALL_START_LEFT
wall_right_x = WALL_START_RIGHT

WALL_CLOSE_SPEED = 0.42
WALL_MIN_GAP = 190

wall_1_y = -130
wall_2_y = 70
wall_3_y = 270

closing_walls_active = False
walls_closed = False

wall_message = "Final walls are waiting."
wall_crossed = [False, False, False]


# Phase 12 - Victory State


GAME_VICTORY = 4

victory_active = False
victory_message = "Reach the eastern door."

final_escape_x = portal_x
final_escape_y = portal_y

# Phase 13 - Coins, Shop, and Progress Rewards

STARTING_COINS = 60
coins = STARTING_COINS
level_start_coins = STARTING_COINS
shop_open = False
shop_message = "Press K to open the shop."
level1_rewarded = False
level2_rewarded = False
final_rewarded = False

SHOP_SPELL_COST = 6
SHOP_WINDOW_COST = 8
SHOP_TORCH_COST = 8
SHOP_GHOST_COST = 12


# coin/collectible economy

COIN_COLLECTIBLE_VALUE=5
COINS_GHOST_BUTTON=4
COINS_LEVEL_COMPLETE={1:12,2:18,3:30}
COINS_UNDER_ONE_MINUTE=12
collectible_coins=[]
collected_coin_ids=set()
button_rewarded=set()
level_completion_rewarded=set()
level_start_button_rewarded=set()
level_start_completion_rewarded=set()
level_failed_message=""
game_complete=False
coin_message=""

MAX_PLAYER_LIVES = 3
PLAYER_MAX_HEALTH = 100
SPIKE_DAMAGE = 25
BLUE_HAZARD_DAMAGE = 30
player_lives = MAX_PLAYER_LIVES
player_health = PLAYER_MAX_HEALTH

def spawn_collectible_coins():
    global collectible_coins,collected_coin_ids
    collectible_coins=[]; collected_coin_ids=set()
    for _ in range(120):
        if len(collectible_coins)>=7: break
        x=random.randint(-420,420); y=random.randint(-320,320)
        if abs(x)>420 or abs(y)>320: continue
        if current_room==2 and -120<x<120 and 0<y<140: continue
        if current_room==1 and any((x-bx)**2+(y-by)**2<100**2 for bx,by in [(button_a_x,button_a_y),(button_b_x,button_b_y),(door_x,door_y)]): continue
        if current_room==2 and any((x-bx)**2+(y-by)**2<100**2 for bx,by in [(level2_button_a_x,level2_button_a_y),(level2_button_b_x,level2_button_b_y),(level2_door_x,level2_door_y)]): continue
        if current_room==3 and any((x-bx)**2+(y-by)**2<100**2 for bx,by in [(final_button_1_x,final_button_1_y),(final_button_2_x,final_button_2_y),(final_button_3_x,final_button_3_y),(portal_x,portal_y)]): continue
        if any((x-c["x"])**2+(y-c["y"])**2<80**2 for c in collectible_coins): continue
        collectible_coins.append({"x":x,"y":y,"id":len(collectible_coins)})

def update_collectible_coins():
    global coins,coin_message
    if not torch_on:
        return

    for c in collectible_coins:
        if c["id"] not in collected_coin_ids and (player_x-c["x"])**2+(player_y-c["y"])**2<45**2:
            collected_coin_ids.add(c["id"]); coins+=COIN_COLLECTIBLE_VALUE
            coin_message=f"+{COIN_COLLECTIBLE_VALUE} coins collected."

def draw_collectible_coins():
    if not torch_on:
        return

    for c in collectible_coins:
        if c["id"] not in collected_coin_ids:
            draw_cylinder(c["x"],c["y"],8,12,12,(0.95,0.72,0.1))
            draw_sphere(c["x"],c["y"],25,9,(1.0,0.84,0.18))

def reward_button_once(key):
    global coins,coin_message
    if key not in button_rewarded:
        button_rewarded.add(key); coins+=COINS_GHOST_BUTTON
        coin_message=f"+{COINS_GHOST_BUTTON} coins: required button activated."

def reward_level(level):
    global coins, coin_message
    if level in level_completion_rewarded: return
    level_completion_rewarded.add(level)
    base=COINS_LEVEL_COMPLETE[level]
    bonus=COINS_UNDER_ONE_MINUTE if room_time_remaining>90 else 0
    coins+=base+bonus
    coin_message=f"Level {level} complete: +{base} coins" + (f" +{bonus} speed bonus." if bonus else ".")


def checkpoint_level_start():
    global level_start_coins
    global level_start_button_rewarded
    global level_start_completion_rewarded

    level_start_coins = coins
    level_start_button_rewarded = set(button_rewarded)
    level_start_completion_rewarded = set(level_completion_rewarded)


def restore_level_start_coins():
    global coins
    global button_rewarded
    global level_completion_rewarded
    global coin_message

    coins = level_start_coins
    button_rewarded = set(level_start_button_rewarded)
    level_completion_rewarded = set(level_start_completion_rewarded)
    coin_message = "Coins restored to level start: " + str(coins) + "."


def set_game_over(message="Game Over!!"):
    global app_state
    global game_running
    global level_failed_message
    global failed_selection_index

    level_failed_message = message
    game_running = False
    failed_selection_index = 0
    app_state = APP_FAILED
    sync_cursor_for_app_state()


def lose_player_life(reason):
    global player_lives
    global player_health
    global room_message

    player_lives -= 1
    player_health = PLAYER_MAX_HEALTH

    if player_lives <= 0:
        player_lives = 0
        room_message = reason + " No lives remaining."
        set_game_over("Game Over!!")
        return

    reset_room()
    room_message = reason + " Life lost. Restarting level."


def damage_player(amount, reason, lose_life_on_zero=True):
    global player_health
    global room_message

    player_health -= amount

    if player_health <= 0:
        player_health = 0
        if lose_life_on_zero:
            lose_player_life(reason)
        else:
            room_message = reason + " Health: 0%."
        return True

    room_message = reason + " Health: " + str(player_health) + "%."
    return False

# HUD Redesign Queues

transient_queue = []
important_queue = []

last_messages = {
    "room": "",
    "ghost": "",
    "puzzle": "",
    "level1": "",
    "level2": "",
    "torch": "",
    "hazard": "",
    "shadow": "",
    "wall": "",
    "victory": "",
    "shop": ""
}

# Text rendering

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1.0, 1.0, 1.0, 1.0), shadow=True):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    if shadow:
        glColor3f(0, 0, 0)
        glRasterPos2f(x + 2, y - 2)
        for ch in text:
            glutBitmapCharacter(font, ord(ch))

    glColor3f(color[0], color[1], color[2])
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glMatrixMode(GL_MODELVIEW)

# Basic 3D helper

def draw_cube(x, y, z, sx, sy, sz):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glutSolidCube(1)
    glPopMatrix()

# Visual helpers

def draw_box(x, y, z, sx, sy, sz, color):
    glColor3f(color[0], color[1], color[2])
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(sx, sy, sz)
    glutSolidCube(1)
    glPopMatrix()


def draw_cylinder(x, y, z, radius, height, color):
    glColor3f(color[0], color[1], color[2])
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluCylinder(quadric, radius, radius, height, 16, 2)
    glPopMatrix()


def draw_sphere(x, y, z, radius, color):
    glColor3f(color[0], color[1], color[2])
    glPushMatrix()
    glTranslatef(x, y, z)
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 16, 12)
    glPopMatrix()


def draw_floor_tiles():
    tile = 100
    for x in range(-500, 501, tile):
        for y in range(-400, 401, tile):
            if ((x // tile) + (y // tile)) % 2 == 0:
                color = (0.16, 0.15, 0.18)
            else:
                color = (0.20, 0.19, 0.21)

            glColor3f(color[0], color[1], color[2])
            glBegin(GL_QUADS)
            glVertex3f(x, y, 1)
            glVertex3f(x + tile, y, 1)
            glVertex3f(x + tile, y + tile, 1)
            glVertex3f(x, y + tile, 1)
            glEnd()


def draw_wall_bands():
    half_w = room_width / 2
    half_d = room_depth / 2
    band_height = 8

    draw_box(0, -half_d - 1, 105, room_width, 8, band_height,
             (0.12, 0.10, 0.11))
    draw_box(0, half_d + 1, 105, room_width, 8, band_height,
             (0.12, 0.10, 0.11))
    draw_box(-half_w - 1, 0, 105, 8, room_depth, band_height,
             (0.12, 0.10, 0.11))
    draw_box(half_w + 1, 0, 105, 8, room_depth, band_height,
             (0.12, 0.10, 0.11))


def draw_pillar(x, y):
    draw_box(x, y, 12, 90, 90, 24, (0.30, 0.25, 0.24))
    draw_box(x, y, 72, 58, 58, 120, (0.36, 0.30, 0.28))
    draw_box(x, y, 138, 78, 78, 20, (0.30, 0.25, 0.24))


def draw_archway():
    x = room_width / 2 - 12

    draw_box(x, -125, 75, 28, 28, 150, (0.38, 0.30, 0.25))
    draw_box(x, 125, 75, 28, 28, 150, (0.38, 0.30, 0.25))
    draw_box(x, 0, 150, 28, 278, 30, (0.38, 0.30, 0.25))
    draw_sphere(x - 18, 0, 78, 18, (0.65, 0.45, 0.12))


def draw_room_lighting_markers():
    torch_positions = [
        (-460, -250), (-460, 250),
        (250, -350), (250, 350)
    ]

    for x, y in torch_positions:
        draw_cylinder(x, y, 55, 8, 70, (0.18, 0.13, 0.10))
        draw_sphere(x, y, 132, 14, (0.70, 0.32, 0.08))

# Player

def draw_player():
    glPushMatrix()

    glTranslatef(player_x, player_y, 0)
    glRotatef(player_rotation, 0, 0, 1)

    draw_box(-12, -8, 10, 18, 26, 20, (0.08, 0.07, 0.07))
    draw_box(12, -8, 10, 18, 26, 20, (0.08, 0.07, 0.07))
    draw_box(0, 0, 42, 48, 34, 55, (0.16, 0.20, 0.30))
    draw_box(0, 0, 73, 58, 40, 20, (0.22, 0.28, 0.40))
    draw_sphere(0, 0, 102, 23, (0.52, 0.40, 0.32))
    draw_sphere(0, 0, 111, 27, (0.08, 0.09, 0.12))
    draw_box(0, 24, 74, 10, 8, 8, (0.65, 0.45, 0.12))

    glPopMatrix()


# Room geometry

def draw_floor():
    draw_floor_tiles()

def draw_room_walls():
    half_w = room_width / 2
    half_d = room_depth / 2
    wall_z = room_wall_height / 2

    # Back wall
    glColor3f(0.28, 0.20, 0.18)
    draw_cube(0, -half_d, wall_z, room_width, room_wall_thickness, room_wall_height)

    # Left wall
    glColor3f(0.32, 0.23, 0.20)
    draw_cube(-half_w, 0, wall_z, room_wall_thickness, room_depth, room_wall_height)

    # Keep the eastern border closed in the final room
    glColor3f(0.32, 0.23, 0.20)

    if current_room == 3:
        draw_cube(half_w, 0, wall_z, room_wall_thickness, room_depth, room_wall_height)
    else:
        doorway_half = 100
        right_segment_depth = (room_depth - doorway_half * 2) / 2
        draw_cube(half_w, -((room_depth / 2 + doorway_half) / 2), wall_z,
                  room_wall_thickness, right_segment_depth, room_wall_height)
        draw_cube(half_w, ((room_depth / 2 + doorway_half) / 2), wall_z,
                  room_wall_thickness, right_segment_depth, room_wall_height)

    # Front wall
    glColor3f(0.28, 0.20, 0.18)
    if current_room == 3:
        doorway_half = 100
        front_segment_width = (room_width - doorway_half * 2) / 2
        draw_cube(-((room_width / 2 + doorway_half) / 2), half_d, wall_z,
                  front_segment_width, room_wall_thickness, room_wall_height)
        draw_cube(((room_width / 2 + doorway_half) / 2), half_d, wall_z,
                  front_segment_width, room_wall_thickness, room_wall_height)
    else:
        draw_cube(0, half_d, wall_z, room_width, room_wall_thickness, room_wall_height)

    # The final portal is centered on the front wall.
    glColor3f(0.65, 0.45, 0.12)
    if current_room == 3:
        draw_cube(portal_x, portal_y - 5, 45, 190, 10, 90)
    else:
        draw_cube(half_w - 5, 0, 45, 10, 190, 90)


def draw_room_decorations():
    draw_pillar(-360, -270)
    draw_pillar(-360, 270)
    draw_pillar(220, -270)
    draw_pillar(220, 270)

    draw_wall_bands()
    draw_archway()
    draw_room_lighting_markers()

    if current_room == 2:
        draw_box(0, 50, 50, 180, 60, 100, (0.26, 0.17, 0.17))
        draw_box(0, 50, 105, 150, 50, 10, (0.38, 0.25, 0.22))
        draw_box(-120, -160, 35, 70, 70, 70, (0.25, 0.21, 0.20))
        draw_box(140, 160, 35, 70, 70, 70, (0.25, 0.21, 0.20))

# Collision

def player_hits_wall(new_x, new_y):
    global room_message
    half_w = room_width / 2
    half_d = room_depth / 2
    radius = player_size * 0.5

    # Outer boundaries.
    if new_x < -half_w + radius:
        return True

    if new_y < -half_d + radius:
        return True

    if new_y > half_d - radius:
        if current_room == 3 and portal_open and portal_x - 100 < new_x < portal_x + 100:
            pass
        else:
            return True

    if current_room == 3 and new_x > half_w - radius:
        return True

    if new_x > half_w - radius and current_room != 3:
        if current_room == 3 and (not portal_open or new_y < -100 or new_y > 100):
            return True

        if current_room != 3 and (new_y < -100 or new_y > 100):
            return True

    # Room 2 central obstacle.
    if current_room == 2:
        obstacle_x_min = -90 - radius
        obstacle_x_max = 90 + radius
        obstacle_y_min = 20 - radius
        obstacle_y_max = 80 + radius

        if (new_x > obstacle_x_min and new_x < obstacle_x_max and
                new_y > obstacle_y_min and new_y < obstacle_y_max):
            return True

    if solid_object_collision(new_x,new_y): return True
    if current_room == 3:
        if (wall_crossed[0] and
                player_y > wall_1_y + radius and
                new_y <= wall_1_y + radius):
            room_message = "Wall 1 has sealed behind you."
            return True

        if (wall_crossed[1] and
                player_y > wall_2_y + radius and
                new_y <= wall_2_y + radius):
            room_message = "Wall 2 has sealed behind you."
            return True

        if (wall_crossed[2] and
                player_y > wall_3_y + radius and
                new_y <= wall_3_y + radius):
            room_message = "Wall 3 has sealed behind you."
            return True

        if (player_y < wall_1_y - radius and
                new_y >= wall_1_y - radius and
                not final_button_1_pressed):
            room_message = "Wall 1 is closing. Leave a Ghost on Button 1."
            return True

        if (player_y < wall_2_y - radius and
                new_y >= wall_2_y - radius and
                not final_button_2_pressed):
            room_message = "Wall 2 is closing. Leave a Ghost on Button 2."
            return True

        if (player_y < wall_3_y - radius and
                new_y >= wall_3_y - radius and
                not final_button_3_latched):
            room_message = "Wall 3 needs a Ghost on Button 3."
            return True

    return False


def update_wall_crossing_locks():
    if current_room != 3:
        return

    radius = player_size * 0.5
    if player_y > wall_1_y + radius:
        wall_crossed[0] = True
    if player_y > wall_2_y + radius:
        wall_crossed[1] = True
    if player_y > wall_3_y + radius:
        wall_crossed[2] = True


def circle_rect_hit(cx,cy,r,x1,x2,y1,y2):
    nx=max(x1,min(cx,x2)); ny=max(y1,min(cy,y2))
    return (cx-nx)**2+(cy-ny)**2<r*r

def solid_object_collision(nx,ny):
    r=player_size*.5
    solids=[(-405,-315,-315,-225),(-405,-315,225,315),(175,265,-315,-225),(175,265,225,315)]
    if current_room==2: solids += [(-90,90,20,80),(-155,-85,-195,-125),(105,175,125,195)]
    if current_room==1:
        if not door_open: solids.append((door_x-30,door_x+30,-115,115))
    elif current_room==2:
        if not level2_door_open: solids.append((level2_door_x-30,level2_door_x+30,-115,115))
    else:
        if not portal_open: solids.append((portal_x-30,portal_x+30,portal_y-125,portal_y+125))
    return any(circle_rect_hit(nx,ny,r,*q) for q in solids)



# Room transition


def is_at_exit():
    half_w = room_width / 2

    # Phase 4: the eastern exit is locked until the room puzzle is solved.
    if current_room == 1 and not door_open:
        return False

    if current_room == 2 and not level2_door_open:
        return False

    if current_room == 3:
        return False

    if player_x > half_w - 60:
        if player_y > exit_y_min and player_y < exit_y_max:
            return True

    return False


def transition_room():
    global current_room
    global player_x
    global player_y
    global room_message
    global level1_step
    global level1_completed
    global level1_message
    global coins
    global level1_rewarded
    global level2_rewarded
    global level2_step
    global level2_completed
    global level2_door_open
    global level2_message

    if current_room == 1:
        level1_step = LEVEL1_COMPLETE
        level1_completed = True
        level1_message = "LEVEL 1 COMPLETE. Entering Room 2."

        if not level1_rewarded:
            reward_level(1)
            level1_rewarded = True

        current_room = 2
        checkpoint_level_start()
        player_x = -350
        player_y = 0
        reset_time_system()
        reset_ghost_system()
        reset_level2()
        start_level_with_torch_on()
        spawn_collectible_coins()
        room_message = "Room 2: use two Ghosts to open the eastern doorway."
    else:
        level2_step = LEVEL2_COMPLETE
        level2_completed = True
        level2_door_open = True
        level2_message = "LEVEL 2 COMPLETE."

        if not level2_rewarded:
            reward_level(2)
            level2_rewarded = True

        current_room = 3
        checkpoint_level_start()
        player_x = 0
        player_y = -340
        reset_time_system()
        reset_ghost_system()
        reset_final_level()
        reset_closing_walls()
        start_level_with_torch_on()
        spawn_collectible_coins()
        room_message = "FINAL ROOM: leave Ghosts on all three buttons."


# Player movement

def move_player(dx, dy, rotation):
    global player_x
    global player_y
    global player_rotation

    new_x = player_x + dx
    new_y = player_y + dy

    if not player_hits_wall(new_x, new_y):
        player_x = new_x
        player_y = new_y
        player_rotation = rotation
        update_wall_crossing_locks()

    if is_at_exit():
        transition_room()

    if current_room == 3:
        update_victory()

# Phase 2 - Time System

def reset_time_system():
    global game_state
    global room_time_remaining
    global spell_charges
    global magic_window_remaining
    global freeze_flash_timer

    game_state = GAME_NORMAL
    room_time_remaining = ROOM_TIME_LIMIT
    spell_charges = BASE_SPELL_CHARGES
    magic_window_remaining = 0.0
    freeze_flash_timer = 0.0


def cast_time_freeze():
    global game_state
    global magic_window_remaining
    global spell_charges
    global freeze_flash_timer
    global room_message

    if game_state != GAME_NORMAL:
        return

    if spell_charges <= 0:
        room_message = "No Time-Freeze charges remaining."
        return

    spell_charges -= 1
    game_state = GAME_MAGIC_WINDOW
    magic_window_remaining = magic_window_duration
    freeze_flash_timer = 0.35

    start_recording()

    room_message = "TIME-FREEZE ACTIVE - RECORD ONE ACTION!"


def update_time_system(dt):
    global game_state
    global room_time_remaining
    global magic_window_remaining
    global freeze_flash_timer
    global room_message
    global game_running
    global app_state
    global level_failed_message

    if freeze_flash_timer > 0:
        freeze_flash_timer -= dt
        if freeze_flash_timer < 0:
            freeze_flash_timer = 0

    if not game_running:
        return

    if game_state == GAME_NORMAL:
        room_time_remaining -= dt

        if room_time_remaining <= 0:
            room_time_remaining = 0
            room_message = "TIME OUT - restart the level."
            set_game_over("Time's up!")

    elif game_state == GAME_MAGIC_WINDOW:
        magic_window_remaining -= dt

        if magic_window_remaining <= 0:
            magic_window_remaining = 0

            if recording_active:
                create_ghost_from_recording()

            game_state = GAME_NORMAL
            room_message = "Ghost created. Room timer resumed."


def get_game_state_text():
    if game_state == GAME_MAGIC_WINDOW:
        return "TIME-FREEZE / MAGIC WINDOW"
    if game_state == GAME_VICTORY:
        return "VICTORY"

    return "NORMAL"

# Phase 3 - Action Recording + Persistent Ghost Replay

def capture_snapshot(snapshot_time):
    return {
        "time": snapshot_time,
        "x": player_x,
        "y": player_y,
        "rotation": player_rotation
    }


def start_recording():
    global recording
    global recording_elapsed
    global recording_active
    global ghost_message

    recording = []
    recording_elapsed = 0.0
    recording_active = True
    recording.append(capture_snapshot(0.0))
    ghost_message = "Recording: perform one action now."


def update_recording(dt):
    global recording_elapsed

    if not recording_active:
        return

    recording_elapsed += dt
    next_snapshot_time = recording[-1]["time"] + RECORD_INTERVAL

    while recording_elapsed >= next_snapshot_time:
        recording.append(capture_snapshot(next_snapshot_time))
        next_snapshot_time += RECORD_INTERVAL


def create_ghost_from_recording():
    global recording_active
    global ghosts
    global ghost_message

    recording_active = False

    if len(recording) < 2:
        ghost_message = "Action was too short. Move during the window."
        return

    if len(ghosts) >= MAX_GHOSTS:
        ghost_message = "Ghost limit reached. Press R to retry."
        return

    ghost = {
        "recording": list(recording),
        "replay_time": 0.0,
        "replay_index": 0,
        "x": recording[0]["x"],
        "y": recording[0]["y"],
        "rotation": recording[0]["rotation"],
        "state": GHOST_MOVING,
        "active": True
    }

    ghosts.append(ghost)
    ghost_message = "Ghost created. Replaying your recorded action."


def update_ghosts(dt):
    for ghost in ghosts:
        if not ghost["active"]:
            continue

        data = ghost["recording"]

        if len(data) == 0:
            ghost["active"] = False
            continue

        if ghost["state"] == GHOST_HOLDING:
            ghost["x"] = data[-1]["x"]
            ghost["y"] = data[-1]["y"]
            ghost["rotation"] = data[-1]["rotation"]
            continue

        ghost["replay_time"] += dt

        while (
            ghost["replay_index"] + 1 < len(data)
            and data[ghost["replay_index"] + 1]["time"] <= ghost["replay_time"]
        ):
            ghost["replay_index"] += 1

        current = data[ghost["replay_index"]]
        ghost["x"] = current["x"]
        ghost["y"] = current["y"]
        ghost["rotation"] = current["rotation"]

        if ghost["replay_time"] >= data[-1]["time"]:
            ghost["replay_index"] = len(data) - 1
            ghost["x"] = data[-1]["x"]
            ghost["y"] = data[-1]["y"]
            ghost["rotation"] = data[-1]["rotation"]
            ghost["state"] = GHOST_HOLDING


def draw_ghost(ghost):
    if not ghost["active"]:
        return

    glPushMatrix()
    glTranslatef(ghost["x"], ghost["y"], 0)
    glRotatef(ghost["rotation"], 0, 0, 1)

    draw_box(0, 0, 42, 48, 34, 55, (0.32, 0.48, 0.58))
    draw_sphere(0, 0, 102, 23, (0.52, 0.68, 0.72))
    draw_sphere(0, 0, 111, 27, (0.16, 0.23, 0.29))
    draw_box(0, 24, 74, 10, 8, 8, (0.75, 0.78, 0.62))

    glPopMatrix()


def get_active_ghost_count():
    count = 0
    for ghost in ghosts:
        if ghost["active"]:
            count += 1
    return count


def get_ghost_status_text():
    if recording_active:
        return "RECORDING ACTION"

    moving = 0
    holding = 0

    for ghost in ghosts:
        if not ghost["active"]:
            continue

        if ghost["state"] == GHOST_HOLDING:
            holding += 1
        else:
            moving += 1

    return (
        "Ghosts: " + str(get_active_ghost_count()) +
        "/" + str(MAX_GHOSTS) +
        "  Moving: " + str(moving) +
        "  Holding: " + str(holding)
    )


def reset_ghost_system():
    global recording
    global recording_elapsed
    global recording_active
    global ghosts
    global ghost_message

    recording = []
    recording_elapsed = 0.0
    recording_active = False
    ghosts = []
    ghost_message = "Ghost system reset."



# Phase 4 - Button / Door Puzzle System


def point_is_on_button(x, y, button_x, button_y):
    dx = x - button_x
    dy = y - button_y

    return (dx * dx + dy * dy) <= (BUTTON_RADIUS * BUTTON_RADIUS)


def player_on_button(button_x, button_y):
    return point_is_on_button(
        player_x,
        player_y,
        button_x,
        button_y
    )


def ghost_on_button(ghost, button_x, button_y):
    if not ghost["active"]:
        return False

    return point_is_on_button(
        ghost["x"],
        ghost["y"],
        button_x,
        button_y
    )


def button_has_actor(button_x, button_y):
    if player_on_button(button_x, button_y):
        return True

    for ghost in ghosts:
        if ghost_on_button(ghost, button_x, button_y):
            return True

    return False


def update_puzzle_state():
    global button_a_pressed
    global button_b_pressed
    global door_open
    global puzzle_message

    # Room 1 is the tutorial puzzle room.
    if current_room != 1:
        button_a_pressed = False
        button_b_pressed = False
        door_open = True
        puzzle_message = "Door open."
        return

    button_a_pressed = button_has_actor(
        button_a_x,
        button_a_y
    )

    button_b_pressed = button_has_actor(
        button_b_x,
        button_b_y
    )

    if button_a_pressed and button_b_pressed:
        reward_button_once("L1_A"); reward_button_once("L1_B")
        door_open = True
        puzzle_message = "Both buttons are active. Door OPEN."
    else:
        door_open = False

        if button_a_pressed or button_b_pressed:
            puzzle_message = "One button active. The door remains locked."
        else:
            puzzle_message = "Activate both buttons to open the eastern door."


def draw_button(button_x, button_y, pressed, label):
    if pressed:
        base_z = 8
        top_z = 18
        color = (0.20, 0.55, 0.24)
    else:
        base_z = 8
        top_z = 24
        color = (0.45, 0.18, 0.16)

    
    draw_box(button_x,button_y,base_z,90,90,16,(0.16, 0.14, 0.14))

    
    draw_box(button_x,button_y,top_z,65,65,18,color)

    
    draw_sphere(button_x,button_y,top_z + 14,9,color)

def draw_puzzle_objects():
    if current_room != 1:
        return

    draw_button(button_a_x,button_a_y,button_a_pressed,"A")

    draw_button(button_b_x,button_b_y,button_b_pressed,"B")

    if door_open:
        draw_box(door_x,door_y,12,50,230,24,(0.18, 0.45, 0.22))
    else:
        draw_box(door_x,door_y,90,50,230,180,(0.18, 0.12, 0.14))

    draw_box(door_x - 8,door_y,12,15,250,24,(0.55, 0.38, 0.12))

def reset_puzzle():
    global button_a_pressed
    global button_b_pressed
    global door_open
    global puzzle_message

    button_a_pressed = False
    button_b_pressed = False
    door_open = False
    puzzle_message = "Activate both buttons to open the eastern door."

# Phase 5 - Level 1 Tutorial Progression

def reset_level1():
    global level1_started
    global level1_completed
    global level1_step
    global level1_message

    level1_started = True
    level1_completed = False
    level1_step = LEVEL1_STEP_A
    level1_message = "Step 1: create a Ghost on Button A."

def update_level1():
    global level1_step
    global level1_completed
    global level1_message

    if current_room != 1:
        return

    if level1_step == LEVEL1_STEP_A:
        if button_a_pressed:
            level1_step = LEVEL1_STEP_B
            level1_message = "Step 2: reach Button B while the Ghost holds A."

    elif level1_step == LEVEL1_STEP_B:
        if button_a_pressed and button_b_pressed:
            level1_step = LEVEL1_STEP_EXIT
            level1_message = "Step 3: both buttons are active. Reach the exit."

    elif level1_step == LEVEL1_STEP_EXIT:
        if door_open:
            level1_message = "Door unlocked. Move through the eastern exit."

    elif level1_step == LEVEL1_COMPLETE:
        level1_completed = True
        level1_message = "LEVEL 1 COMPLETE."


def draw_level1_progress():
    if current_room != 1:
        return

    if level1_step == LEVEL1_STEP_A:
        draw_text(650, 760, "LEVEL 1: STEP 1 / 3")
    elif level1_step == LEVEL1_STEP_B:
        draw_text(650, 760, "LEVEL 1: STEP 2 / 3")
    elif level1_step == LEVEL1_STEP_EXIT:
        draw_text(650, 760, "LEVEL 1: STEP 3 / 3")
    else:
        draw_text(650, 760, "LEVEL 1: COMPLETE")

# Phase 6 - Level 2 Multi-Ghost Puzzle

def level2_point_is_on_button(x, y, button_x, button_y):
    dx = x - button_x
    dy = y - button_y
    return (dx * dx + dy * dy) <= (BUTTON_RADIUS * BUTTON_RADIUS)

def level2_player_on_button(button_x, button_y):
    return level2_point_is_on_button(player_x,player_y,button_x,button_y)

def level2_ghost_on_button(ghost, button_x, button_y):
    if not ghost["active"]:
        return False

    return level2_point_is_on_button(ghost["x"],ghost["y"],button_x,button_y)

def level2_button_has_ghost(button_x, button_y):
    for ghost in ghosts:
        if level2_ghost_on_button(ghost, button_x, button_y):
            return True
    return False

def level2_button_has_actor(button_x, button_y):
    if level2_player_on_button(button_x, button_y):
        return True

    return level2_button_has_ghost(button_x, button_y)

def update_level2():
    global level2_step
    global level2_completed
    global level2_button_a_pressed
    global level2_button_b_pressed
    global level2_door_open
    global level2_message

    if current_room != 2:
        return

    level2_button_a_held_by_ghost = level2_button_has_ghost(level2_button_a_x,level2_button_a_y)

    level2_button_b_held_by_ghost = level2_button_has_ghost(level2_button_b_x,level2_button_b_y)

    level2_button_a_pressed = level2_button_has_actor(level2_button_a_x,level2_button_a_y)

    level2_button_b_pressed = level2_button_has_actor(level2_button_b_x,level2_button_b_y)

    level2_door_open = level2_button_a_held_by_ghost and level2_button_b_held_by_ghost

    if level2_step == LEVEL2_GHOST_A:
        if level2_button_a_held_by_ghost:
            reward_button_once("L2_A")
            level2_step = LEVEL2_GHOST_B
            level2_message = "Ghost 1 is holding A. Create Ghost 2 on B."

    elif level2_step == LEVEL2_GHOST_B:
        if level2_button_a_held_by_ghost and level2_button_b_held_by_ghost:
            reward_button_once("L2_B")
            level2_step = LEVEL2_PLAYER_EXIT
            level2_message = "Two Ghosts hold both buttons. Reach the exit."

    elif level2_step == LEVEL2_PLAYER_EXIT:
        if level2_door_open:
            level2_message = "Both Ghosts remain active. Exit is open."
        else:
            level2_message = "A Ghost left a button. Put Ghosts on both buttons."


def reset_level2():
    global level2_step
    global level2_completed
    global level2_button_a_pressed
    global level2_button_b_pressed
    global level2_door_open
    global level2_message

    level2_step = LEVEL2_GHOST_A
    level2_completed = False
    level2_button_a_pressed = False
    level2_button_b_pressed = False
    level2_door_open = False
    level2_message = "Room 2: create the first Ghost on Button A."


def draw_level2_button(button_x, button_y, pressed):
    if pressed:
        color = (0.20, 0.55, 0.24)
        top_z = 18
    else:
        color = (0.45, 0.18, 0.16)
        top_z = 24

    draw_box(button_x, button_y, 8,90, 90, 16,(0.16, 0.14, 0.14))

    draw_box(button_x, button_y, top_z,65, 65, 18,color)

    draw_sphere(button_x, button_y, top_z + 14,9, color)


def draw_level2_objects():
    if current_room != 2:
        return

    draw_level2_button(level2_button_a_x,level2_button_a_y,level2_button_a_pressed)

    draw_level2_button(level2_button_b_x,level2_button_b_y,level2_button_b_pressed)

    if level2_door_open:
        draw_box(level2_door_x,level2_door_y,12,50,230,24,(0.18, 0.45, 0.22))
    else:
        draw_box(level2_door_x,level2_door_y,90,50,230,180,(0.18, 0.12, 0.14))

# Phase 7 - Torch / Darkness System

def toggle_torch():
    global torch_on
    global torch_message

    if torch_charge <= 0:
        torch_on = False
        torch_message = "Torch empty. Find a refill."
        return

    torch_on = not torch_on

    if torch_on:
        torch_message = "Torch active."
    else:
        torch_message = "Torch off. Darkness surrounds you."


def update_torch():
    global torch_charge
    global torch_on
    global torch_message

    if not torch_on:
        return

    if torch_charge > 0:
        torch_charge -= TORCH_DRAIN_PER_STEP

        if torch_charge <= 0:
            torch_charge = 0
            torch_on = False
            torch_message = "Torch empty. Find a refill."


def refill_torch():
    global torch_charge
    global torch_on
    global torch_message

    torch_charge = TORCH_MAX_CHARGE
    torch_on = True
    torch_message = "Torch refilled."


def get_torch_charge_text():
    return "Torch: " + str(int(torch_charge)) + "%"


def draw_torch_darkness():
    if torch_on: return
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0,1000,0,800)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glColor3f(0.005,0.004,0.01); glBegin(GL_QUADS)
    glVertex2f(0,0); glVertex2f(1000,0); glVertex2f(1000,800); glVertex2f(0,800); glEnd()
    glPopMatrix(); glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)


def start_level_with_torch_on():
    global torch_charge
    global torch_on
    global torch_message

    torch_charge = TORCH_MAX_CHARGE
    torch_on = True
    torch_message = "Torch active."

# Phase 8 - Environmental Hazards: Rifts + Spikes

def point_is_on_hazard(x, y, hazard_x, hazard_y):
    dx = x - hazard_x
    dy = y - hazard_y
    return (dx * dx + dy * dy) <= (HAZARD_RADIUS * HAZARD_RADIUS)


def get_white_spike_positions():
    if current_room == 1:
        return [
            (spike_x, spike_y),
            (-220, -150)
        ]

    return [(spike_x, spike_y)]


def player_hits_hazard():
    return player_hits_rift() or player_hits_spike()


def player_hits_rift():
    if current_room != 2 and current_room != 3:
        return False

    if rift_active and point_is_on_hazard(
        player_x, player_y, rift_x, rift_y
    ):
        return True

    return False


def player_hits_spike():
    if not spike_active:
        return False

    for sx, sy in get_white_spike_positions():
        if point_is_on_hazard(player_x, player_y, sx, sy):
            return True

    return False


def ghost_hits_hazard(ghost):
    if not ghost["active"] or (current_room != 2 and current_room != 3):
        return False

    if rift_active and point_is_on_hazard(
        ghost["x"], ghost["y"], rift_x, rift_y
    ):
        return True

    if spike_active:
        for sx, sy in get_white_spike_positions():
            if point_is_on_hazard(ghost["x"], ghost["y"], sx, sy):
                return True

    return False


def update_hazards():
    global room_message
    global hazard_message
    global hazard_hit_cooldown

    if hazard_hit_cooldown > 0:
        hazard_hit_cooldown = max(0, hazard_hit_cooldown - SIMULATION_STEP)
        return

    if player_hits_spike():
        damage_player(SPIKE_DAMAGE, "Spike hit.")
        hazard_hit_cooldown = 0.8
        hazard_message = "White spike hit: -" + str(SPIKE_DAMAGE) + "% health."
        return

    if player_hits_rift():
        damage_player(BLUE_HAZARD_DAMAGE, "Blue hazard hit.")
        hazard_hit_cooldown = 0.8
        hazard_message = "Blue hazard hit: -" + str(BLUE_HAZARD_DAMAGE) + "% health."
        return

    for ghost in ghosts:
        if ghost_hits_hazard(ghost):
            hazard_message = "A Ghost is crossing a dangerous area."


def draw_rift():
    if (current_room != 2 and current_room != 3) or not rift_active:
        return

    draw_box(rift_x, rift_y, 5,125, 55, 8,(0.05, 0.18, 0.42))

    draw_box(rift_x, rift_y, 11, 80, 30, 10,(0.10, 0.42, 0.85))


def draw_spike_at(x, y):
    draw_box(x - 28, y, 18,18, 18, 36,(0.45, 0.42, 0.38))

    draw_box(x, y, 28,18, 18, 56,(0.55, 0.50, 0.44))

    draw_box( x + 28, y, 18,18, 18, 36,(0.45, 0.42, 0.38))


def draw_spikes():
    if not spike_active:
        return

    for sx, sy in get_white_spike_positions():
        draw_spike_at(sx, sy)


def draw_hazards():
    draw_rift()
    draw_spikes()

# Phase 9 - Shadow Threat System

def reset_shadow():
    global shadow_x
    global shadow_y
    global shadow_rotation
    global shadow_active
    global shadow_distance
    global shadow_message
    global shadow_hit_count

    shadow_x = SHADOW_START_X
    shadow_y = SHADOW_START_Y
    shadow_rotation = 0
    shadow_active = True
    shadow_distance = 0.0
    shadow_message = "The Shadow is watching."
    shadow_hit_count = 0


def shadow_distance_to_player():
    dx = player_x - shadow_x
    dy = player_y - shadow_y
    return (dx * dx + dy * dy) ** 0.5


def move_shadow_toward_player():
    global shadow_x
    global shadow_y
    global shadow_rotation
    global shadow_distance

    if not shadow_active or game_state == GAME_MAGIC_WINDOW:
        return
    if current_room in (2, 3) and not torch_on:
        shadow_distance = shadow_distance_to_player()
        return

    dx = player_x - shadow_x
    dy = player_y - shadow_y
    distance = (dx * dx + dy * dy) ** 0.5
    shadow_distance = distance

    if distance <= 0 or distance > SHADOW_CHASE_RADIUS:
        return

    step = SHADOW_SPEED
    if distance < step:
        step = distance

    shadow_x += (dx / distance) * step
    shadow_y += (dy / distance) * step

    if abs(dx) > abs(dy):
        shadow_rotation = -90 if dx > 0 else 90
    else:
        shadow_rotation = 0 if dy > 0 else 180


def shadow_hits_player():
    if not shadow_active:
        return False
    return shadow_distance_to_player() <= SHADOW_CONTACT_RADIUS


def update_shadow():
    global room_message
    global shadow_message
    global shadow_hit_count

    if (current_room != 2 and current_room != 3) or not shadow_active:
        return

    move_shadow_toward_player()

    if shadow_hits_player():
        shadow_hit_count += 1
        shadow_message = "The Shadow caught you. Keep moving."
        lose_player_life("Shadow contact.")


def draw_shadow():
    if (current_room != 2 and current_room != 3) or not shadow_active:
        return

    glPushMatrix()
    glTranslatef(shadow_x, shadow_y, 0)
    glRotatef(shadow_rotation, 0, 0, 1)

    draw_box(0, 0, 48, 58, 42, 65, (0.055, 0.045, 0.065))
    draw_sphere(0, 0, 112, 27, (0.075, 0.055, 0.085))
    draw_sphere(-9, 22, 118, 4, (0.72, 0.24, 0.18))
    draw_sphere(9, 22, 118, 4, (0.72, 0.24, 0.18))

    glPopMatrix()


def get_shadow_status_text():
    if current_room != 2 and current_room != 3:
        return "Shadow: dormant"

    return (
        "Shadow: active  Distance: " +
        str(int(shadow_distance)) +
        "  Contacts: " +
        str(shadow_hit_count)
    )

# Phase 10 - Closing Walls / Extraction Portal

def final_point_is_on_button(x, y, button_x, button_y):
    dx = x - button_x
    dy = y - button_y
    return (dx * dx + dy * dy) <= (FINAL_BUTTON_RADIUS * FINAL_BUTTON_RADIUS)

def final_ghost_on_button(button_x, button_y):
    for ghost in ghosts:
        if ghost["active"] and final_point_is_on_button(ghost["x"],ghost["y"],button_x,button_y):
            return True
    return False

def final_player_on_button(button_x, button_y):
    return final_point_is_on_button(player_x, player_y,button_x,button_y)

def final_button_has_actor(button_x, button_y):
    if final_player_on_button(button_x, button_y):
        return True

    return final_ghost_on_button(button_x, button_y)


def update_final_level():
    global final_button_1_pressed
    global final_button_2_pressed
    global final_button_3_pressed
    global portal_open
    global final_level_message
    global final_button_3_latched

    if current_room != 3:
        return

    final_button_1_held_by_ghost = final_ghost_on_button(final_button_1_x,final_button_1_y)

    final_button_2_held_by_ghost = final_ghost_on_button(final_button_2_x,final_button_2_y)

    final_button_3_held_by_ghost = final_ghost_on_button(final_button_3_x,final_button_3_y)

    final_button_1_pressed = final_button_has_actor(final_button_1_x,final_button_1_y)

    final_button_2_pressed = final_button_has_actor(final_button_2_x,final_button_2_y)

    final_button_3_pressed = final_button_has_actor(final_button_3_x,final_button_3_y)

    final_button_3_latched = final_button_3_held_by_ghost

    if (final_button_1_held_by_ghost and final_button_2_held_by_ghost and final_button_3_held_by_ghost):
        reward_button_once("L3_1"); reward_button_once("L3_2"); reward_button_once("L3_3")
        portal_open = True
        final_level_message = "ALL WALLS HALTED. Reach the eastern door."
    else:
        portal_open = False

        if not final_button_1_held_by_ghost:
            final_level_message = "Need a Ghost on Button 1."
        elif not final_button_2_held_by_ghost:
            final_level_message = "Need a Ghost on Button 2."
        elif not final_button_3_held_by_ghost:
            final_level_message = "Need a Ghost on Button 3."


def draw_final_button(button_x, button_y, pressed, label):
    if pressed:
        color = (0.20, 0.55, 0.24)
        top_z = 18
    else:
        color = (0.45, 0.18, 0.16)
        top_z = 24

    draw_box(button_x,button_y,8,90,90,16,(0.16, 0.14, 0.14))

    draw_box(button_x,button_y,top_z,65,65,18,color)

    draw_sphere(button_x,button_y,top_z + 14,9,color)


def draw_extraction_portal():
    if current_room != 3:
        return

    if portal_open:
        draw_box(portal_x,portal_y,12,50,230,24,(0.18, 0.52, 0.30))

        draw_box(portal_x - 8,portal_y,12,15,250,24,(0.55, 0.38, 0.12))
    else:
        draw_box(portal_x,portal_y,90,50,230,180,(0.12, 0.10, 0.14))

        draw_box(portal_x - 8,portal_y,12,15,250,24,(0.55, 0.38, 0.12))


def draw_final_level_objects():
    if current_room != 3:
        return

    draw_final_button(final_button_1_x,final_button_1_y,final_button_1_pressed,"1")

    draw_final_button(final_button_2_x,final_button_2_y,final_button_2_pressed,"2")

    draw_final_button(final_button_3_x,final_button_3_y,final_button_3_pressed,"3")

    draw_extraction_portal()


def reset_final_level():
    global final_button_1_pressed
    global final_button_2_pressed
    global final_button_3_pressed
    global portal_open
    global final_level_message
    global final_level_complete
    global final_button_3_latched

    final_button_1_pressed = False
    final_button_2_pressed = False
    final_button_3_pressed = False
    portal_open = False
    final_level_message = "Final room: leave Ghosts on Buttons 1 and 2."
    final_level_complete = False
    final_button_3_latched = False

# Phase 11 - Closing Walls / Final Pressure

def reset_closing_walls():
    global wall_left_x
    global wall_right_x
    global closing_walls_active
    global walls_closed
    global wall_message
    global wall_crossed

    wall_left_x = WALL_START_LEFT
    wall_right_x = WALL_START_RIGHT
    closing_walls_active = False
    walls_closed = False
    wall_message = "Final walls are waiting."
    wall_crossed = [False, False, False]


def update_closing_walls():
    global wall_left_x
    global wall_right_x
    global closing_walls_active
    global walls_closed
    global wall_message
    if current_room != 3:
        return

    closing_walls_active = True
    walls_closed = False

    if not final_button_1_pressed:
        wall_message = "Wall 1 closing: Ghost 1 must hold Button 1."
    elif not final_button_2_pressed:
        wall_message = "Wall 2 closing: Ghost 2 must hold Button 2."
    elif not final_button_3_latched:
        wall_message = "Wall 3 closing: leave a Ghost on Button 3."
    else:
        wall_message = "All three walls are halted. Run for the eastern door."


def draw_closing_walls():
    if current_room != 3:
        return

    if not closing_walls_active:
        return

    wall_data = [(wall_1_y, final_button_1_pressed),(wall_2_y, final_button_2_pressed),(wall_3_y, final_button_3_latched)]

    for wall_y, held_open in wall_data:
        if not held_open:
            draw_box(0, wall_y, 76, 940, 35, 150, (0.14, 0.09, 0.12))


def get_wall_status_text():
    if current_room != 3:
        return "Walls: dormant"

    if not closing_walls_active:
        return "Walls: waiting"

    return "Walls: 1=" + ("OPEN" if final_button_1_pressed else "CLOSED") + \
           " 2=" + ("OPEN" if final_button_2_pressed else "CLOSED") + \
           " 3=" + ("OPEN" if final_button_3_latched else "CLOSED")

# Phase 12 - Final Extraction / Victory State

def reset_victory():
    global victory_active
    global victory_message

    victory_active = False
    victory_message = "Reach the eastern door."

def player_at_final_escape():
    if current_room != 3:
        return False

    half_w = room_width / 2

    return (
        portal_open
        and player_y > room_depth / 2 - 70
        and portal_x - 100 < player_x < portal_x + 100
    )


def update_victory():
    global victory_active
    global victory_message
    global game_state
    global game_running
    global final_level_complete
    global final_rewarded
    global coins
    global game_complete
    global app_state
    global completed_selection_index

    if current_room != 3:
        return

    if victory_active:
        return

    if not portal_open:
        victory_message = "Activate all three buttons."
        return

    if player_at_final_escape():
        victory_active = True
        game_state = GAME_VICTORY
        game_running = False
        final_level_complete = True
        if not final_rewarded:
            reward_level(3)
            final_rewarded = True
        victory_message = "ESCAPE COMPLETE - YESTERDAY'S SHADOW SURVIVED."
        game_complete=True
        completed_selection_index = 0
        app_state=APP_COMPLETED
        sync_cursor_for_app_state()


def draw_victory_overlay():
    if not victory_active:
        return

    # immediate-mode HUD system.
    draw_text(300, 430, "YESTERDAY'S SHADOW")
    draw_text(300, 400, "ESCAPE COMPLETE")
    draw_text(300, 370, "THE SHADOW CANNOT FOLLOW YOU HERE.")
    draw_text(300, 340, "PRESS R TO RESTART")

# Keyboard input

def sync_cursor_for_app_state():
    return


def keyboardListener(key,x,y):
    global app_state,menu_selection_index,main_menu_selection,game_running
    global coins,spell_charges,magic_window_duration,torch_charge,torch_on,MAX_GHOSTS,shop_message
    global failed_selection_index, completed_selection_index
    if app_state==APP_MAIN_MENU:
        if key in (b'w',b's'): main_menu_selection=(main_menu_selection+(1 if key==b's' else -1))%4
        elif key in (b'\r',b' '):
            if main_menu_selection==0: restart_game()
            elif main_menu_selection in (1,2): app_state=APP_HOW_TO_PLAY
            else: quit_game()
        return
    if app_state==APP_COMPLETED:
        if key in (b'w',b's'):
            completed_selection_index=(completed_selection_index+(1 if key==b's' else -1))%2
        elif key in (b'\r',b' '):
            if completed_selection_index==0: restart_game()
            else: quit_game()
        elif key==b'x': quit_game()
        return
    if app_state==APP_FAILED:
        if key in (b'w',b's'):
            failed_selection_index=(failed_selection_index+(1 if key==b's' else -1))%2
        elif key in (b'r',b'\r',b' '):
            if failed_selection_index==0:
                restart_game()
            else:
                app_state=APP_MAIN_MENU
                game_running=False
                sync_cursor_for_app_state()
        elif key==b'm': app_state=APP_MAIN_MENU; game_running=False
        sync_cursor_for_app_state()
        return
    if key==b'\x1b':
        if app_state==APP_PLAYING: app_state=APP_PAUSED; menu_selection_index=0
        elif app_state in (APP_SHOP,APP_HOW_TO_PLAY): app_state=APP_PAUSED
        elif app_state==APP_PAUSED: app_state=APP_PLAYING
        sync_cursor_for_app_state()
        return
    if app_state==APP_PAUSED:
        if key in (b'w',b's'): menu_selection_index=(menu_selection_index+(1 if key==b's' else -1))%6
        elif key==b'\r':
            if menu_selection_index==0: app_state=APP_PLAYING
            elif menu_selection_index==1: reset_room(); app_state=APP_PLAYING
            elif menu_selection_index==2: restart_game()
            elif menu_selection_index==3: app_state=APP_SHOP
            elif menu_selection_index==4: app_state=APP_HOW_TO_PLAY
            else: quit_game()
            sync_cursor_for_app_state()
        return
    if app_state==APP_SHOP:
        if key in (b'\x08',b'\x1b'): app_state=APP_PAUSED
        elif key in (b'1',b'2',b'3',b'4'): buy_shop_item(int(key)-48)
        else: shop_message="Not enough coins."
        return
    if app_state==APP_HOW_TO_PLAY:
        if key in (b'\x08',b'\x1b'):
            app_state=APP_MAIN_MENU if not game_running else APP_PAUSED
            sync_cursor_for_app_state()
        return
    if app_state!=APP_PLAYING: return
    if key==b'w' and game_running: move_player(0,player_speed,0)
    elif key==b's' and game_running: move_player(0,-player_speed,180)
    elif key==b'a' and game_running: move_player(-player_speed,0,90)
    elif key==b'd' and game_running: move_player(player_speed,0,-90)
    elif key==b'f' and game_running: cast_time_freeze()
    elif key==b't' and game_running: toggle_torch()
    elif key==b'k' and game_running:
        app_state=APP_SHOP
        sync_cursor_for_app_state()
    elif key==b'r': reset_room()

def specialKeyListener(key,x,y):
    global main_menu_selection,menu_selection_index,failed_selection_index,completed_selection_index
    if app_state==APP_MAIN_MENU:
        if key==GLUT_KEY_UP: main_menu_selection=(main_menu_selection-1)%4
        elif key==GLUT_KEY_DOWN: main_menu_selection=(main_menu_selection+1)%4
    elif app_state==APP_PAUSED:
        if key==GLUT_KEY_UP: menu_selection_index=(menu_selection_index-1)%6
        elif key==GLUT_KEY_DOWN: menu_selection_index=(menu_selection_index+1)%6
    elif app_state==APP_FAILED:
        if key==GLUT_KEY_UP: failed_selection_index=(failed_selection_index-1)%2
        elif key==GLUT_KEY_DOWN: failed_selection_index=(failed_selection_index+1)%2
    elif app_state==APP_COMPLETED:
        if key==GLUT_KEY_UP: completed_selection_index=(completed_selection_index-1)%2
        elif key==GLUT_KEY_DOWN: completed_selection_index=(completed_selection_index+1)%2
    elif app_state==APP_PLAYING and game_running:
        if key==GLUT_KEY_UP: move_player(0,player_speed,0)
        elif key==GLUT_KEY_DOWN: move_player(0,-player_speed,180)
        elif key==GLUT_KEY_LEFT: move_player(-player_speed,0,90)
        elif key==GLUT_KEY_RIGHT: move_player(player_speed,0,-90)

def hud_mouse_coordinates(x,y):
    return x, 800-y

def buy_shop_item(item):
    global coins,spell_charges,magic_window_duration,shop_message,MAX_GHOSTS
    purchases={
        1:(SHOP_SPELL_COST,lambda: "Bought one spell charge."),
        2:(SHOP_WINDOW_COST,lambda: "Magic Window extended."),
        3:(SHOP_TORCH_COST,lambda: "Torch recharged."),
        4:(SHOP_GHOST_COST,lambda: "Extra Ghost slot purchased.")
    }
    if item not in purchases:
        return
    cost,message=purchases[item]
    if coins<cost:
        shop_message="Not enough coins."
        return
    coins-=cost
    if item==1: spell_charges+=1
    elif item==2: magic_window_duration=min(12,magic_window_duration+1)
    elif item==3: refill_torch()
    else: MAX_GHOSTS=min(5,MAX_GHOSTS+1)
    shop_message=message()

def mouseListener(button,state,x,y):
    global app_state,main_menu_selection,menu_selection_index,how_to_back_hover
    global game_running, failed_selection_index, completed_selection_index
    if state!=GLUT_DOWN or button!=GLUT_LEFT_BUTTON:return
    hx,hy=hud_mouse_coordinates(x,y)
    if app_state==APP_MAIN_MENU:
        if 385<=hy<=435: main_menu_selection=0; restart_game()
        elif 323<=hy<373: main_menu_selection=1; app_state=APP_HOW_TO_PLAY
        elif 261<=hy<311: main_menu_selection=2; app_state=APP_HOW_TO_PLAY
        elif 199<=hy<249: main_menu_selection=3; quit_game()
    elif app_state==APP_COMPLETED:
        if 425<=hy<=475:
            completed_selection_index=0
            restart_game()
        elif 375<=hy<425:
            completed_selection_index=1
            quit_game()
    elif app_state==APP_FAILED:
        if 435<=hy<=485:
            failed_selection_index=0
            restart_game()
        elif 375<=hy<425:
            failed_selection_index=1
            app_state=APP_MAIN_MENU
            game_running=False
            sync_cursor_for_app_state()
    elif app_state==APP_PAUSED:
        if 480<=hy<=520: app_state=APP_PLAYING
        elif 420<=hy<480: reset_room(); app_state=APP_PLAYING
        elif 360<=hy<420: restart_game()
        elif 300<=hy<360: app_state=APP_SHOP
        elif 240<=hy<300: app_state=APP_HOW_TO_PLAY
        elif 180<=hy<240: quit_game()
        sync_cursor_for_app_state()
    elif app_state==APP_HOW_TO_PLAY:
        if 90 <= hy <= 135:
            app_state=APP_MAIN_MENU if not game_running else APP_PAUSED
            how_to_back_hover=False
            sync_cursor_for_app_state()
    elif app_state==APP_SHOP:
        if 525 <= hy <= 575: buy_shop_item(1)
        elif 475 <= hy < 525: buy_shop_item(2)
        elif 425 <= hy < 475: buy_shop_item(3)
        elif 375 <= hy < 425: buy_shop_item(4)
        elif 220 <= hy <= 280:
            app_state=APP_PAUSED
            sync_cursor_for_app_state()


def quit_game():
    try:
        glutLeaveMainLoop()
    except Exception:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

def mouseMotion(x,y):
    global main_menu_selection,menu_selection_index,how_to_back_hover,shop_selection_index
    global failed_selection_index,completed_selection_index
    hx,hy=hud_mouse_coordinates(x,y)
    if app_state==APP_MAIN_MENU:
        if 385<=hy<=435: main_menu_selection=0
        elif 323<=hy<373: main_menu_selection=1
        elif 261<=hy<311: main_menu_selection=2
        elif 199<=hy<249: main_menu_selection=3
    elif app_state==APP_PAUSED:
        pause_rows=((470,530),(410,470),(350,410),(290,350),(230,290),(170,230))
        for index,(lower,upper) in enumerate(pause_rows):
            if lower <= hy < upper:
                menu_selection_index=index
                break
    elif app_state==APP_SHOP:
        shop_selection_index=-1
        shop_rows=((525,575),(475,525),(425,475),(375,425))
        for index,(lower,upper) in enumerate(shop_rows):
            if lower <= hy < upper:
                shop_selection_index=index
                break
    elif app_state==APP_HOW_TO_PLAY:
        how_to_back_hover=90 <= hy <= 135
    elif app_state==APP_FAILED:
        if 435<=hy<=485: failed_selection_index=0
        elif 375<=hy<425: failed_selection_index=1
    elif app_state==APP_COMPLETED:
        if 425<=hy<=475: completed_selection_index=0
        elif 375<=hy<425: completed_selection_index=1

    glutPostRedisplay()


def restart_game():
    """Completely restart the game from Level 1."""
    global current_room, coins, level_start_coins
    global spell_charges, magic_window_duration, MAX_GHOSTS
    global level1_rewarded, level2_rewarded, final_rewarded
    global game_complete, game_running, app_state
    global level_completion_rewarded, button_rewarded
    global level_start_button_rewarded, level_start_completion_rewarded
    global main_menu_selection, menu_selection_index
    global torch_charge, torch_on
    global player_lives, player_health
    global failed_selection_index, completed_selection_index

    current_room = 1

    # Reset progression/currency to the starting state.
    coins = STARTING_COINS
    level_start_coins = STARTING_COINS
    spell_charges = BASE_SPELL_CHARGES
    magic_window_duration = BASE_MAGIC_WINDOW
    MAX_GHOSTS = 3

    level1_rewarded = False
    level2_rewarded = False
    final_rewarded = False
    game_complete = False

    level_completion_rewarded = set()
    button_rewarded = set()
    level_start_completion_rewarded = set()
    level_start_button_rewarded = set()

    main_menu_selection = 0
    menu_selection_index = 0
    failed_selection_index = 0
    completed_selection_index = 0
    player_lives = MAX_PLAYER_LIVES
    player_health = PLAYER_MAX_HEALTH

    app_state = APP_PLAYING
    game_running = True

    checkpoint_level_start()
    reset_room()

    sync_cursor_for_app_state()
    glutPostRedisplay()

# Reset

def reset_room():
    global player_x
    global player_y
    global player_rotation
    global room_message
    global game_running
    global shadow_hit_count
    global shadow_message
    global shadow_distance
    global shadow_active
    global shadow_rotation
    global shadow_y
    global shadow_x
    global hazard_message
    global spike_active
    global rift_active
    global torch_charge
    global torch_on
    global torch_message, app_state, level_failed_message, game_complete
    global collectible_coins, collected_coin_ids
    global hazard_hit_cooldown

    restore_level_start_coins()
    level_failed_message=''; game_complete=False
    hazard_hit_cooldown = 0.0
    if current_room == 1 or current_room == 2:
        player_x = -350
        player_y = 0
    else:
        player_x = 0
        player_y = -340
    player_rotation = 0
    game_running = True

    reset_time_system()
    reset_ghost_system()
    reset_puzzle()
    reset_level1()
    reset_level2()
    reset_shadow()
    reset_final_level()
    reset_closing_walls()
    reset_victory()
    spawn_collectible_coins()

    start_level_with_torch_on()
    rift_active = True
    spike_active = True
    hazard_message = "Watch for rifts and spikes."

    if current_room == 1:
        room_message = "Room 1 reset. Use a Ghost to hold Button A."
    elif current_room == 2:
        room_message = "Room 2 reset. Two Ghosts are required."
    else:
        room_message = "Final room reset. Start with Wall 1 and Ghost 1."

# Third-person camera

def setupCamera():
    global camera_pos
    aspect=1000.0/800.0
    cx=player_x
    cy=player_y-1100
    cz=1000
    camera_pos=(cx,cy,cz)
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(68,aspect,.1,2200)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    gluLookAt(cx,cy,cz,player_x,player_y,70,0,0,1)

# Update loop

def idle():
    global room_message, ghost_message, puzzle_message, level1_message, level2_message
    global torch_message, hazard_message, shadow_message, wall_message, shop_message, victory_message
    global transient_queue, important_queue, last_messages
    global app_state

    if app_state == APP_PLAYING:
        update_time_system(SIMULATION_STEP)
        update_recording(SIMULATION_STEP)
        update_ghosts(SIMULATION_STEP)
        update_puzzle_state()
        update_torch()
        update_collectible_coins()
        update_level1()
        update_level2()
        update_hazards()
        update_shadow()
        update_final_level()
        update_closing_walls()
        update_victory()

    # Message queue processing
    current_msgs = {
        "room": room_message,
        "ghost": ghost_message,
        "puzzle": puzzle_message,
        "level1": level1_message,
        "level2": level2_message,
        "torch": torch_message,
        "hazard": hazard_message,
        "shadow": shadow_message,
        "wall": wall_message,
        "shop": shop_message
    }
    
    for key, msg in current_msgs.items():
        if msg != last_messages.get(key, "") and msg != "":
            color = (1.0, 1.0, 1.0, 1.0)
            msg_lower = msg.lower()
            if key in ["hazard", "shadow", "wall"] or "empty" in msg_lower or "caught" in msg_lower or "closing" in msg_lower or "out" in msg_lower:
                color = (1.0, 0.3, 0.2, 1.0) 
            elif "complete" in msg_lower or "open" in msg_lower or "created" in msg_lower or "refilled" in msg_lower or "resumed" in msg_lower or "survived" in msg_lower:
                color = (0.3, 1.0, 0.3, 1.0) 
                
            transient_queue.append({"text": msg, "timer": 8.0, "color": color})
            last_messages[key] = msg
            
    if victory_message != last_messages.get("victory", "") and victory_message != "":
        important_queue.append({"text": victory_message, "timer": 10.0, "color": (1.0, 0.84, 0.0, 1.0)})
        last_messages["victory"] = victory_message
        
    for q in transient_queue:
        q["timer"] -= SIMULATION_STEP
    for q in important_queue:
        q["timer"] -= SIMULATION_STEP
        
    transient_queue = [q for q in transient_queue if q["timer"] > 0]
    important_queue = [q for q in important_queue if q["timer"] > 0]

    glutPostRedisplay()

# Main rendering function

def overlay(alpha):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(0,1000,0,800)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glColor3f(0,0,0); glBegin(GL_QUADS)
    glVertex2f(0,0);glVertex2f(1000,0);glVertex2f(1000,800);glVertex2f(0,800);glEnd()
    glPopMatrix();glMatrixMode(GL_PROJECTION);glPopMatrix();glMatrixMode(GL_MODELVIEW);glEnable(GL_DEPTH_TEST)

def draw_hud_circle(cx, cy, radius, color, segments=56):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glVertex2f(cx-radius, cy-radius)
    glVertex2f(cx+radius, cy-radius)
    glVertex2f(cx+radius, cy+radius)
    glVertex2f(cx-radius, cy+radius)
    glEnd()

def draw_hud_ring(cx, cy, radius, color, segments=72):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_LINES)
    glVertex2f(cx-radius, cy-radius); glVertex2f(cx+radius, cy-radius)
    glVertex2f(cx+radius, cy-radius); glVertex2f(cx+radius, cy+radius)
    glVertex2f(cx+radius, cy+radius); glVertex2f(cx-radius, cy+radius)
    glVertex2f(cx-radius, cy+radius); glVertex2f(cx-radius, cy-radius)
    glEnd()

def minimap_world_to_radar(world_x, world_y, cx, cy):
    dx = world_x - player_x
    dy = world_y - player_y
    scale = (MINIMAP_RADIUS - 15) / MINIMAP_SCAN_RADIUS
    rx = dx * scale
    ry = dy * scale
    distance = math.sqrt(rx * rx + ry * ry)
    max_distance = MINIMAP_RADIUS - 17

    if distance > max_distance and distance > 0:
        rx = rx / distance * max_distance
        ry = ry / distance * max_distance

    return cx + rx, cy + ry

def draw_minimap_dot(world_x, world_y, color, radius=MINIMAP_DOT_RADIUS):
    cx = 1000 - MINIMAP_RADIUS - MINIMAP_MARGIN
    cy = MINIMAP_RADIUS + MINIMAP_MARGIN
    hud_x, hud_y = minimap_world_to_radar(world_x, world_y, cx, cy)

    draw_hud_circle(hud_x, hud_y, radius + 2,(0.0, 0.0, 0.0, 0.34), 20)
    draw_hud_circle(hud_x, hud_y, radius, color, 20)

def draw_minimap_player(cx, cy):
    angle = math.radians(player_rotation + 90)
    forward_x = math.cos(angle)
    forward_y = math.sin(angle)
    side_x = math.cos(angle + math.pi / 2)
    side_y = math.sin(angle + math.pi / 2)

    nose_x = cx + forward_x * 12
    nose_y = cy + forward_y * 12
    left_x = cx - forward_x * 8 + side_x * 7
    left_y = cy - forward_y * 8 + side_y * 7
    right_x = cx - forward_x * 8 - side_x * 7
    right_y = cy - forward_y * 8 - side_y * 7

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(nose_x + 1, nose_y - 1)
    glVertex2f(left_x + 1, left_y - 1)
    glVertex2f(right_x + 1, right_y - 1)
    glEnd()

    glColor3f(0.92, 0.96, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(nose_x, nose_y)
    glVertex2f(left_x, left_y)
    glVertex2f(right_x, right_y)
    glEnd()

def draw_minimap_torch(cx, cy):
    charge_ratio = max(0.0, min(1.0, torch_charge / TORCH_MAX_CHARGE))
    icon_x = cx - 33
    icon_y = cy - MINIMAP_RADIUS + 16
    flame_color = (1.0, 0.74, 0.18, 1.0) if torch_on else (0.95, 0.18, 0.14, 1.0)
    text_color = (0.88, 0.90, 0.92, 0.92) if torch_on else (0.95, 0.48, 0.42, 0.95)

    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(icon_x - 3, icon_y - 5)
    glVertex2f(icon_x + 50, icon_y - 5)
    glVertex2f(icon_x + 50, icon_y + 7)
    glVertex2f(icon_x - 3, icon_y + 7)
    glEnd()

    draw_hud_circle(icon_x, icon_y + 1, 5, flame_color, 18)
    glColor3f(0.34, 0.25, 0.16)
    glBegin(GL_QUADS)
    glVertex2f(icon_x - 2, icon_y - 10)
    glVertex2f(icon_x + 2, icon_y - 10)
    glVertex2f(icon_x + 2, icon_y)
    glVertex2f(icon_x - 2, icon_y)
    glEnd()

    glColor3f(0.24, 0.25, 0.27)
    glBegin(GL_QUADS)
    glVertex2f(icon_x + 12, icon_y - 3)
    glVertex2f(icon_x + 44, icon_y - 3)
    glVertex2f(icon_x + 44, icon_y + 3)
    glVertex2f(icon_x + 12, icon_y + 3)
    glEnd()

    glColor3f(flame_color[0], flame_color[1], flame_color[2])
    glBegin(GL_QUADS)
    glVertex2f(icon_x + 12, icon_y - 3)
    glVertex2f(icon_x + 12 + 32 * charge_ratio, icon_y - 3)
    glVertex2f(icon_x + 12 + 32 * charge_ratio, icon_y + 3)
    glVertex2f(icon_x + 12, icon_y + 3)
    glEnd()

    return text_color

def get_minimap_buttons():
    if current_room == 1:
        return [(button_a_x, button_a_y), (button_b_x, button_b_y)]
    if current_room == 2:
        return [(level2_button_a_x, level2_button_a_y),(level2_button_b_x, level2_button_b_y)]
    return [(final_button_1_x, final_button_1_y),(final_button_2_x, final_button_2_y),(final_button_3_x, final_button_3_y)]

def get_minimap_door():
    if current_room == 1:
        return door_x, door_y
    if current_room == 2:
        return level2_door_x, level2_door_y
    return portal_x, portal_y

def draw_minimap():
    cx = 1000 - MINIMAP_RADIUS - MINIMAP_MARGIN
    cy = MINIMAP_RADIUS + MINIMAP_MARGIN

    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    draw_hud_circle(cx, cy - 2, MINIMAP_RADIUS + 5,(0.0, 0.0, 0.0, 0.34), 64)
    draw_hud_circle(cx, cy, MINIMAP_RADIUS,(0.025, 0.032, 0.045, 0.86), 72)
    draw_hud_circle(cx, cy, MINIMAP_RADIUS - 7,(0.05, 0.065, 0.085, 0.64), 72)

    glLineWidth(1)
    draw_hud_ring(cx, cy, MINIMAP_RADIUS - 28,(0.62, 0.70, 0.78, 0.16), 56)
    draw_hud_ring(cx, cy, MINIMAP_RADIUS - 8,(0.62, 0.70, 0.78, 0.20), 72)

    glColor3f(0.78, 0.84, 0.88)
    glLineWidth(2)
    glBegin(GL_LINES)
    for i in range(8):
        angle = math.pi * 2 * i / 8
        inner = MINIMAP_RADIUS - (15 if i % 2 == 0 else 10)
        outer = MINIMAP_RADIUS - 5
        glVertex2f(cx + math.cos(angle) * inner,cy + math.sin(angle) * inner)
        glVertex2f(cx + math.cos(angle) * outer,cy + math.sin(angle) * outer)
    glEnd()

    for bx, by in get_minimap_buttons():
        draw_minimap_dot(bx, by, (1.0, 0.16, 0.12, 0.95), 5)

    door_pos = get_minimap_door()
    draw_minimap_dot(door_pos[0], door_pos[1], (0.15, 1.0, 0.28, 0.95), 5)

    if current_room >= 2 and shadow_active:
        draw_minimap_dot(shadow_x, shadow_y, (0.15, 0.50, 1.0, 0.95), 5)

    draw_minimap_player(cx, cy)
    torch_text_color = draw_minimap_torch(cx, cy)

    glLineWidth(2)
    draw_hud_ring(cx, cy, MINIMAP_RADIUS,(0.86, 0.90, 0.94, 0.72), 80)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_DEPTH_TEST)
    draw_text(cx - 24, cy + MINIMAP_RADIUS + 10, "ROOM " + str(current_room),font=GLUT_BITMAP_HELVETICA_18,color=(0.86, 0.90, 0.94, 0.92),shadow=True)
    draw_text(cx + 20, cy - MINIMAP_RADIUS + 10,"ON" if torch_on else "OFF",font=GLUT_BITMAP_HELVETICA_18,color=torch_text_color,shadow=True)
    glEnable(GL_DEPTH_TEST)

def showScreen():
    sync_cursor_for_app_state()
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    if app_state in (APP_MAIN_MENU,APP_COMPLETED,APP_FAILED):
        overlay(.9); glDisable(GL_DEPTH_TEST)
        if app_state==APP_MAIN_MENU:
            draw_text(315,610,"YESTERDAY'S SHADOW",font=GLUT_BITMAP_HELVETICA_18,color=(1,.84,.1,1))
            for i,t in enumerate(["Play","How to Play","Controls","Exit Game"]):
                c=(1,.84,.1,1) if i==main_menu_selection else (.85,.85,.85,1)
                draw_text(385,410-i*62,("> " if i==main_menu_selection else "  ")+t,font=GLUT_BITMAP_HELVETICA_18,color=c)
            draw_text(315,120,"W/S or Arrow Keys - Enter - Mouse",font=GLUT_BITMAP_HELVETICA_18,color=(.9,.9,.9,1))
        elif app_state==APP_FAILED:
            draw_text(400,520,"Game Over",font=GLUT_BITMAP_HELVETICA_18,color=(1,.25,.2,1))
            for i,t in enumerate(["Play Again","Main Menu"]):
                c=(1,.84,.1,1) if i==failed_selection_index else (.85,.85,.85,1)
                draw_text(390 if i==failed_selection_index else 410,460-i*60,
                          ("> " if i==failed_selection_index else "")+t,
                          font=GLUT_BITMAP_HELVETICA_18,color=c)
        else:
            draw_text(300,520,"Congratulations! You Have Completed All Levels",font=GLUT_BITMAP_HELVETICA_18,color=(1,.84,.1,1))
            for i,t in enumerate(["Play Again","Exit"]):
                c=(1,.84,.1,1) if i==completed_selection_index else (.85,.85,.85,1)
                draw_text(410 if i==completed_selection_index else 430,450-i*50,
                          ("> " if i==completed_selection_index else "")+t,
                          font=GLUT_BITMAP_HELVETICA_18,color=c)
        glEnable(GL_DEPTH_TEST);glutSwapBuffers();return
    glViewport(0,0,1000,800)
    setupCamera()
    draw_floor();draw_room_walls();draw_room_decorations();draw_puzzle_objects();draw_level2_objects()
    draw_hazards();draw_final_level_objects();draw_closing_walls();draw_collectible_coins();draw_shadow()
    for g in ghosts: draw_ghost(g)
    draw_player()
    glDisable(GL_DEPTH_TEST)
    draw_text(20,770,"YESTERDAY'S SHADOW",font=GLUT_BITMAP_HELVETICA_18,color=(1,.84,0,1))
    draw_text(20,745,f"Level {current_room} | Lives: {player_lives} | Health: {player_health}% | Spells: {spell_charges} | Coins: {coins}",font=GLUT_BITMAP_HELVETICA_18)
    timer=f"MAGIC WINDOW  {magic_window_remaining:04.1f}s" if game_state==GAME_MAGIC_WINDOW else f"LEVEL TIMER  {room_time_remaining:04.1f}s"
    draw_text(740,770,timer,font=GLUT_BITMAP_HELVETICA_18,color=(1,.78,.12,1) if game_state==GAME_MAGIC_WINDOW else (.45,.85,1,1))
    draw_text(20,710,f"Torch: {int(torch_charge)}% [{'ON' if torch_on else 'OFF'}]",font=GLUT_BITMAP_HELVETICA_18,color=(1,.75,.25,1) if torch_on else (1,.3,.25,1))
    if current_room in (2,3): draw_text(20,660,"Shadow detects/follows you ONLY while Torch is ON.",font=GLUT_BITMAP_HELVETICA_18,color=(.5,1,.55,1) if torch_on else (1,.4,.3,1))
    if not torch_on: draw_torch_darkness()
    if app_state==APP_PAUSED:
        overlay(.78);draw_text(430,610,"PAUSED",font=GLUT_BITMAP_HELVETICA_18)
        for i,t in enumerate(["Resume","Restart Level","Restart Game","Shop","How to Play","Quit"]):
            c=(1,.84,.1,1) if i==menu_selection_index else (.75,.75,.75,1)
            draw_text(390 if i==menu_selection_index else 410,500-i*60,("> " if i==menu_selection_index else "")+t,font=GLUT_BITMAP_HELVETICA_18,color=c)
    elif app_state==APP_SHOP:
        overlay(.78);draw_text(420,620,"SHOP",font=GLUT_BITMAP_HELVETICA_18,color=(1,.84,.1,1))
        for i,t in enumerate(["1  Spell Charge       6 coins","2  Magic Window      8 coins","3  Torch Recharge     8 coins","4  Ghost Slot        12 coins"]):
            color=(1,.84,.1,1) if i==shop_selection_index else (1,1,1,1)
            draw_text(350,550-i*50,t,font=GLUT_BITMAP_HELVETICA_18,color=color)
        draw_text(350,320,f"Coins: {coins}",font=GLUT_BITMAP_HELVETICA_18,color=(1,.84,.1,1))
        draw_text(300,250,"ESC / Backspace: Back",font=GLUT_BITMAP_HELVETICA_18)
    elif app_state==APP_HOW_TO_PLAY:
        overlay(.82)
        draw_text(365,665,"HOW TO PLAY",font=GLUT_BITMAP_HELVETICA_18,color=(1,.84,.1,1))
        draw_text(145,610,"GOAL",font=GLUT_BITMAP_HELVETICA_18,color=(.45,.85,1,1))
        for i,t in enumerate(["Use Ghosts to hold buttons and open each exit.",
                              "Coins are collected while the torch is ON.",
                              "The Shadow follows only when the torch is ON in Levels 2 and 3.",
                              "Final room: leave Ghosts on all three buttons, then escape."]):
            draw_text(145,570-i*34,t,font=GLUT_BITMAP_HELVETICA_18,color=(.96,.96,.96,1))
        draw_text(145,410,"CONTROLS",font=GLUT_BITMAP_HELVETICA_18,color=(.45,.85,1,1))
        for i,t in enumerate(["WASD / Arrow Keys : Move",
                              "F : Record Ghost",
                              "T : Toggle Torch",
                              "K : Shop",
                              "R : Restart Level",
                              "ESC / Backspace : Back or Pause"]):
            draw_text(145,370-i*31,t,font=GLUT_BITMAP_HELVETICA_18,color=(.96,.96,.96,1))
        color=(1,.84,.1,1) if how_to_back_hover else (1,1,1,1)
        draw_text(380,105,"CLICK HERE TO GO BACK",font=GLUT_BITMAP_HELVETICA_18,color=color)
    draw_minimap()
    glEnable(GL_DEPTH_TEST);glutSwapBuffers()

# Main

def main():
    glutInit()

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)

    wind = glutCreateWindow(b"Yesterday's Shadow")

    glEnable(GL_DEPTH_TEST)

    reset_time_system()
    spawn_collectible_coins()
    sync_cursor_for_app_state()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutPassiveMotionFunc(mouseMotion)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
    