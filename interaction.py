from settings import *
from map import world_map, WORLD_HEIGHT, WORLD_WIDTH
from ray_casting import mapping
import math
import pygame
from numba import njit
from random import randint

@njit(fastmath=True, cache=True)
def ray_casting_npc (npc_x, npc_y, world_map, player_pos): #видимость игрока для нпс, один луч
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = math.sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    #вертикали
    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * TILE

    #горизонтали
    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing
        self.sound = pygame.mixer.Sound('sounds/vaszametili.mp3')
        self.sound_trigger = True

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'hostile':
                if ray_casting_npc(obj.x, obj.y, world_map, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                    if obj.weezer:
                        if obj.distance_to_sprite < 6 and self.sound_trigger:
                            self.sound_trigger = False
                            self.sound.play()
                            self.player.x = randint(0, WORLD_WIDTH)
                            self.player.y = randint(0, WORLD_HEIGHT)
                            break
                else:   
                    obj.npc_action_trigger = False
                    self.sound_trigger = True

    def npc_move(self, obj):
        if abs(obj.distance_to_sprite) >= 1:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1.5 if dx < 0 else obj.x - 1.5
            obj.y = obj.y + 1.5 if dy < 0 else obj.y - 1.5
    
    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sounds/theme.mp3')
        pygame.mixer.music.play(10)
        pygame.mixer.music.set_volume(0.07)

    def win(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/win.mp3')
        pygame.mixer.music.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.drawing.win()
    def check_defeat(self):
        for obj in self.sprites.list_of_objects:
            if abs(obj.distance_to_sprite) <= 2 and not obj.weezer: 
                pygame.mixer.music.stop()
                pygame.mixer.music.load('sounds/lose.mp3')
                pygame.mixer.music.play()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                    self.drawing.defeat()

            