from settings import *
import pygame
from numba.core import types #оптимизация
from numba.typed import Dict
from numba import int32

_ = False
matrix_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, _, 1, _, _, _, 1, _, _, _, _, _, 1],
    [1, _, 2, 2, 2, _, _, _, _, 2, 2, 2, _, _, _, 3, _, _, _, 2, 2, 2, _, 1],
    [1, _, _, _, _, _, 2, 2, _, _, _, 2, 2, _, _, _, 3, _, _, _, _, _, _, 1],
    [1, _, 2, 2, _, _, 2, _, _, _, _, _, 2, _, 1, _, _, 3, _, 1, _, 1, _, 1],
    [1, _, 1, _, _, _, 2, _, 3, 3, 3, _, 2, _, 1, _, _, 1, _, 1, _, _, _, 1],
    [1, _, _, _, _, _, 2, _, _, 3, _, _, 2, _, 1, _, 1, _, _, 1, _, 1, _, 1],
    [1, _, _, 3, 3, _, 2, _, _, 3, _, 2, _, _, _, _, _, _, 3, _, _, _, _, 1],
    [1, _, _, _, 3, _, _, _, _, _, _, 2, _, 3, 3, _, 1, _, 3, 1, 1, _, 1, 1],
    [1, _, 3, _, _, _, 3, 3, _, 3, _, 2, _, 3, 3, _, 1, _, 3, 2, 1, _, _, 1],
    [1, _, _, _, _, 3, _, 3, _, _, 3, _, _, _, _, _, 1, _, _, 2, _, _, _, 1],
    [1, _, 1, _, 3, _, _, _, _, 3, _, _, 2, _, 1, 1, 1, 1, _, 2, _, 2, _, 1],
    [1, _, _, _, _, _, 1, 1, _, _, _, 2, 2, _, _, _, _, 1, _, _, 2, 2, _, 1],
    [1, _, 1, 1, 1, _, _, 1, 1, _, _, _, _, 2, 2, 2, _, _, _, 2, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, 1, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

WORLD_WIDTH = len(matrix_map[0]) * TILE #для вычисления луча в рейкасте
WORLD_HEIGHT = len(matrix_map) * TILE
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32) #словарик, в котором ключи это кортежи с типом инт32, значения инт того же типа (оптимизация)
mini_map = set()
collision_walls = []
for j, row in enumerate(matrix_map): #элементы списка карты это у, элементы строк - х
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            collision_walls.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 1:
                world_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                world_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                world_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                world_map[(i * TILE, j * TILE)] = 4
            

