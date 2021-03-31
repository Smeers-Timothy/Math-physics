# Smeers Timothy
# SALEHIKATOZI SeyedPouria
# Ngandu Raphaël

#encoding: utf-8
import math
import pygame
import sys
# Variables

objects = []

# Constantes

BLEUCLAIR = (127, 191, 255)
RED = (255,0,0)
BLUE =(0,0,255)
GREEN = (0, 255, 0)
A = 1
B = 5
C = 10
LEFT = 1
MIDDLE = 2
RIGHT = 3

# Param�tres

dimensions_fenetre = (1600, 900)  # en pixels
images_par_seconde = 25

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
        pygame.draw.circle(fenetre, color, (x, y), 10)

def move_head(point, distance, orientation):
    
    x_1, y_1 = point
    y_2 = math.sin(orientation) * distance
    x_2 = math.cos(orientation) * distance
    x = x_1 + x_2
    y = y_1 + y_2
    return (x,y)

def draw_vector(fenetre, couleur, origine, vecteur):
     
    x, y = vecteur
    teta = math.atan2(y,x)
    norme = math.sqrt((x ** 2) + (y ** 2))
 
    if norme >= C:
        p_4 = (origine[0] + vecteur[0],origine[1] + vecteur[1])
        p_1 = move_head(origine, A, (teta - (math.pi / 2)))
        p_2 = move_head(p_1, (norme - C), teta)
        p_3 = move_head(p_2, B, (teta - (math.pi / 2)))
        p_7 = move_head(origine, A, (teta + (math.pi / 2)))
        p_6 = move_head(p_7, (norme - C), teta)
        p_5 = move_head(p_6, B, (teta + (math.pi / 2)))
 
        fleche = [p_1, p_2, p_3, p_4, p_5, p_6, p_7] 
           
    else:
        p_3 = (origine[0] + vecteur[0], origine[1] + vecteur[1])
        p_1 = move_head(p_3, C, (teta + math.pi))
        p_2 = move_head(p_1, (A + B), (teta - (math.pi / 2)))
        p_4 = move_head(p_1, (A + B), (teta + (math.pi / 2)))
     
        fleche = [p_1, p_2, p_3, p_4]
         
    return pygame.draw.polygon(fenetre,couleur,fleche)

 
def draw_champ():
     
    (x,y) = dimensions_fenetre
    lower_bound = -50
    increment = 50
     
    for i in range(lower_bound, x+2*increment ,increment):
        for j in range(lower_bound, y+2*increment ,increment):
              
            e_v = calculate_champ(i, j)
              
            if(e_v != None):
                
                norme = math.sqrt(e_v[0]**2 + e_v[1]**2)
                
                if (norme >= pow(10, -10)):
                    
                    if (e_v[0] == 0):
                        vector = [0, 40*(e_v[1])/norme]
                        
                    elif(e_v[1] == 0):
                        vector = [40*(e_v[0])/norme, 0]
                            
                    else:
                        vector = [40*(e_v[0])/norme, 40*(e_v[1])/norme]
                    
                    origine_x = i- (vector[0]/2)
                    origine_y = j- (vector[1]/2)
                    v = math.sqrt(1000*math.hypot(e_v[0], e_v[1]))
                    color = (255,0,255)

                    if(v<=8):
                        offset = (255 *v)/8
                        color = (255,offset,0)
                        
                    elif(v <= 16):
                        offset = (255 * (v-8))/8
                        color = (255-offset, 255, offset)
                        
                    elif(v <= 24):
                        offset = (255 * (v-16))/8
                        color = (0, 255-offset, 255)
                        
                    elif(v <= 32):
                        offset = (255 * (v-24))/8
                        color = (offset, 0, 255)
                          
                    draw_vector(fenetre, color, (origine_x, origine_y), vector)

def calculate_champ(x,y):
    
    champ =[0,0]
    k = 8.9876*10**9
    
    for object in objects:
        charge_x = object[0]
        charge_y = object[1]
        charge_q = object[2]
        r = math.hypot((x - charge_x),(y - charge_y))  
        
        if r<=20:
            return None
        else:
            i =[0,0]
            i=[(x - charge_x), (y - charge_y)]

            if r > 1e-10:
                i[0] /= r
                i[0] *= (k*charge_q)/r**2
                i[1] /= r
                i[1] *= (k*charge_q)/r**2
                champ[0] +=i[0]
                champ[1] +=i[1]
    
    if(champ != None):
        return champ
    
def update():                                               # prog_2
    fenetre.fill(couleur_fond)                              # prog_2
    draw_object()                                           # prog_2
    draw_champ()                                            # prog_2
    
def get_position():                                         # prog_2
    x,y = pygame.mouse.get_pos()                            # prog_2
    return(x,y)                                             # prog_2

def mouse_pressed(C):                                       # prog_2
    add_object(get_position()[0], get_position()[1], C)     # prog_2
    update()                                                # prog_2                                     

def delete_object(position):                                # prog_2
    x,y = position                                          # prog_2
                                                            # prog_2
    for object in objects:                                  # prog_2
        pos = math.sqrt((object[0]-x)**2 + (object[1]-y)**2)# prog_2
                                                            # prog_2
        if pos <= 10:                                       # prog_2
            objects.remove(object)                          # prog_2
            update()                                        # prog_2

# Initialisation
pygame.init()

add_object(800, 200, 10**-6)         # programme de base
add_object(800, 700, -10**-6)        # programme de base
# add_object(533, 200, 10**-6)         # expérience 1
# add_object(1066, 700, 10**-6)        # expérience 1
# add_object(1066, 200, -10**-6)       # expérience 1
# add_object(533, 700, -10**-6)        # expérience 1
# for i in range(533,1060,27):         # expérience 2
#     add_object(i, 200, 10**-7)       # expérience 2
# for i in range(533,1060,27):         # expérience 2
#     add_object(i, 700, -10**-7)      # expérience 2

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 2")

horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

# Dessin

update()                
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:      # prog_2
            if event.button == LEFT:                    # prog_2
                print("left mouse button")              # prog_2
                mouse_pressed(pow(10,-7))               # prog_2
                
            elif event.button == MIDDLE:                # prog_2
                print("middle mouse button")            # prog_2
                delete_object(get_position())           # prog_2
                    
            elif event.button == RIGHT:                 # prog_2
                print("right mouse button")             # prog_2
                mouse_pressed(pow(-10,-7))              # prog_2

    pygame.display.flip()  
    horloge.tick(images_par_seconde)