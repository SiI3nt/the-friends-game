import pygame


screen_size = (1000,750)
player_x = 500
player_y = 300
#25
player_size = 25
tool_radius = player_size/2
tool_distance = 50
player_momentum_x = 0
player_momentum_y = 0
boost_cooldown = -0.1


#this is the map data, write a pixel onto the screen by puting its position in mp(x,y)
map_pixel_size = 5
map_data = []
def mp(x, y):
    map_data.append((x, y))

mp(100,100)

#window stuff
pygame.init()
screen = pygame.display.set_mode((screen_size))
pygame.display.set_caption("game")
running = True

#key/mouse inputs (obv)
keys = pygame.key.get_pressed()

#window running
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    #gravity ig
    if player_y < screen_size[1] - player_size: 
        player_y += 2


    for x, y in map_data:
        pygame.draw.rect(screen, "red", (x*map_pixel_size,y*map_pixel_size,map_pixel_size,map_pixel_size))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    

    pygame.draw.circle(screen, "white", (player_x,player_y),player_size)
    #pygame.draw.circle(screen, "white", (player_x+mouse_x*-1,player_y+mouse_y*-1),player_size/2)

    #this is to calulate where the tool visual is around the player
    #and they said algebra was useless :)
    distance_x = mouse_x-player_x
    distance_y = mouse_y-player_y
    distance_xy = (distance_x**2 + distance_y**2)**0.5

    #this keeps it from crashing if your mouse is at the exact center of player (not really likly but you can never be too sure ig)
    if distance_xy > 0:
        direction_x = distance_x / distance_xy
        direction_y = distance_y / distance_xy
    else:
        direction_x = 0
        direction_y = 0
    #final calulation f
    tool_coord_x = player_x + direction_x*tool_distance
    tool_coord_y = player_y + direction_y*tool_distance


    


    pygame.draw.circle(screen, "white", (tool_coord_x, tool_coord_y),tool_radius)


    #boost
    if pygame.mouse.get_pressed()[0] and boost_cooldown <= 0:

        boost_cooldown = 100

        player_momentum_x = 3
        player_momentum_y = 3


    if pygame.mouse.get_pressed()[0]:

        player_x += ((((tool_coord_x-player_x)/10)*player_momentum_x)*-1)
        player_y += ((((tool_coord_y-player_y)/10)*player_momentum_y)*-1)

    if boost_cooldown > 0:
        boost_cooldown -= 1

    if player_momentum_x > 0:
        #player_x += player_momentum_x
        player_momentum_x -= 0.01
    
    if player_momentum_y > 0:
        #player_x += player_momentum_x
        player_momentum_y -= 0.05


    font = pygame.font.Font(None, 50)
    text = font.render(f"{((tool_coord_x-player_x)/10)*-1},{((tool_coord_y-player_y)/10)*-1}", True,"white")
    screen.blit(text, (100,100))


    font = pygame.font.Font(None, 50)
    text = font.render(f"{boost_cooldown}", True,"white")
    screen.blit(text, (300,300))
    
    pygame.display.flip()
pygame.quit()




#debug lines, delete later 
    #font = pygame.font.Font(None, 50)
    #text = font.render(f"{mouse_x},{mouse_y}", True,"white")
    #screen.blit(text, (100,100))







    