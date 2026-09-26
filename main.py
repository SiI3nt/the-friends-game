import pygame
import math


# -- CONFIGURATION --
GAME_WIDTH = 1000
GAME_HEIGHT = 750

MAP_PIXEL_SIZE = 30

player_x = 500.0
player_y = 300.0

player_size = 50
player_radius = player_size / 2

# -- Movement --
player_speed = 300.0  # pixels / seconde

# -- Gravity / Jump --
gravity = 1000.0
jump_strength = 500.0
on_ground = False

# -- Physical velocity --
velocity_x = 0.0
velocity_y = 0.0

# -- Boost --
boost_strength = 700.0
boost_cooldown = 0.0
BOOST_COOLDOWN_TIME = 1.0

# -- Tool / Weapon --
tool_distance = 50
tool_radius = player_size / 5



# -- MAP --

# Map with collision
map_data = []

# Map sans collision
map_data_nc = []


def mp(x, y, sprite_tile="blueground"):
    """
    Ajoute une tuile à la map physique.
    """
    map_data.append((x, y, sprite_tile))


def mp_nc(x, y, sprite_tile):
    """
    Ajoute une tuile décorative sans collision.
    """
    map_data_nc.append((x, y, sprite_tile))


def draw_rect(x1, y1, x2, y2, sprite_tile="blueground"):
    """
    Crée un rectangle de tiles avec collision.
    """
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            mp(x, y, sprite_tile)


# -- Ground --

draw_rect(
    0,
    20,
    35,
    30,
    "dirt"
)

# -- Grass top --

draw_rect(
    0,
    19,
    35,
    19,
    "grass_short"
)


collision_tiles = {
    (x, y): sprite_tile
    for x, y, sprite_tile in map_data
}

def get_nearby_collision_tiles(player_x, player_y):
    player_tile_x = int(player_x // MAP_PIXEL_SIZE)
    player_tile_y = int(player_y // MAP_PIXEL_SIZE)


    for tile_x in range(
        player_tile_x - 2,
        player_tile_x + 3
    ):
        for tile_y in range(
            player_tile_y - 2,
            player_tile_y + 3
        ):

            sprite_tile = collision_tiles.get(
                (tile_x, tile_y)
            )

            if sprite_tile is not None:
                yield (
                    tile_x,
                    tile_y,
                    sprite_tile
                )


# -- NON-PHYSICAL DECORATION --
mp_nc(0, 18, "grass_tall")
mp_nc(1, 18, "plant-1")
mp_nc(5, 18, "rosebush")
mp_nc(7, 18, "flowers")
mp_nc(12, 18, "grass_tall")
mp_nc(14, 18, "grass_tall")



# -- PYGAME INITIALIZATION --
pygame.init()

screen_size = (GAME_WIDTH, GAME_HEIGHT)

screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Game")

clock = pygame.time.Clock()



# -- IMAGES --
background = pygame.image.load(
    "tiles/game-background.png"
).convert_alpha()

background = pygame.transform.scale(
    background,
    screen_size
)



# -- MAP TILES --
tile_images = {}

tile_paths = {
    "dirt": "tiles/sprite_Grimm_Dirt0.png",
    "grass_short": "tiles/sprite_Grimm_Grass0.png",
    "grass_tall": "tiles/sprite_Grimm_Grass_Tall0.png",
    "plant-1": "tiles/plant-1.png",
    "flowers": "tiles/flowers.png",
    "rosebush": "tiles/rose_bush.png",
}


for name, path in tile_paths.items():

    image = pygame.image.load(path).convert_alpha()

    image = pygame.transform.scale(
        image,
        (MAP_PIXEL_SIZE, MAP_PIXEL_SIZE)
    )

    tile_images[name] = image


# -- PLAYER IMAGES --
idle_player_path = "tiles/character1_pygame.png"

idle_player_image = pygame.image.load(
    idle_player_path
).convert_alpha()

idle_player_image = pygame.transform.scale(
    idle_player_image,
    (player_size, player_size)
)


# -- WALK RIGHT --
walk_right_frames = []

for i in range(19):

    path = (
        f"tiles/charactor1walkright/"
        f"charactor1walkright_{i:02d}.png"
    )

    frame = pygame.image.load(
        path
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (player_size, player_size)
    )

    walk_right_frames.append(frame)


# -- WALK LEFT --
walk_left_frames = []

for i in range(20):

    path = (
        f"tiles/charactor1walkleft/"
        f"charactor1left_{i:02d}.png"
    )

    frame = pygame.image.load(
        path
    ).convert_alpha()

    frame = pygame.transform.scale(
        frame,
        (player_size, player_size)
    )

    walk_left_frames.append(frame)



# -- GAME SOUNDS --

# Start sound
start_sound_1 = pygame.mixer.Sound(
    "sounds/mondamusic-retro-arcade-game-music-512837.mp3"
)

start_sound_1.play()

pygame.mixer.music.fadeout(1000)


# Movement sounds
left_right_sound = pygame.mixer.Sound(
    "sounds/power_up_1.wav"
)

up_down_sound = pygame.mixer.Sound(
    "sounds/power_up_3.wav"
)


# -- GAME LOOP --
running = True

while running:
    # -- TIME --
    dt = clock.tick(60) / 1000.0
    
    # Prevent huge physics jumps if the game freezes
    dt = min(dt, 0.05)
    # -- EVENTS --
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            running = False
   
        # Jump
        if event.type == pygame.KEYDOWN:

            if (
                event.key == pygame.K_SPACE
                and on_ground
            ):
                velocity_y = -jump_strength
                on_ground = False


        # Boost
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and boost_cooldown <= 0
        ):

            mouse_x, mouse_y = pygame.mouse.get_pos()

            screen_center_x = GAME_WIDTH / 2
            screen_center_y = GAME_HEIGHT / 2

            direction_x = (
                mouse_x - screen_center_x
            )

            direction_y = (
                mouse_y - screen_center_y
            )

            distance = math.hypot(
                direction_x,
                direction_y
            )

            if distance > 0:
                # Normalize direction
                direction_x /= distance
                direction_y /= distance

                # Propulsion opposite to weapon direction
                velocity_x = (
                    -direction_x
                    * boost_strength
                )

                velocity_y = (
                    -direction_y
                    * boost_strength
                )

                boost_cooldown = BOOST_COOLDOWN_TIME


    # -- INPUT --
    keys = pygame.key.get_pressed()

    # -- HORIZONTAL MOVEMENT --
    move_x = 0

    if keys[pygame.K_a]:
        move_x -= 1

    if keys[pygame.K_d]:
        move_x += 1

    # -- HORIZONTAL MOVEMENT --
    # To properly restore the position from the movement that just happened.
    old_x = player_x
    
    player_x += (
        move_x
        * player_speed
        * dt
    )

    # -- HORIZONTAL COLLISION --
    # We already moved player_x above.
    # If we collide, restore the previous position
    player_rect = pygame.Rect(
        player_x - player_size / 2,
        player_y - player_size / 2,
        player_size,
        player_size
    )

    for x, y, sprite_tile in get_nearby_collision_tiles(
        player_x,
        player_y
        ):

        tile_rect = pygame.Rect(
            x * MAP_PIXEL_SIZE,
            y * MAP_PIXEL_SIZE,
            MAP_PIXEL_SIZE,
            MAP_PIXEL_SIZE
        )

        if player_rect.colliderect(tile_rect):

            player_x = old_x

            break

    # -- PHYSICS --

    # Gravity
    if not on_ground:
        velocity_y += gravity * dt

    # VERTICAL MOVEMENT
    old_y = player_y

    player_y += velocity_y * dt

    # Player collision rectangle
    player_rect = pygame.Rect(
        player_x - player_size / 2,
        player_y - player_size / 2,
        player_size,
        player_size
    )

    # Assume we are not on the ground
    on_ground = False

    # VERTICAL COLLISION
    for x, y, sprite_tile in get_nearby_collision_tiles(
        player_x,
        player_y
    ):

        tile_rect = pygame.Rect(
            x * MAP_PIXEL_SIZE,
            y * MAP_PIXEL_SIZE,
            MAP_PIXEL_SIZE,
            MAP_PIXEL_SIZE
        )

        # No collision at all
        if not player_rect.colliderect(tile_rect):
            continue

        # Falling onto a tile
        if velocity_y > 0:

            old_bottom = (
                old_y
                + player_size / 2
            )

            # We were above the tile before moving
            if old_bottom <= tile_rect.top:

                player_y = (
                    tile_rect.top
                    - player_size / 2
                )

                velocity_y = 0

                on_ground = True

                break

        # Hitting the bottom of a tile
        elif velocity_y < 0:

            old_top = (
                old_y
                - player_size / 2
            )

            # We were below the tile before moving
            if old_top >= tile_rect.bottom:

                player_y = (
                    tile_rect.bottom
                    + player_size / 2
                )

                velocity_y = 0

                break

    # GROUND CHECK
    # We create a tiny rectangle just below the player's feet.
    ground_check = pygame.Rect(
        player_x - player_size / 2 + 1,
        player_y + player_size / 2,
        player_size - 2,
        2
    )


    for x, y, sprite_tile in get_nearby_collision_tiles(
        player_x,
        player_y
    ):

        tile_rect = pygame.Rect(
            x * MAP_PIXEL_SIZE,
            y * MAP_PIXEL_SIZE,
            MAP_PIXEL_SIZE,
            MAP_PIXEL_SIZE
        )

        if ground_check.colliderect(tile_rect):

            # Only count tiles that are underneath us
            if tile_rect.top >= player_y + player_size / 2 - 1:

                on_ground = True
                velocity_y = 0

                break    

    # -- BOOST FRICTION --
    friction = 4.0

    velocity_x *= max(
        0.0,
        1.0 - friction * dt
    )

    # -- BOOST COOLDOWN --
    if boost_cooldown > 0:

        boost_cooldown -= dt

        if boost_cooldown < 0:
            boost_cooldown = 0

    # -- CAMERA --
    view_offset_x = (
        player_x
        - GAME_WIDTH / 2
    )

    view_offset_y = (
        player_y
        - GAME_HEIGHT / 2
    )

    # -- BACKGROUND --
    screen.fill("black")
    
    screen.blit(
        background,
        (0, 0)
    )


    # -- MAP WITH COLLISION --
    for x, y, sprite_tile in map_data:

        pixel_position_x = (
            x * MAP_PIXEL_SIZE
            - view_offset_x
        )

        pixel_position_y = (
            y * MAP_PIXEL_SIZE
            - view_offset_y
        )

        screen.blit(
            tile_images[sprite_tile],
            (
                pixel_position_x,
                pixel_position_y
            )
        )

    # -- MAP WITHOUT COLLISION --
    for x, y, sprite_tile in map_data_nc:

        pixel_position_x = (
            x * MAP_PIXEL_SIZE
            - view_offset_x
        )

        pixel_position_y = (
            y * MAP_PIXEL_SIZE
            - view_offset_y
        )

        screen.blit(
            tile_images[sprite_tile],
            (
                pixel_position_x,
                pixel_position_y
            )
        )

    # -- PLAYER ANIMATION --
    if keys[pygame.K_a]:

        frame = (
            pygame.time.get_ticks() // 25
        ) % len(walk_left_frames)

        current_player_image = (
            walk_left_frames[frame]
        )

    elif keys[pygame.K_d]:

        frame = (
            pygame.time.get_ticks() // 25
        ) % len(walk_right_frames)

        current_player_image = (
            walk_right_frames[frame]
        )

    else:

        current_player_image = idle_player_image

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
        current_player_image,
        (
            player_screen_x,
            player_screen_y
        )
    )

    # -- TOOL / WEAPON --
    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen_center_x = GAME_WIDTH / 2
    screen_center_y = GAME_HEIGHT / 2

    direction_x = (
        mouse_x - screen_center_x
    )

    direction_y = (
        mouse_y - screen_center_y
    )

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
    font = pygame.font.Font(
        None,
        30
    )

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

    ground_text = font.render(
        f"Ground: {on_ground}",
        True,
        "white"
    )

    fps_text = font.render(
        f"FPS: {clock.get_fps():.0f}",
        True,
        "white"
    )

    screen.blit(
        boost_text,
        (20, 20)
    )

    screen.blit(
        velocity_text,
        (20, 50)
    )

    screen.blit(
        position_text,
        (20, 80)
    )

    screen.blit(
        ground_text,
        (20, 110)
    )

    screen.blit(
        fps_text,
        (20, 140)
    )

    # -- DISPLAY --
    pygame.display.flip()


pygame.quit()
