#game will be coded using sprites/OOP
#this version of the code omits some comments for the sake of readability
#see secondary version for those comments, and for the version of the same game in functional/procedural code

import pygame
from sys import exit
from random import randint, choice
from utils import load_and_scale_image, scale_by_width, display_score

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        
        self.image = self.player_walk[self.player_index] #essential to have self.image and self.rect
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 1
        self.velocity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5) #choose a value between 0 and 1, with 0 being no sound, and 1 being full sound

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.velocity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        if self.rect.bottom >=300: self.rect.bottom = 300 #everytime player is underneath ground, teleport them to on ground, gives illusion of a solid ground

    def animation_state(self):
        if self.rect.bottom <300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index > len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]


    def update(self): #put all update methods inside this
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == 'fly':
            fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210
        if self.type == 'snail':
            snail_frame_1= pygame.image.load('graphics/snail/snail1.png').convert_alpha() #Surface object contains actual image data
            snail_frame_2= pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
       
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        if self.type == 'fly':
            self.animation_index += 0.25
        if self.type == 'snail':
            self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()



def collision_sprite():
# first argument: sprite, second argument: group, third argument: boolean that asks if a snail/fly collids with player is the snail/fly deleted  
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):  #returns a list of collisions
        obstacle_group.empty() #resets obstacles to none before next game start
        return False
    else:
        return True
    


pygame.init() #starts up the game, kind of like starting up the engine of the car
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

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


#Background
sky_surface = load_and_scale_image('graphics/background_sky.jpg', screen_width) #elegant way of creating a surface, and scaling it simultaneously using functions
ground_surface = load_and_scale_image('graphics/background_ground.jpg', screen_width) #this is not the syntax for loading in an image!! See above for actual syntax


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


while True:  #runs forever, unless broken from the inside
    for event in pygame.event.get(): #loops through every event that happened since it was last called
        if event.type == pygame.QUIT:   #QUIT is a constant equivalent to pressing x to quit out of the screen
            pygame.quit() #opposite of pygame.init()
            exit() #closes any type of code, including the while True loop
        
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail']))) #1/3 chance of fly, 2/3 chance of snail
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
        

    if game_active:  #needed for different game states
        #Backdrop, Score
        screen.blit(sky_surface, (0,-75)) 
        screen.blit(ground_surface, (0, 300)) 
        score = display_score(screen, start_time, test_font)
        
        #Groups
        player.update()
        player.draw(screen)
       
        obstacle_group.update()
        obstacle_group.draw(screen)

        #collision
        game_active = collision_sprite()
  
        
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        
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

