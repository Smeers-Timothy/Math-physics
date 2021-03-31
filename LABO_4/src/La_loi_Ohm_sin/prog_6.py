# ------------------------------------------------------------------------
# Laboratoires de programmation mathématique et physique 2
# ------------------------------------------------------------------------
#
# Programme : 6 La Loi d'Ohm Laboratoires 4
#
# Smeers Timothy
# SALEHIKATOZI SeyedPouria
# Ngandu Raphaël
# -----------------------------------------------------------------------

import math
import pygame
import sys

# Fonctions

def draw_dotted_lines_h(surface, color, y):
    n = window_dimensions[0] // (dot_length * 2)

    for i in range(n + 1):
        x1 = int((i - 0.25) * dot_length * 2)
        x2 = x1 + dot_length
        pygame.draw.line(surface, color, (x1, y), (x2, y))

    return

def draw_dotted_lines_v(surface, color, x):
    n = window_dimensions[1] // (dot_length * 2)

    for i in range(n + 1):
        y1 = (i - 0.25) * dot_length * 2
        y2 = y1 + dot_length
        pygame.draw.line(surface, color, (x, y1), (x, y2))

    return

def show_grid():
    yc = window_dimensions[1] // 2
    nh = yc // grid_size

    for i in range(1, nh + 1):
        
        draw_dotted_lines_h(screen, GREY, yc + i * grid_size)
        draw_dotted_lines_h(screen, GREY, yc - i * grid_size)

    pygame.draw.line(screen, GREY, (0, yc), (window_dimensions[0], yc))

    nv = window_dimensions[0] // grid_size
    for i in range(0, nv + 1):
        draw_dotted_lines_v(screen, GREY, i * grid_size)

    return

def generate_signaux(delta_t):

    PERIOD = 0.009

    voltage = 5         # 5 V
    intensity = 2.5     # I = U/R
    power = 12.5        # P = U * I
    signal_4 = 100

    global signals_initialized, TEMP_1, TEMP_2, TEMP_3, TEMP_4
    if not signals_initialized:

        TEMP_1 = 0
        TEMP_2 = 0
        TEMP_3 = 0
        TEMP_4 = 0

        signals_initialized = True
        return (0, 0, 0, 0)

    TEMP_1 = math.fmod(TEMP_1 + delta_t * 2 * math.pi / PERIOD,
                   2 * math.pi)
    TEMP_2 = math.fmod(TEMP_2 + delta_t * 2 * math.pi / PERIOD,
                   2 * math.pi)
    TEMP_3 = math.fmod(TEMP_3 + delta_t * 2 * math.pi / PERIOD,
                   2 * math.pi)
    TEMP_4 = math.fmod(TEMP_4 + delta_t * 2 * math.pi / PERIOD,
                   2 * math.pi)
        
    
    return (voltage * math.cos(TEMP_1),
            intensity * math.cos(TEMP_2),
            power * (math.cos(TEMP_3) * math.cos(TEMP_3)),
            signal_4 * math.cos(TEMP_4))
    
        
def acquisition(t):
    global acquisition_initialized, t_signaux_prec

    if acquisition_initialized:
        dt = t - t_signaux_prec
        if dt <= 0:
            print("timing error")
            sys.exit()

        while dt > t_samples:
            generate_signaux(t_samples)
            dt -= t_samples

        s = generate_signaux(dt)
    else:
        s = (0, 0, 0, 0)
        acquisition_initialized = True

    t_signaux_prec = t

    return s

def display_signal(x, v, color, gain):
    y = window_dimensions[1] // 2 - v * gain
    pygame.draw.line(screen, color, (x, y - 5), (x, y + 5))
    return

def display_frame(time_now):
    signals_prec = acquisition(time_now)

    for x in range(window_dimensions[0]):
        time_now += t_samples
        signals = acquisition(time_now)

        if (signals[0] >= threshold_trigger and
            signals_prec[0] < threshold_trigger):
            break

        signals_prec = signals

    for x in range(window_dimensions[0]):
        time_now += t_samples
        signals = acquisition(time_now)
        for i in range(4):
            display_signal(x, signals[i], signal_colour[i],
                            signal_gain[i])
    return

def display_trigger():
    y =  window_dimensions[1] // 2 - threshold_trigger * signal_gain[0]
    pygame.draw.line(screen, RED, (0, y), (20, y), 5)
    return

# Constantes

LIGHT_BLUE = (127, 191, 255)
CYAN = (0, 255, 255)
GREY = (127, 127, 127)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Paramètres

window_dimensions = (800, 600)  # en pixels
images_per_second = 25

grid_size = 100
dot_length = 10

t_trame = 0.010
t_samples = t_trame / window_dimensions[0]

threshold_trigger = 5
threshold_trigger_delta = 0.2

signal_colour = [ YELLOW, CYAN, MAGENTA, GREEN ]
signal_gain = [ 20, 20, 20, 20 ]

# Initialisation

pygame.init()

screen = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption("Programme 6")

clock = pygame.time.Clock()
background_colour = LIGHT_BLUE

pygame.key.set_repeat(10, 10)

acquisition_initialized = False
signals_initialized = False

# Dessin

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_UP:
                threshold_trigger += threshold_trigger_delta
            elif evenement.key == pygame.K_DOWN:
                threshold_trigger -= threshold_trigger_delta

    time_now = pygame.time.get_ticks() / 1000

    screen.fill(background_colour)
    display_frame(time_now)
    display_trigger()
    show_grid()
    pygame.display.flip()
    clock.tick(images_per_second)
