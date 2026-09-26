import pygame
import math
import random


# -- CONFIGURATION --
GAME_WIDTH = 1000
GAME_HEIGHT = 750

MAP_PIXEL_SIZE = 30

TREE_WIDTH = MAP_PIXEL_SIZE * 2
TREE_HEIGHT = MAP_PIXEL_SIZE * 3

player_x = 500.0
player_y = 300.0

player_size = 50
player_radius = player_size / 2

# Normal speed
player_speed = 300.0  # pixels / seconde

# Gravity
gravity = 1000.0      # pixels / seconde²
jump_strength = 600.0
on_ground = False

# Physical speed of player
velocity_x = 0.0
velocity_y = 0.0

# Boost
boost_strength = 700.0
boost_cooldown = 0.0
BOOST_COOLDOWN_TIME = 1.0

# Tool / Weapon
tool_distance = 50
tool_radius = player_size / 5

# MAP
map_data = []


tree_positions = []
# Function to generate trees positionns
def generate_trees(start_x, end_x, number_of_trees, ground_y):
    tree_positions = []

    width = end_x - start_x + 1
    zone_size = width / number_of_trees

    for i in range(number_of_trees):
        zone_start = start_x + i * zone_size
        zone_end = start_x + (i + 1) * zone_size

        tree_x = random.uniform(zone_start, zone_end)

        tree_positions.append(
            (tree_x, ground_y)
        )

    return tree_positions

tree_positions = generate_trees(
    0,
    35,
    3,
    20
)

def mp(x, y):
    map_data.append((x, y))


def draw_rect(x1, y1, x2, y2):
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            mp(x, y)


# Ground ?
draw_rect(0, 20, 35, 30)


# -- PYGAME --
pygame.init()

screen_size = (GAME_WIDTH, GAME_HEIGHT)

screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Game")

clock = pygame.time.Clock()


# -- IMAGES --
background = pygame.image.load(
    "just-filip-6Q0csNrm_Bk-unsplash.jpg"
).convert_alpha()

background = pygame.transform.scale(
    background,
    screen_size
)

dirt_image = pygame.image.load(
    "blueground.png"
).convert_alpha()

dirt_image = pygame.transform.scale(
    dirt_image,
    (MAP_PIXEL_SIZE, MAP_PIXEL_SIZE)
)

grass_image = pygame.image.load(
    "sprite_Grimm_Grass0.png"
).convert_alpha()

grass_image = pygame.transform.scale(
    grass_image,
    (MAP_PIXEL_SIZE, MAP_PIXEL_SIZE)
)

tree_image = pygame.image.load(
    "tree_light.png"
).convert_alpha()

tree_image = pygame.transform.scale(
    tree_image,
    (TREE_WIDTH, TREE_HEIGHT)
)

player_image = pygame.image.load(
    "character1_pygame.png"
).convert_alpha()

player_image = pygame.transform.scale(
    player_image,
    (player_size, player_size)
)

# -- GAME SOUNDS --
# Load start sound
start_sound_1 = pygame.mixer.Sound('sounds/song.wav') 

# Play start sound
start_sound_1.play()
pygame.mixer.music.fadeout(5000)

# Moving left and right sound
left_right_sound = pygame.mixer.Sound('sounds/power_up_1.wav') 

# Moving up and down sound
up_down_sound = pygame.mixer.Sound('sounds/power_up_3.wav') 

# -- GAME LOOP --
running = True

while running:
    # Time passed before the last frame
    dt = clock.tick(60) / 1000.0
    # Security
    dt = min(dt, 0.05)

    # -- EVENTS --
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and on_ground:
                velocity_y = -jump_strength
                on_ground = False

        if event.type == pygame.QUIT:
            running = False

        # -- BOOST --
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and boost_cooldown <= 0
        ):
            # Player direction via mouse
            mouse_x, mouse_y = pygame.mouse.get_pos()

            screen_center_x = GAME_WIDTH / 2
            screen_center_y = GAME_HEIGHT / 2

            direction_x = mouse_x - screen_center_x
            direction_y = mouse_y - screen_center_y

            distance = math.hypot(
                direction_x,
                direction_y
            )
            # Security for 0 division
            if distance > 0:
                # Normalisation
                direction_x /= distance
                direction_y /= distance
                # Propulsion dans la direction opposée
                velocity_x = -direction_x * boost_strength
                velocity_y = -direction_y * boost_strength
                # Reset du cooldown
                boost_cooldown = BOOST_COOLDOWN_TIME

    # -- INPUT --
    keys = pygame.key.get_pressed()

    # -- MOVEMENT --
    move_x = 0
    move_y = 0


    if keys[pygame.K_a]:
        move_x -= 1
        left_right_sound.play()

    if keys[pygame.K_d]:
        move_x += 1
        left_right_sound.play()

    if keys[pygame.K_w]:
            move_y -= 1
            up_down_sound.play()

    if keys[pygame.K_s]:
            move_y += 1
            up_down_sound.play()

    # Normalisation of keyboard mouvements
    # to avoid that the diagonal is faster
    if move_x != 0 or move_y != 0:

        length = math.hypot(move_x, move_y)

        move_x /= length
        move_y /= length

    player_x += move_x * player_speed * dt

    # -- PHYSICS --
    
    # Gravity
    velocity_y += gravity * dt
    # Apply of the physical speed
    player_x += velocity_x * dt
    player_y += velocity_y * dt

    # Ground collision
    ground_y = 20 * MAP_PIXEL_SIZE

    if player_y + player_radius >= ground_y:

        player_y = ground_y - player_radius

        velocity_y = 0

        on_ground = True

    else:
        on_ground = False

    # -- BOOST FRICTION --

    # The boost slower with time
    friction = 4.0

    velocity_x *= max(0.0, 1.0 - friction * dt)
    velocity_y *= max(0.0, 1.0 - friction * dt)

    # -- BOOST COOLDOWN --
    if boost_cooldown > 0:
        boost_cooldown -= dt

        if boost_cooldown < 0:
            boost_cooldown = 0

    # -- CAMERA --
    view_offset_x = player_x - GAME_WIDTH / 2
    view_offset_y = player_y - GAME_HEIGHT / 2

    # -- DRAW BACKGROUND --
    screen.blit(background, (0, 0))

    # -- DRAW MAP --
    for map_position in map_data:
        map_x, map_y = map_position

        pixel_position_x = map_x * MAP_PIXEL_SIZE - view_offset_x
        pixel_position_y = map_y * MAP_PIXEL_SIZE - view_offset_y

        if map_y == 20:
            screen.blit(
                grass_image,
                (pixel_position_x, pixel_position_y)
            )
        else:
            screen.blit(
                dirt_image,
                (pixel_position_x, pixel_position_y)
            )

    for tree_x, tree_y in tree_positions:

        pixel_position_x = (
            tree_x * MAP_PIXEL_SIZE
            - view_offset_x
            - TREE_WIDTH / 2
        )

        pixel_position_y = (
            tree_y * MAP_PIXEL_SIZE
            - view_offset_y
            - TREE_HEIGHT
        )

        screen.blit(
            tree_image,
            (pixel_position_x, pixel_position_y)
        )        

    # -- PLAYER --
    player_screen_x = (
        GAME_WIDTH / 2
        - player_size / 2
    )

    player_screen_y = (
        GAME_HEIGHT / 2
        - player_size / 2
    )

    screen.blit(
        player_image,
        (
            player_screen_x,
            player_screen_y
        )
    )

    # -- TOOL / WEAPON --
    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen_center_x = GAME_WIDTH / 2
    screen_center_y = GAME_HEIGHT / 2

    direction_x = mouse_x - screen_center_x
    direction_y = mouse_y - screen_center_y

    distance = math.hypot(
        direction_x,
        direction_y
    )

    if distance > 0:

        direction_x /= distance
        direction_y /= distance

    else:

        direction_x = 0
        direction_y = 0


    tool_coord_x = (
        screen_center_x
        + direction_x * tool_distance
    )

    tool_coord_y = (
        screen_center_y
        + direction_y * tool_distance
    )

    pygame.draw.circle(
        screen,
        "white",
        (
            tool_coord_x,
            tool_coord_y
        ),
        tool_radius
    )

    # -- DEBUG INFORMATION --
    font = pygame.font.Font(None, 30)

    boost_text = font.render(
        f"Boost: {boost_cooldown:.2f}s",
        True,
        "white"
    )

    velocity_text = font.render(
        f"Velocity: {velocity_x:.0f}, {velocity_y:.0f}",
        True,
        "white"
    )

    position_text = font.render(
        f"Position: {player_x:.1f}, {player_y:.1f}",
        True,
        "white"
    )

    screen.blit(boost_text, (20, 20))
    screen.blit(velocity_text, (20, 50))
    screen.blit(position_text, (20, 80))

    # -- DISPLAY --
    pygame.display.flip()


pygame.quit()
