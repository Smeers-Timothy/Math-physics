# ------------------------------------------------------------------------
# Laboratoires de programmation mathématique et physique 2
# ------------------------------------------------------------------------
#
# Programme : 7 segments.
#
# Smeers Timothy
# SALEHIKATOZI SeyedPouria
# Ngandu Raphaël
# ------------------------------------------------------------------------

import math
import pygame
import sys
import numpy as np

### Constante(s)

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)

### Variables Globales


def draw_arduino(output_arduino, output_CD4511, output_button):
    screen.blit(image_arduino, pos_arduino)
    screen.blit(image_CD4511, pos_CD4511)
    screen.blit(image_button, pos_button)

    off_ard = 194
    off_cd = 15
    for i in range(0, 4):
        
        if output_arduino[i] == 0:
            color = BLACK
        else:
            color = RED

        pygame.draw.line(screen, color, (pos_arduino[0] + 280, pos_arduino[1] + off_ard),
                         (pos_CD4511[0] + 7, pos_CD4511[1] + off_cd), 5)
        off_ard = off_ard + 14
        off_cd = off_cd + 19

    off_cd = 15
    off_aff = 27
    for i in range(0, 7):
        if output_CD4511[i] == 0:
            color = BLACK
        else:
            color = RED
        pygame.draw.line(screen, color, (pos_segment_display[0], pos_segment_display[1] + off_aff),
                         (pos_CD4511[0] + 102, pos_CD4511[1] + off_cd), 5)
        off_aff = off_aff + 19
        off_cd = off_cd + 19

    connection_button(output_button)


def draw_segment_display(output_CD4511):
    bar_pos = [[32, 14], [89, 20], [87, 88], [28, 150],
                        [17, 88], [19, 20], [30, 82]]
    screen.blit(image_segment_display, pos_segment_display)

    i = 0
    for barre in bar_pos:
        if output_CD4511[i] == 0:
            i = i + 1
            continue
        x_b = pos_segment_display[0] + int(round(barre[0] * (image_segment_display.get_width() / 133)))
        y_b = pos_segment_display[1] + int(round(barre[1] * (image_segment_display.get_height() / 192)))
        if i == 0 or i == 3 or i == 6:
            screen.blit(horizontal_bar, (x_b, y_b))
        else:
            screen.blit(vertical_bar, (x_b, y_b))
        i = i + 1
    return


def component_CD4511(input):
    number = 0
    for i in range(4):
        number += 2 ** i * int(input[3 - i])
    return tdv[number]


def memorized_output():
    
    integer_number = int(number_stored_value)
    result = ''  
    
    for x in range(4):
        r = integer_number % 2
        integer_number = integer_number//2
        result += str(r)

    result = result[::-1]
    
    return np.array([result[0],result[1],result[2],result[3]])

def connection_button(output_button):
    if(output_button):
        pygame.draw.line(screen, RED, pin_button, pin_arduino,5)
    else:
        pygame.draw.line(screen, BLACK, pin_button, pin_arduino,5)

    return output_button

def temp_loop():
    color = BLACK
    if(sig_clock):
        color = RED
    ray = 10
    pygame.draw.circle(screen, color, (pos_segment_display[0] - ray, pos_segment_display[1] - ray), ray)
    
### Paramètre(s)

dimensions_screen = (1100, 600)  # en pixels
images_per_second = 25
number_stored_value = 0
tdv = np.array(
    [[1, 1, 1, 1, 1, 1, 0], [0, 1, 1, 0, 0, 0, 0], [1, 1, 0, 1, 1, 0, 1], [1, 1, 1, 1, 0, 0, 1], [0, 1, 1, 0, 0, 1, 1],
     [1, 0, 1, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 0, 1, 1]])

pos_arduino = (65, 84)
pos_CD4511 = (537, 263)
pos_segment_display = (818, 251)
pos_button = (537, 486)
pos_center_button = (589, 521)
ray_button = 18
pin_arduino = (pos_arduino[0] + 279, pos_arduino[1] + 353)
pin_button = (pos_button[0] + 13, pos_button[1] + 13)

### Programme

# Initialisation

pygame.init()

screen = pygame.display.set_mode(dimensions_screen)
pygame.display.set_caption("Programme 7 segments")

pygame.time.set_timer(pygame.USEREVENT, 500)

horloge = pygame.time.Clock()
sig_clock = False

image_segment_display = pygame.image.load('images/7_seg_s.png').convert_alpha(screen)
vertical_bar_segment = pygame.image.load('images/vertical_s.png').convert_alpha(screen)
horizontal_bar_segement = pygame.image.load('images/horizontal_s.png').convert_alpha(screen)
image_segment_display = pygame.image.load('images/7_seg.png').convert_alpha(screen)
vertical_bar = pygame.image.load('images/vertical.png').convert_alpha(screen)
horizontal_bar = pygame.image.load('images/horizontal.png').convert_alpha(screen)
image_arduino = pygame.image.load('images/arduino.png').convert_alpha(screen)
image_CD4511 = pygame.image.load('images/CD4511.png').convert_alpha(screen)
image_CD4028 = pygame.image.load('images/CD4028.png').convert_alpha(screen)
image_button = pygame.image.load('images/bouton.png').convert_alpha(screen)
font_color = GREY

# Boucle principale


while True:
    time_now = pygame.time.get_ticks()
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            sig_clock = not sig_clock
            
        elif pygame.mouse.get_pressed() [0]:
            
            if pygame.mouse.get_pos()[0] >= 571 and pygame.mouse.get_pos()[1] >= 503 and pygame.mouse.get_pos()[0] <= 607 and pygame.mouse.get_pos()[1] <= 539 :
                output_button = 1

                if(number_stored_value > 9 and number_stored_value >= 0):
                    number_stored_value = 0
                    
                elif(number_stored_value == 9):
                    number_stored_value = 0
                    
                else:
                    number_stored_value += 1
        else:
            output_button = 0


    screen.fill(font_color)
    temp_loop()

    output_CD4511 = component_CD4511(memorized_output())
    draw_segment_display(output_CD4511)
    draw_arduino(memorized_output(), output_CD4511, output_button)

    pygame.display.flip()
    horloge.tick(images_per_second)
