import math
WIDTH = 1200 
HEIGHT = 800

FPS = 120
H_W = WIDTH //2
H_H = HEIGHT//2
TILE = 100
X2_HEIGHT = HEIGHT*2


#FOV, дальность прорисовки, настройки ray casting
FOV = math.pi/3 #области видимости, угол обзора, a = -FOV/2, -a = FOV/2 это границы угла обзора
H_FOV = FOV /2 #половина угла обзора просто чтобы чтоб
NUM_RAYS = 200 #количество лучей
MAX_DEPTH = 1000 #дальность прорисовки
DELTA_ANGLE = FOV/NUM_RAYS #угол между лучами
DIST = NUM_RAYS/(2* math.tan(H_FOV))

PROJ_COFF = 2 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

#мини-карта
MINIMAP_SCALE = 7
MAP_SCALE = 2 * MINIMAP_SCALE 
MINIMAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - X2_HEIGHT // MAP_SCALE)


#спрайты
D_PI = 2 * math.pi
C_RAY = NUM_RAYS // 2 - 1
F_RAY = 100
F_RAY_RANGE = NUM_RAYS - 1 + 2 * F_RAY

#ТЕКСТУРНЫЙ ПРИХОД (1000х1000)
TEXTURE_WIDTH = 900
TEXTURE_HEIGHT = 900
TEXTURE_SCALE = TEXTURE_WIDTH // TILE
HALF_TEXT_H = TEXTURE_HEIGHT // 2

#PLAYER
pl_position = (H_H+5, H_W+1)
pl_angle = 0
pl_speed = 3.5

#COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (125,125,125)
SKY = (13,13,23)
FLOOR = (60,42,32)
BACK_MINI =(147, 118, 181)
MINI_PL = (139, 199, 173)


