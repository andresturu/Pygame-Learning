import pygame
from sys import exit
from utils import load_and_scale_image, scale_by_width


pygame.init() #starts up the game, kind of like starting up the engine of the car

screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height)) #creates a display surface, stores it in a variable called 'screen'
pygame.display.set_caption('Runner') #changes name of game window
clock = pygame.time.Clock() 
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)


sky_surface = load_and_scale_image('graphics/background_sky.jpg', screen_width) #elegant way of creating a surface, and scaling it simultaneously using functions
ground_surface = load_and_scale_image('graphics/background_ground.jpg', screen_width) #this is not the syntax for loading in an image!! See above for actual syntax
score_surf = test_font.render('My game', False, 'Black')#creates text surface, second parameter is to smooth the text out
score_rect = score_surf.get_rect(center = (400, 50) )

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #Surface object contains actual image data
snail_rect = snail_surf.get_rect(bottomright = (600,300)) #Rect object stores coordinates and dimensions, NOT the image data(pixels, etc..)


player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))


while True:  #runs forever, unless broken from the inside
    for event in pygame.event.get(): #loops through every event that happened since it was last called
        if event.type == pygame.QUIT:   #QUIT is a constant equivalent to pressing x to quit out of the screen
            pygame.quit() #opposite of pygame.init()
            exit() #closes any type of code, including the while True loop
        if event.type == pygame.MOUSEMOTION: 
            print(event.pos)
            if player_rect.collidepoint(event.pos):
                print('player x mouse collision')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('left click')
            if event.button ==3:
                print('right click')
        if event.type == pygame.MOUSEBUTTONUP:
            print('mouse up')
       


    screen.blit(sky_surface, (0,-75)) #blit() is like sticking pictures onto a canvas at certain coordinates
    screen.blit(ground_surface, (0, 300)) 
    screen.blit(score_surf, score_rect)

    snail_rect.x -= 4
    if snail_rect.right <= 0: snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    #if player_rect.colliderect(snail_rect): #returns true or false
    #    print('collision')
    mouse_pos = pygame.mouse.get_pos() #returns x and y position
    if player_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed()) #returns tuple of boolean values for left click, middle click, and right click


    #draw all our elements
    #update everything
    
    pygame.display.update() #anything drawn within while loop is displayed to user
    clock.tick(60) #sets maximum frame rate, tells computer that while True loop should not run faster than 60 times per second, so that game doesn't run too fast

