
import pygame

def load_and_scale_image(path, screen_width): #load image, scale surface to fill screen width while maintaining aspect ratio, return new surface
    surface = pygame.image.load(path).convert_alpha()
    new_width, new_height = scale_by_width(surface, screen_width)
    return pygame.transform.scale(surface, (new_width, new_height))

def scale_by_width(surface, screen_width):   #scale surface to fill screen width while maintaining aspect ratio
    og_width, og_height = surface.get_size()
    scale_w = screen_width/og_width
    new_width = og_width *scale_w
    new_height = og_height *scale_w
    return new_width, new_height

def display_score(screen, start_time, test_font): #counts and draws the score on the screen
    #screen needs to be passed into this function, like Canvas from Stanford
    current_time = int((pygame.time.get_ticks() - start_time) / 1000) #milliseconds since pygame.init() - when game starts
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time