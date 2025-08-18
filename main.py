import pygame
from sys import exit
from utils import load_and_scale_image, scale_by_width

'''
-Didn't set a minimum frame rate because game is very simple, not very demanding on computer
- Surfaces:
    -Display Surface(the game window. Anything displayed goes on here)
        -Must be unique, must always be visible
    -(Regular) Surface(essentially a single image)
        -Needs to be on display surface to be visible
        -Flexible amount, only displayed when connected to display surface 
'''

pygame.init() #starts up the game, kind of like starting up the engine of the car

screen_width, screen_height = 800, 400
screen = pygame.display.set_mode((screen_width, screen_height)) #creates a display surface, stores it in a variable called 'screen'
pygame.display.set_caption('Runner') #changes name of game window
clock = pygame.time.Clock() 
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)#first argument font type, second argument font size

'''
sky_surface = pygame.image.load('graphics/sky.jpg') #directs to an image inside the folder 'Pygame-Learning'ground_surface = pygame.image.load('graphics/ground.jpg') #image is convereted into surface object 537 x 200
ground_surface = pygame.image.load('graphics/ground.jpg')
'''

def load_and_scale_image(path): #load image, scale surface to fill screen width while maintaining aspect ratio, return new surface
    surface = pygame.image.load(path)
    new_width, new_height = scale_by_width(surface)
    return pygame.transform.scale(surface, (new_width, new_height))

def scale_by_width(surface):   #scale surface to fill screen width while maintaining aspect ratio
    og_width, og_height = surface.get_size()
    scale_w = screen_width/og_width
    new_width = og_width *scale_w
    new_height = og_height *scale_w
    return new_width, new_height

sky_surface = load_and_scale_image('graphics/sky.jpg') #elegant way of creating a surface, and scaling it simultaneously using functions
ground_surface = load_and_scale_image('graphics/ground.jpg') #this is not the syntax for loading in an image!! See above for actual syntax
text_surface = test_font.render('My game', False, 'Black')#creates text surface, second parameter is to smooth the text out




#test_surface = pygame.Surface((100, 200)) #creates a (regular) surface
#test_surface.fill('Red')

while True:  #runs forever, unless broken from the inside
    for event in pygame.event.get(): #loops through every event 
        if event.type == pygame.QUIT:   #QUIT is a constant equivalent to pressing x to quit out of the screen
            pygame.quit() #opposite of pygame.init()
            exit() #closes any type of code, including the while True loop
    
    
    screen.blit(sky_surface, (0,-75)) #blit() is like sticking pictures onto a canvas at certain coordinates
    screen.blit(ground_surface, (0, 300)) 
    screen.blit(text_surface, (300,50))
    
    #draw all our elements
    #update everything
    
    pygame.display.update() #anything drawn within while loop is displayed to user
    clock.tick(60) #sets maximum frame rate, tells computer that while True loop should not run faster than 60 times per second, so that game doesn't run too fast