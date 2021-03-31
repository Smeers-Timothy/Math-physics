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

###FUNCTION

def draw_arduino(output_arduino, output_CD4511, output_CD4028, output_button):

    screen.blit(image_arduino, pos_arduino)
    screen.blit(image_CD4511, pos_CD4511)
    screen.blit(image_button, pos_button)
    screen.blit(image_CD4028, pos_CD4028)


    for j in range(0, 2):
        if j == 0:
            off_ard = 285
            off_cd = 15
            pos_carte = pos_CD4511
            r = range(0, 4)

        if j == 1:
            off_ard = 194
            off_cd = 91
            pos_carte = pos_CD4028
            r = range(4, 8)

        for i in r:
            if output_arduino[i] == 0:
                color = BLACK
            else:
                color = RED

            pygame.draw.line(screen, color, (pos_arduino[0] + 280, pos_arduino[1] + off_ard),
                            (pos_carte[0] + 7, pos_carte[1] + off_cd), 5)
            off_ard = off_ard + 14
            off_cd = off_cd + 19

    off_cd = 15
    off_aff = 5
    i = 0
    for i in range(0, 7):
        if output_CD4511[i] == 0:
            color = BLACK
        else:
            color = RED
        pygame.draw.line(screen, color, (pos_segment_display[0] + 591, pos_segment_display[1] + off_aff),
                        (pos_CD4511[0] + 102, pos_CD4511[1] + off_cd), 5)
        off_aff = off_aff + 19
        off_cd = off_cd + 19


    if output_button == 0:
        color = BLACK
    else:
        color = RED
    pygame.draw.line(screen, color, (pos_arduino[0] + 279, pos_arduino[1] + 353),
                        (pos_button[0] + 13, pos_button[1] + 13), 5)

    i = 0
    off_cd = (102, 111)
    off_aff = 44
    for i in range(0, 6):
        if output_CD4028[i] == 0:
            color = BLACK
        else:
            color = RED
        pygame.draw.line(screen, color, (pos_CD4028[0] + off_cd[0], pos_CD4028[1] + off_cd[1]),
                        (pos_segment_display[0] + off_aff, pos_CD4028[1] + off_cd[1]), 5)

        pygame.draw.line(screen, color, (pos_segment_display[0] + off_aff, pos_segment_display[1]),
                        (pos_segment_display[0] + off_aff, pos_CD4028[1] + off_cd[1] - 2), 5)
        off_cd = (off_cd[0], off_cd[1] - 20)
        off_aff = off_aff + 101



def draw_segment_display(output_CD4511, output_CD4028):

    pos_bar = [[32, 14], [89, 20], [87, 88], [28, 150],
                        [17, 88], [19, 20], [30, 82]]

    for j in range(0, 6):
        screen.blit(image_segment_display, (pos_segment_display[0] + j*101, pos_segment_display[1]))
        i = 0
        for bar in pos_bar:
            if latency_matrix[j][i] == 0:
                i += 1
                continue
            x_b = j*101 + pos_segment_display[0] + int(round(bar[0]*(image_segment_display.get_width()/133)))
            y_b = pos_segment_display[1] + int(round(bar[1]*(image_segment_display.get_height()/192)))
            if i == 0 or i == 3 or i == 6:
                screen.blit(horizontal_bar_segement, (x_b, y_b))
            else:
                screen.blit(vertical_bar_segment, (x_b, y_b))
            i += 1
    return


def component_CD4511(input):

    number = 0
    input = np.flip(input)
    for i in range(len(input)):
        number += input[i] * pow(2,i)

    number = int(number)
    
    tdv = np.array([[0,0,1,0,1,1,1], [1,0,0,1,1,1,1],[0,0,0,1,1,1,0],[0,0,1,1,1,0,1],[0,1,1,1,1,1,1],[0,0,0,0,1,0,1],[0,1,1,1,1,0,1],[0,0,0,0,0,0,0]])
        
    return tdv[number]

def component_CD4028(input):

    number = 0
    input = np.flip(input)
    
    for i in range(len(input)):
        number += input[i] * pow(2,i)

    number = int(number)
    
    light_up_display = [0,0,0,0,0,0]
    light_up_display[number-1] = 1
    print(light_up_display)

    return light_up_display

def memorized_output():
    global number_stored_value,  number_display
    
    size_array = 4
    array_bin = np.zeros(size_array)
    array_num = np.zeros(size_array)
    
    temp_val = number_stored_value
    temp_display = number_display
    
    while temp_val != 0:
        residue = temp_val % 2
        array_bin[size_array -1] = residue
        temp_val = temp_val // 2
        size_array -= 1
    
    size_array = 4
    
    while temp_display != 0:
        residue = temp_display % 2
        array_num[size_array -1] = residue
        temp_display = temp_display // 2
        size_array -= 1
    
    array = np.append(array_bin, array_num)
    return array
    
def connection_button(output_button):
    
    if output_button == 1:
        pygame.draw.line(screen, RED, pin_arduino, pin_button, 5)

    else:
        pygame.draw.line(screen, BLACK, pin_arduino, pin_button, 5)
    return
    
def move_hello(hello):
    
    pos_0  = hello[0]
    pos_1 = hello[1]
    pos_2 = hello[2]
    pos_3 = hello[3]
    pos_4= hello[4]
    pos_5= hello[5]
    pos_6= hello[6]
    pos_7= hello[7]
    pos_8= hello[8]
    pos_9= hello[9]
    pos_10= hello[10]
    pos_11 = hello[11]

    hello[0] = pos_1
    hello[1] = pos_2
    hello[2] = pos_3
    hello[3] = pos_4
    hello[4] = pos_5
    hello[5] = pos_6
    hello[6] = pos_7
    hello[7] = pos_8
    hello[8] = pos_9
    hello[9] = pos_10
    hello[10] = pos_11
    hello[11] = pos_0

    return hello

### Paramètre(s)

dimensions_screen = (1100, 600)  
images_per_second = 25
pos_arduino = (0, 70)
pos_CD4511 = (333, 340)
pos_CD4028 = (333, 128)
pos_segment_display = (500, 350)
pos_button = (333, 524)
pos_center_button = (pos_button[0] + 51, pos_button[1] + 34)
ray_button = 18
pin_arduino = (pos_arduino[0] + 279, pos_arduino[1] + 353)
pin_button = (pos_button[0] + 13, pos_button[1] + 13)


### Programme

# Initialisation

pygame.init()

screen = pygame.display.set_mode(dimensions_screen)
pygame.display.set_caption("Programme 7 segments")

pygame.time.set_timer(pygame.USEREVENT, 1000)
pygame.time.set_timer(pygame.USEREVENT+1, 40)
horloge = pygame.time.Clock()


image_segment_display = pygame.image.load('images/7_seg_s.png').convert_alpha(screen)
vertical_bar_segment = pygame.image.load('images/vertical_s.png').convert_alpha(screen)
horizontal_bar_segement = pygame.image.load('images/horizontal_s.png').convert_alpha(screen)
vertical_bar = pygame.image.load('images/vertical.png').convert_alpha(screen)
horizontal_bar = pygame.image.load('images/horizontal.png').convert_alpha(screen)
image_arduino = pygame.image.load('images/arduino.png').convert_alpha(screen)
image_CD4511 = pygame.image.load('images/CD4511.png').convert_alpha(screen)
image_CD4028 = pygame.image.load('images/CD4028.png').convert_alpha(screen)
image_button = pygame.image.load('images/bouton.png').convert_alpha(screen)
font_color = GREY

#Variable 
number_stored_value = 0
number_display = 0

array = memorized_output()

latency_matrix = np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])

hello = np.array([0,1,2,2,3,7,4,3,5,2,6,7])

# Boucle principale
while True:
    
        output_button = 0
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                
                    if mouse_x<pos_center_button[0] + ray_button and mouse_x > pos_center_button[0] - ray_button:
                        
                        if mouse_y < pos_center_button[1] + ray_button and mouse_y > pos_center_button[1] - ray_button:
                            output_button = 1
                            move_hello(hello)
                
            elif event.type == pygame.USEREVENT:
                
                hello = move_hello(hello)
    
            elif event.type == pygame.USEREVENT+1:
                number_display += 1
                
                if number_display >= 6:
                    number_display = 0
    
    
        screen.fill(font_color)
        
        number_stored_value = hello[number_display]
        array = memorized_output()
            
        output_CD4511 = component_CD4511(array[:4])
        latency_matrix[number_display] = output_CD4511

        light_up_display = component_CD4028(array[4:])
        
        draw_arduino(memorized_output(), output_CD4511, light_up_display, output_button)
        
        draw_segment_display(output_CD4511, light_up_display)
        
        pygame.display.flip()
        horloge.tick(images_per_second)
        
