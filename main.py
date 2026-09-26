import pygame

screen_size = (1000,750)

player_x = 500
player_y = 300
player_size = 50
tool_radius = player_size/5
tool_distance = 50
player_momentum_x = 0
player_momentum_y = 0
boost_cooldown = -0.1
player_speed = 1

view_offset_x = player_x - (screen_size[0] / 2)
view_offset_y = player_y - (screen_size[1] / 2)

#today i learned a path and surface are not the same :/
idle_player_path = "tiles/character1_pygame.png"

#this is the map data, write a pixel onto the screen by puting its position in mp(x,y)
map_pixel_size = 30
map_data = []

def mp(x, y, sprite_tile="tiles/blueground.png"):
    map_data.append((x, y, sprite_tile))




def draw_rect(x1, y1, x2, y2, mp, sprite_tile="tiles/blueground.png"):
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            mp(x, y, sprite_tile)
            
draw_rect(0, 20, 35, 30, mp, "dirt")
draw_rect(0, 19, 35, 19, mp, "grass_short")

#this is for tiles with no collision
map_data_nc = []
def mp(x, y, sprite_tile="tiles/blueground.png"):
    map_data_nc.append((x, y, sprite_tile))

# grass-plant position
mp(0, 18, "grass-plant")
mp(1, 18, "grass-plant")
mp(2, 18, "grass-plant")
mp(3, 18, "grass-plant")
mp(4, 18, "grass-plant")

mp(2, 10, "grass-plant")
mp(3, 10, "grass-plant")
mp(4, 10, "grass-plant")
mp(5, 10, "grass-plant")
mp(6, 10, "grass-plant")

mp(18, 18, "grass-plant")
mp(19, 18, "grass-plant")
mp(20, 18, "grass-plant")
mp(21, 18, "grass-plant")
mp(22, 18, "grass-plant")
mp(23, 18, "grass-plant")
mp(24, 18, "grass-plant")
mp(25, 18, "grass-plant")


# plant-1 position
mp(30, 13, "plant-1")
mp(31, 13, "plant-1")
mp(32, 13, "plant-1")
mp(33, 13, "plant-1")
mp(34, 13, "plant-1")
mp(35, 13, "plant-1")
mp(36, 13, "plant-1")
mp(37, 13, "plant-1")

mp(53, 23, "plant-1")
mp(54, 23, "plant-1")
mp(55, 23, "plant-1")
mp(56, 23, "plant-1")
mp(57, 23, "plant-1")
mp(58, 23, "plant-1")
mp(59, 23, "plant-1")
mp(60, 23, "plant-1")

mp(73, 23, "plant-1")
mp(74, 23, "plant-1")
mp(75, 23, "plant-1")
mp(76, 23, "plant-1")
mp(77, 23, "plant-1")
mp(78, 23, "plant-1")
mp(79, 23, "plant-1")
mp(80, 23, "plant-1")




#mp(7, 18, "rosebush")
mp(8, 18, "flowers")
mp(9, 18, "flowers")
mp(10, 18, "flowers")
mp(11, 18, "flowers")
mp(12, 18, "flowers")
mp(13, 18, "flowers")
mp(14, 18, "flowers")
mp(15, 18, "flowers")
mp(42, 18, "flowers")
mp(43, 18, "flowers")
mp(44, 18, "flowers")
mp(45, 18, "flowers")
mp(46, 18, "flowers")
mp(47, 18, "flowers")
mp(48, 18, "flowers")
mp(49, 18, "flowers")
mp(63, 23, "flowers")
mp(64, 23, "flowers")
mp(65, 23, "flowers")
mp(66, 23, "flowers")
mp(67, 23, "flowers")
mp(68, 23, "flowers")
mp(69, 23, "flowers")
mp(70, 23, "flowers")

mp(83, 23, "flowers")
mp(84, 23, "flowers")
mp(85, 23, "flowers")
mp(86, 23, "flowers")
mp(87, 23, "flowers")
mp(88, 23, "flowers")
mp(89, 23, "flowers")
mp(90, 23, "flowers")
   
#mp(18, 18, "purple_fire")
#mp(25, 18, "willow-wisp")



#this is just the window that opens (the majority of the stuff should be in here)
pygame.init()
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("game")

background = pygame.image.load("tiles/zees-art/game-background.png").convert_alpha()
background = pygame.transform.scale(background, screen_size)
running = True

idle_player_image = pygame.image.load(idle_player_path).convert_alpha()
idle_player_image = pygame.transform.scale(idle_player_image, (player_size, player_size))


#this function was from a template on the web (cause idk how to do it)
walk_right_frames = []
for i in range(19):
    path = f"tiles/charactor1walkright/charactor1walkright_{i:02d}.png"
    frame = pygame.image.load(path).convert_alpha()
    frame = pygame.transform.scale(frame, (player_size, player_size))
    walk_right_frames.append(frame)

walk_left_frames = []
for i in range(20):
    path = f"tiles/charactor1walkleft/charactor1left_{i:02d}.png"
    frame = pygame.image.load(path).convert_alpha()
    frame = pygame.transform.scale(frame, (player_size, player_size))
    walk_left_frames.append(frame)


# -- GAME SOUNDS --
# Load start sound
start_sound_1 = pygame.mixer.Sound('sounds/mondamusic-retro-arcade-game-music-512837.mp3') 

# Play start sound
start_sound_1.play()
pygame.mixer.music.fadeout(1000)

# Moving left and right sound
left_right_sound = pygame.mixer.Sound('sounds/universfield-footsteps-walking-278819-cropped.mp3') 


# -- GAME LOOP --

#window running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    #screen.blit(background, (0, 0))

    #to make background move instead of player :p
    view_offset_x = player_x - (screen_size[0] / 2)
    view_offset_y = player_y - (screen_size[1] / 2)

    #mapdataload
    tile_images = {

        "dirt": pygame.image.load("tiles/sprite_Grimm_Dirt0.png").convert_alpha(),
        "grass_short": pygame.image.load("tiles/sprite_Grimm_Grass0.png").convert_alpha(),
        "grass_tall": pygame.image.load("tiles/sprite_Grimm_Grass_Tall0.png").convert_alpha(),
        "plant-1": pygame.image.load("tiles/plant-1.png").convert_alpha(),
        "flowers": pygame.image.load("tiles/flowers.png").convert_alpha(),
        "purple_fire": pygame.image.load("tiles/zees-art/purple_fire.png").convert_alpha(),
        "grass-plant": pygame.image.load("tiles/zees-art/grass-plant.png").convert_alpha(),
        "rosebush": pygame.image.load("tiles/rose_bush.png").convert_alpha(),
        #"willow-wisp": pygame.image.load("tiles/zees-art/willow-wisp.png").convert_alpha(),
    }

    for name, image in tile_images.items():
        tile_images[name] = pygame.transform.scale(image, (map_pixel_size, map_pixel_size))


    #this is the mapdata that has collision
    for x, y, sprite_tile in map_data:

        pixel_position_x = (x * map_pixel_size) - view_offset_x
        pixel_position_y = (y * map_pixel_size) - view_offset_y
        
        screen.blit(tile_images[sprite_tile], (pixel_position_x, pixel_position_y))

    #this is the mapdata that has no collision (hence the _nc)
    for x, y, sprite_tile in map_data_nc:

        pixel_position_x = (x * map_pixel_size) - view_offset_x
        pixel_position_y = (y * map_pixel_size) - view_offset_y
        
        screen.blit(tile_images[sprite_tile], (pixel_position_x, pixel_position_y))


    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    #the player

    

    #screen.blit(player_image, (player_x-(player_size/2), player_y-(player_size/2)))
    

    #wasd movement
    movement_right = False

    temp_x = player_y
    temp_y = player_y
    
    old_x = player_x
    #A
    if keys[pygame.K_a]:
        player_x -= player_speed
        frame = (pygame.time.get_ticks() // 25) % len(walk_left_frames)
        current_player_image = walk_left_frames[frame]
        left_right_sound.play()
    
    #D
    elif keys[pygame.K_d]:
        player_x += player_speed
        frame = (pygame.time.get_ticks() // 25) % len(walk_right_frames)
        current_player_image = walk_right_frames[frame]
        left_right_sound.play()

    for x, y, sprite_tile in map_data:
        tile_rect = pygame.Rect(x * map_pixel_size, y * map_pixel_size, map_pixel_size, map_pixel_size)
        player_rect = pygame.Rect(player_x - player_size / 2, player_y - player_size / 2, player_size, player_size)
        if player_rect.colliderect(tile_rect):
            player_x = old_x
            break

    old_y = player_y
    if keys[pygame.K_w]:
        player_y -= player_speed

    if keys[pygame.K_s]:
        player_y += player_speed

    #gravity
    if player_y < screen_size[1] - player_size: 
        player_y += 1

    for x, y, sprite_tile in map_data:
            tile_rect = pygame.Rect(x * map_pixel_size, y * map_pixel_size, map_pixel_size, map_pixel_size)
            player_rect = pygame.Rect(player_x - player_size / 2, player_y - player_size / 2, player_size, player_size)
            if player_rect.colliderect(tile_rect):
                player_y = old_y
                break

                
    
    else:
            current_player_image = idle_player_image
    screen.blit(current_player_image, ((screen_size[0] / 2)-player_size/2, (screen_size[1] / 2)-player_size/2))
        
    
    #this is to calulate where the tool visual is around the player
    distance_x = mouse_x-(screen_size[0] / 2)
    distance_y = mouse_y-(screen_size[1] / 2)
    distance_xy = (distance_x**2 + distance_y**2)**0.5

    #this keeps it from crashing if your mouse is at the exact center of player (not really likly but you can never be too sure ig)
    if distance_xy > 0:
        direction_x = distance_x / distance_xy
        direction_y = distance_y / distance_xy
    else:
        direction_x = 0
        direction_y = 0
    #final calulation 
    tool_coord_x = (screen_size[0] / 2) + direction_x*tool_distance
    tool_coord_y = (screen_size[1] / 2) + direction_y*tool_distance

    #draws the tool
    pygame.draw.circle(screen, "white", (tool_coord_x, tool_coord_y),tool_radius)

    ##boost (doent work btw :p)
    #for event in pygame.event.get():
    #   if event.type == pygame.MOUSEBUTTONDOWN and boost_cooldown <= 0:
    #       boost_cooldown = 100
    #       player_momentum_x = 3
    #       player_momentum_y = 3

    #player_x += ((((tool_coord_x-player_x)/10)*player_momentum_x)*-1)
    #player_y += ((((tool_coord_y-player_y)/10)*player_momentum_y)*-1)

    #if boost_cooldown > 0:
    #    boost_cooldown -= 1

    #if player_momentum_x > 0:
    #    #player_x += player_momentum_x
    #    player_momentum_x -= 0.01
    
    #if player_momentum_y > 0:
    #    #player_x += player_momentum_x
    #    player_momentum_y -= 0.05



#-------------------------------------------------------





#displaying info (dont mess)

    #this displays the direction of the boost/weapon
    font = pygame.font.Font(None, 50)
    text = font.render(f"{((tool_coord_x-player_x)/100)*-1},{((tool_coord_y-player_y)/100)*-1}", True,"white")
    screen.blit(text, (100,100))

    #this displays the boost cooldown
    font = pygame.font.Font(None, 50)
    text = font.render(f"{boost_cooldown}", True,"white")
    screen.blit(text, (300,300))
    
    pygame.display.flip()
pygame.quit()