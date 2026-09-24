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


#this is the map data, write a pixel onto the screen by puting its position in mp(x,y)
map_pixel_size = 30
map_data = []
def mp(x, y):
    map_data.append((x, y))




def draw_rect(x1, y1, x2, y2, mp):
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            mp(x, y)
            
draw_rect(0, 20, 35, 30, mp)





#this is just the window that opens (the majority of the stuff should be in here)
pygame.init()
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("game")

background = pygame.image.load("Space Background.png").convert_alpha()
background = pygame.transform.scale(background, screen_size)
running = True

#window running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #screen.fill("black")

    screen.blit(background, (0, 0))

    #to make background move instead of player :p
    view_offset_x = player_x - (screen_size[0] / 2)
    view_offset_y = player_y - (screen_size[1] / 2)

    block_image = pygame.image.load("blueground.png").convert_alpha()
    block_image = pygame.transform.scale(block_image,(map_pixel_size, map_pixel_size))







    for mp in map_data:

        pixel_position_x = (mp[0] * map_pixel_size) - view_offset_x
        pixel_position_y = (mp[1] * map_pixel_size) - view_offset_y
        

        pygame.draw.rect(screen, "red", (pixel_position_x,pixel_position_y,map_pixel_size,map_pixel_size))
        screen.blit(block_image, (pixel_position_x, pixel_position_y))

    #for x1, y1, x2, y2 in map_data:



                
            #pygame.draw.rect(screen, "red", (x*map_pixel_size,y*map_pixel_size,map_pixel_size,map_pixel_size))
    

    #gravity
    if player_y < screen_size[1] - player_size: 
        player_y += 0

    mouse_x, mouse_y = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    #the player
    player_image = pygame.image.load("character1_pygame.png").convert_alpha()
    player_image = pygame.transform.scale(player_image,(player_size, player_size))

    #screen.blit(player_image, (player_x-(player_size/2), player_y-(player_size/2)))
    screen.blit(player_image, ((screen_size[0] / 2)-player_size/2, (screen_size[1] / 2)-player_size/2))
    

    #wasd movement
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_d]:
        player_x += player_speed
        
    
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

    ##boost
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