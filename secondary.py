#in this file the game will be coded in Functional/Procedural code, not with sprites/OOP

import pygame
from sys import exit
from random import randint, choice
from utils import load_and_scale_image, scale_by_width, display_score


pygame.init() #starts up the game, kind of like starting up the engine of the car

def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:  #if list is empty, returns False
        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -=5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
          
            obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x >-100]#weird syntax but basically creates a new version of the list that only includes on-screen obstacles
        return obstacle_rect_list
    else:
        return []
    


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                return False
    return True

    
def player_animation():
    global player_surf, player_index #player_rect is mutable so you can access it here without global
    if player_rect.bottom <300: #above ground, so should be jumping
        player_surf = player_jump
    else:
        player_index +=0.1 # 0.1 means it takes multiple frames to get to the next image
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]



screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height)) #creates a display surface, stores it in a variable called 'screen'
pygame.display.set_caption('Runner') #changes name of game window
clock = pygame.time.Clock() 
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False #for creating different game states
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.3)
bg_music.play(loops = -1) #-1 means to loop forever, 6 would mean to loop the sound 6 times
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)


#Background
sky_surface = load_and_scale_image('graphics/background_sky.jpg', screen_width) #elegant way of creating a surface, and scaling it simultaneously using functions
ground_surface = load_and_scale_image('graphics/background_ground.jpg', screen_width) #this is not the syntax for loading in an image!! See above for actual syntax

#Snail
snail_frame_1= pygame.image.load('graphics/snail/snail1.png').convert_alpha() #Surface object contains actual image data
snail_frame_2= pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

#Fly
fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []


#Player
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 1
player_velocity = 0

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0 , 2) #first argument: surface, second argument: angle, third argument: scale
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center= (400, 80))

game_message = test_font.render('Press space to run', False, (111,196,169))
game_message_rect= game_message.get_rect(center = (400,320))

#Timer
obstacle_timer = pygame.USEREVENT + 1 #custom user event, with it's own integer ID. Every Pygame event has a unique integer event type
pygame.time.set_timer(obstacle_timer, 1500) #Pygame internally starts a timer that pushes an event with type obstacle_timer onto the event queue every 1500 milliseconds.

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 150)


while True:  #runs forever, unless broken from the inside
    for event in pygame.event.get(): #loops through every event that happened since it was last called
        if event.type == pygame.QUIT:   #QUIT is a constant equivalent to pressing x to quit out of the screen
            pygame.quit() #opposite of pygame.init()
            exit() #closes any type of code, including the while True loop

        if game_active == True: 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #could remove this if statement but wtv
                    if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
                        player_velocity = -20
                        jump_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_velocity= -20
                    jump_sound.play()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        
        if game_active:
            if event.type == obstacle_timer:
                if randint(0,1):   #50-50 chance, could change that if wanted
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index =1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:  #needed for creating different game states
        #Backdrop, Score
        screen.blit(sky_surface, (0,-75)) #blit() is like sticking pictures onto a canvas at certain coordinates
        screen.blit(ground_surface, (0, 300)) 
        #pygame.draw.rect(screen, '#c0e8ec', score_rect)
        #pygame.draw.rect(screen, '#c0e8ec', score_rect, 6) #1st argument: surface to drawn on, 2nd: color, 3rd: position of the rectangle, 4th: border width
        #screen.blit(score_surf, score_rect)
        score = display_score(screen, start_time, test_font)
        
        #Player
        player_velocity += player_gravity #quadratic- projectile motion 
        player_rect.y += player_velocity     
        if player_rect.bottom >=300: player_rect.bottom = 300 #everytime player is underneath ground, teleport them to on ground, gives illusion of a solid ground
        player_animation()
        screen.blit(player_surf, player_rect)
        
       
        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        game_active = collisions(player_rect, obstacle_rect_list)
        
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear() #prevents getting hit by same obstacle
        player_rect.midbottom = (80,300)
        player_velocity = 0
        
        score_message = test_font.render(f'Your score was: {score}', False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,320))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
        
    #update everthing
    #then draw
    pygame.display.update() #anything drawn within while loop is displayed to user
    clock.tick(60) #sets maximum frame rate, tells computer that while True loop should not run faster than 60 times per second, so that game doesn't run too fast

