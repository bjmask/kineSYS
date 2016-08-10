#!/usr/bin/python

import math
import sys
import time

import numpy as np

import pygame

from pygame.locals import *

# FPS = 30
SQUARE_DIMENSION = 120

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def make_sin_array(frequency):

    f = frequency
    w = 2. * np.pi * f
    time_interval = 1
    samples = 360
    wave = np.sin(w * np.linspace(0, time_interval, samples))
    return wave

def toggle_fullscreen():

    screen = pygame.display.get_surface()
    tmp = screen.convert()
    caption = pygame.display.get_caption()
    cursor = pygame.mouse.get_cursor()
   
    w, h = screen.get_width(),screen.get_height()
    flags = screen.get_flags()
    bits = screen.get_bitsize()
   
    pygame.display.init()
   
    screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
    screen.blit(tmp,(0,0))
    pygame.display.set_caption(*caption)

    pygame.key.set_mods(0) 
    pygame.mouse.set_cursor(*cursor )   
    return screen



def main():

    def draw_square(color, x, y):
        pygame.draw.rect(background, color, (x, y, SQUARE_DIMENSION, SQUARE_DIMENSION))

    clock = pygame.time.Clock()
    # Initialise screen
    pygame.init()
    SW, SH = 1920, 1080
    screen = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption('SSVEP Trainer')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    #create four wave arrays
    array_of_sines = [make_sin_array(frequency) for frequency in [10, 15, 20, 60]]

    # Event loop
    while True:
        # t0 = time.time()
        for i in range(360):
            # Create rectangles to emit frequencies
            if array_of_sines[0][i] > 0:
                draw_square(WHITE, 0, 440)
            else:
                draw_square(BLACK, 0, 440)

            if array_of_sines[1][i] > 0:
                draw_square(WHITE, 840, 0)
            else:
                draw_square(BLACK, 840, 0) 

            if array_of_sines[2][i] > 0:
                draw_square(WHITE, 840, 960)
            else:
                draw_square(BLACK, 840, 960)

            if array_of_sines[3][i] > 0:
                draw_square(WHITE, SW - 120, 440)
            else:
                draw_square(BLACK, SW - 120, 440)

            # Blit everything to the screen
            screen.blit(background, (0, 0))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type is QUIT:
                    _quit = True
                if (event.type is KEYDOWN and event.key == K_f):
                    toggle_fullscreen()
                if event.type is KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()

            # screen.blit(background, (0, 0))
        pygame.display.flip()
        # print time.time() - t0         

if __name__ == '__main__':
    main()
