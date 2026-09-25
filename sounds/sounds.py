import pygame

pygame.init()

# Game window in pixels
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = pygame.Rect((300, 250, 50, 50))

# Load start sound
start_sound_1 = pygame.mixer.Sound('song.wav') 

# Play start sound
start_sound_1.play()

# Time delay option in miliseconds
pygame.time.delay(3000)
start_sound_1.play()

# Set sound volume (value between 0 and 1, e.g. .3 is quieter than 1)
start_sound_1.set_volume(.3)

# Game loop
run = True
while run:

    screen.fill((0, 0, 0))

    # Rectangle
    pygame.draw.rect(screen, (255, 0, 0), player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_d] == True:
            player.move_ip(1, 0)
    elif key[pygame.K_w] == True:
                player.move_ip(0, -1)
    elif key[pygame.K_s] == True:
                    player.move_ip(0, 1)

    # Event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()