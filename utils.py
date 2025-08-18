
import pygame

def load_and_scale_image(path, screen_width): #load image, scale surface to fill screen width while maintaining aspect ratio, return new surface
    surface = pygame.image.load(path)
    new_width, new_height = scale_by_width(surface, screen_width)
    return pygame.transform.scale(surface, (new_width, new_height))

def scale_by_width(surface, screen_width):   #scale surface to fill screen width while maintaining aspect ratio
    og_width, og_height = surface.get_size()
    scale_w = screen_width/og_width
    new_width = og_width *scale_w
    new_height = og_height *scale_w
    return new_width, new_height
