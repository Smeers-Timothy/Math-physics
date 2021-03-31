# Smeers Timothy
# SALEHIKATOZI SeyedPouria
# Ngandu Raphaël

#encoding: utf-8
import math
import pygame
import sys
# Variables

objects = []
mobile_pos = [0, 0]
mobile_speed = [0, 0]

# Constantes
LIGHTBLUE = (127, 191, 255)
RED = (255,0,0)
BLUE =(0,0,255)
PURPLE =(255,51,204) 

LEFT = 1
MIDDLE = 2
RIGHT = 3

BULK = pow(10,-10)
K = 8.9876* pow(10,9)

MOBILE_CHARGE = pow(10,-7) 
# Parametres

window_dimensions = (1600, 900)  # en pixels
images_per_second = 25
mobile_is_present = False

# Fonctions

def add_object(x,y,q):
    objects.append((x, y, q))
    
def draw_object():

    for i in range(0, len(objects)):
        y = objects[i][1]
        x = objects[i][0]
        
        if objects[i][2] >= 0:
            color = RED
        else :
            color = BLUE
            
        pygame.draw.circle(screen, color, (x, y), 10)
        
def draw_mobile():
    position = (int(mobile_pos[0]), int(mobile_pos[1]))
    
    if(mobile_is_present):
        if(MOBILE_CHARGE < 0):
            color = BLUE
        else:
            color = RED
        
        pygame.draw.circle(screen, color, position, 10, 4)

def calculate_champ(x,y):
    champ = [0, 0]
 
    for i in range(0, len(objects)):
        charge_x = objects[i][0]
        charge_y = objects[i][1]
        charge_q = objects[i][2]
 
        if(abs(charge_x - x) <= 20 and abs(charge_y - y) <= 20):
            return None
 
        dist = math.sqrt(pow((x - charge_x), 2) + pow((y - charge_y), 2))
        standard = (K * abs(charge_q)) / pow(dist, 2)
 
        angle = math.atan2(y - charge_y, x - charge_x)
        if(charge_q >= 0):
            vecteur = [standard * math.cos(angle), standard * math.sin(angle)]
        else:
            vecteur = [-standard * math.cos(angle), -standard * math.sin(angle)]
 
        champ[0] += vecteur[0]
        champ[1] += vecteur[1]
 
    return champ                                                                                                                       

def delete_object(position):                                
    x,y = position                                          
                                                            
    for object in objects:                                  
        pos = math.sqrt(pow((object[0] - x), 2) + pow((object[1] - y), 2))
                                                            
        if pos <= 10:                                       
            objects.remove(object)                                   
            
def calculate_coulomb_force():
        
    E = calculate_champ(int(mobile_pos[0]), int(mobile_pos[1]))

    if(E != None):
        force = [MOBILE_CHARGE*E[0], MOBILE_CHARGE*E[1]]
        
    return(force)
    
    
def update_mobile():
    global mobile_speed, mobile_pos, mobile_is_present
    
    if (mobile_is_present):  
        E = calculate_champ(int(mobile_pos[0]), int(mobile_pos[1]))

        if(E != None):
            force = [MOBILE_CHARGE * E[0], MOBILE_CHARGE * E[1]]
        
            acceleration = ((force[0] / BULK) , 
                            (force[1] / BULK))
    
            mobile_speed = [mobile_speed[0] + 0.001 * acceleration[0], 
                            mobile_speed[1] + 0.001 * acceleration[1]]

            mobile_pos = [mobile_pos[0] + mobile_speed[0] * 0.001, 
                          mobile_pos[1] + mobile_speed[1] * 0.001]
        else:
            mobile_is_present = False

def calculate_potential_energy(x, y ,charge):

    if mobile_is_present:
        w = 0
        for object in objects:
            dist = math.sqrt(pow((x - object[0]), 2) + 
                             pow((y - object[1]), 2))
            w += (K* object[2] * charge) / dist
        return w
    return 0

def calculate_kinetic_energy(bulk, speed):
    
    if(mobile_is_present):
        stantard = math.sqrt(pow(speed[0], 2) + pow(speed[1], 2))
        kinetic = 0.5 * bulk * pow(stantard, 2)
        
        return kinetic
    return 0


def display_energy(kinetic, potential, electrical_potential ):
    
    kinetic_text = "Energie Cinétique: {0:.2f} µJ".format(kinetic * pow(10, 6))
    potential_text = "Energie Potentielle: {0:.2f} µJ".format(potential * pow(10, 6))
    sum_text = "Somme des énergies: {0:.2f} µJ".format((kinetic+potential) * pow(10, 6))
    mouse_potential_text = "Potentiel Souris: {0:.2f} V".format(electrical_potential)

    k_img = police.render(kinetic_text, True, PURPLE)
    u_img = police.render(potential_text, True, PURPLE)
    som_img = police.render(sum_text, True, PURPLE)
    pot_img = police.render(mouse_potential_text, True, PURPLE)

    screen.blit(k_img, (50, 50))
    screen.blit(u_img, (50, 75))
    screen.blit(som_img, (50, 100))
    screen.blit(pot_img, (50, 125))
    
def calculate_potential(position):
    speed = 0
    x, y = position
    
    for object in objects:
        dist = math.sqrt(pow((x - object[0]), 2) + 
                         pow((y - object[1]), 2))
        if(dist <= 10):
            return 0
        
        speed += (K * object[2]) / dist
        
    if mobile_is_present:
        dist = math.sqrt(pow((mobile_pos[0] - x), 2) + 
                         pow((mobile_pos[1] - y), 2))
        if(dist <= 10):
            return 0
        
        speed += (K * MOBILE_CHARGE) / dist
    return speed    

# Initialisation
pygame.init()

add_object(800, 200, pow(10, -7))         
add_object(800, 700, pow(-10, -7))       

screen = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption("Programme 3")
police = pygame.font.SysFont("ubuntu", 20)

horloge = pygame.time.Clock()
fond_color = LIGHTBLUE

# GLOBAL VAR
previous_time = 0;
potential_energy = 0
kinetic_energy = 0            
    
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        elif event.type == pygame.MOUSEBUTTONDOWN: 
                 
            if event.button == LEFT:                                  
                add_object(int(event.pos[0]), int(event.pos[1]), pow(10, -7))           
                 
            elif event.button == MIDDLE:                         
                delete_object(event.pos[0], event.pos[1])                         
                     
            elif event.button == RIGHT:                 
                add_object(int(event.pos[0]), int(event.pos[1]), pow(-10, -7))

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_p:
                mobile_is_present = True
                MOBILE_CHARGE = abs(MOBILE_CHARGE)
                mobile_speed = [0,0]
                mobile_pos = pygame.mouse.get_pos()  
                
            if event.key == pygame.K_n:
                mobile_is_present = True
                MOBILE_CHARGE = -1 * abs(MOBILE_CHARGE)
                mobile_speed = [0,0]
                mobile_pos = pygame.mouse.get_pos() 
                       
    screen.fill(fond_color)
    time_now = pygame.time.get_ticks()
        
    for i in range(previous_time, time_now):
        update_mobile()
        
    draw_object()
    draw_mobile()
    
    potential_energy = calculate_potential_energy(mobile_pos[0], mobile_pos[1], 
                                                    MOBILE_CHARGE)
    
    kinetic_energy = calculate_kinetic_energy(BULK, mobile_speed)
    
    electrical_potential = calculate_potential((pygame.mouse.get_pos()[0], 
                                                    pygame.mouse.get_pos()[1]))
    
    display_energy(kinetic_energy, potential_energy, electrical_potential)
            
    pygame.display.flip()  
    previous_time = time_now
    horloge.tick(images_per_second)
    
    
    