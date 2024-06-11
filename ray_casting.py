import pygame
from settings import *
from map import world_map, WORLD_WIDTH, WORLD_HEIGHT
from numba import njit #ускорение вычислений, оптимизация

@njit(fastmath=True)
def mapping(a, b): # возвращение координатов левого верхнего угла столкновения с тайлом (квадратиком)
    return (a // TILE) * TILE, (b // TILE) * TILE

@njit(fastmath=True)
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    x0, y0 = player_pos #начальная координата луча
    texture_v, texture_h = 1, 1 #костыль для фикса ошибки при генерации текстур
    xm, ym = mapping(x0, y0)
    current_angl = player_angle - H_FOV
    for ray in range(NUM_RAYS):
        sin_a = math.sin(current_angl)
        cos_a = math.cos(current_angl)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        #вертикали
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1) #x - текущая вертикаль, dx - подручный
        for i in range(0, WORLD_WIDTH, TILE): #проход по вертикалям и ширине экрана
            depth_v = (x - x0) / cos_a #расстояние до вертикали
            yv = y0 + depth_v * sin_a #координата вертикали
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        #горизонтали
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1) #y - текущая горизонталь, dy - подручный
        for i in range(0, WORLD_HEIGHT, TILE): #проход по горизонталям, высоте экрана
            depth_h = (y - y0) / sin_a #расстояние до горизонтали
            xh = x0 + depth_h * cos_a #координата горизонтали
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map: #выбор текстурки для отрисовки
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        #проекция
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h) #Проверка того, что ближе
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - current_angl) #избавление от эффекта рыбьего глаза
        depth = max(depth, 0.00001)
        proj_height = int(PROJ_COFF / depth)

        casted_walls.append((depth, offset, proj_height, texture))
        current_angl += DELTA_ANGLE #изменение угла для луча
    return casted_walls

def ray_casting_walls(player, textures): #отрисовка стен отдельно (иначе нумба не работает, формирование текстер)
    casted_walls = ray_casting(player.pos, player.angle, world_map)
    walls = []

    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > HEIGHT:
            coeff = proj_height / HEIGHT
            texture_height = TEXTURE_HEIGHT / coeff
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, HALF_TEXT_H - texture_height // 2, TEXTURE_SCALE, texture_height)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, 0)
        else:
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, H_H - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
    return walls