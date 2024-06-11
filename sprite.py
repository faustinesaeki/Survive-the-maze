import pygame
from settings import *
from collections import deque


class Sprites:
    def __init__(self):
        self.parameters ={
            'cat':{
                'sprite' : pygame.image.load('sprites/kitty.png').convert_alpha(),
                'viewing_angles' : None,
                'shift' : 0.2, #сдвиг
                'scale' : (0.7, 0.7), #масштаб
                'animation' : deque(
                    [pygame.image.load(f'sprites/kitty.png').convert_alpha() for i in range(1)]),
                'animation_dist' : 800,
                'animation_speed' : 1,
                'blocked' : True,
                'flag' : 'hostile',
                'action' : deque(
                    [pygame.image.load(f'sprites/kitty1.png').convert_alpha() for i in range(1)]),
                'side' : 50,
                'weezer' : False
            },
            'rick':{
                'sprite' : pygame.image.load('sprites/rick.png').convert_alpha(),
                'viewing_angles' : None,
                'shift' : -0.1, #сдвиг
                'scale' : (2,2), #масштаб
                'animation' : deque(
                    [pygame.image.load(f'sprites/anim/{i}.png').convert_alpha() for i in range(27)]),
                'animation_dist' : 800,
                'animation_speed' : 10,
                'blocked' : True,
                'flag' : 'hostile',
                'action' : deque(
                    [pygame.image.load(f'sprites/anim/{i}.png').convert_alpha() for i in range(27)]),
                'side' : 50,
                'weezer' : False
            },
            'wee':{
                'sprite' : pygame.image.load('sprites/run.png').convert_alpha(),
                'viewing_angles' : None,
                'shift' : -0.2, #сдвиг
                'scale' : (1.7, 1.7), #масштаб
                'animation' : deque(
                    [pygame.image.load(f'sprites/run.png').convert_alpha() for i in range(1)]),
                'animation_dist' : 800,
                'animation_speed' : 1,
                'blocked' : True,
                'flag' : 'hostile',
                'action' :  deque(
                    [pygame.image.load(f'sprites/run1.png').convert_alpha() for i in range(1)]),
                'side' : 85,
                'weezer' : True
            }
        }
        self.list_of_objects = [
            SpriteObject(self.parameters['cat'], (9.1, 11)),
            SpriteObject(self.parameters['cat'], (20.2, 14.8)),
            SpriteObject(self.parameters['cat'], (9, 4.8)),
            SpriteObject(self.parameters['cat'], (10, 10)),
            SpriteObject(self.parameters['rick'], (11, 20)),
            SpriteObject(self.parameters['wee'], (12.34, 13.54)),
            SpriteObject(self.parameters['cat'], (15, 7)),
            SpriteObject(self.parameters['cat'], (10, 20)),
            SpriteObject(self.parameters['cat'], (1, 4)),
            SpriteObject(self.parameters['cat'], (8, 16)),
    ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite'].copy()
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_speed = parameters['animation_speed']
        self.animation_dist = parameters['animation_dist']
        self.animation_count = 0
        self.blocked = parameters['blocked'] #проходимость
        self.action = parameters['action']
        self.flag = parameters['flag']
        self.side = 30 #квадрат спрайта
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.npc_action_trigger = False
        self.side = parameters['side']
        self.weezer = parameters['weezer']
        
        if self.viewing_angles:
            if len(self.object) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
            dx, dy = self.x - player.x, self.y - player.y
            self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

            self.theta = math.atan2(dy, dx)
            gamma = self.theta - player.angle
            if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
                gamma += D_PI
            self.theta -= 1.4 * gamma
            delta_rays = int(gamma / DELTA_ANGLE)
            current_ray = C_RAY + delta_rays
            self.distance_to_sprite *= math.cos(H_FOV - current_ray * DELTA_ANGLE)

            fake_ray = current_ray + F_RAY
            if 0 <= fake_ray <= F_RAY_RANGE and self.distance_to_sprite > 30:

                self.proj_height = min(int(PROJ_COFF / self.distance_to_sprite), X2_HEIGHT)

                sprite_width = int(self.proj_height * self.scale[0]) #масштаб по осям
                sprite_height = int(self.proj_height * self.scale [1])
                h_sprite_height = sprite_height // 2
                h_sprite_width = sprite_width // 2
                shift = h_sprite_height * self.shift

                if self.npc_action_trigger:
                    sprite_object = self.npc_acting()
                else:
                    self.object = self.visibility()
                    sprite_object = self.sprite_animate()

                #позиция и масштаб
                sprite_pos = (current_ray * SCALE - h_sprite_width, H_H - h_sprite_height + shift)
                sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
                return (self.distance_to_sprite, sprite, sprite_pos)
            else:
                return (False,)
            
    def sprite_animate(self):
        #анимация
        if self.animation and self.distance_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_speed and self.animation_count < self.animation_speed:
                self.animation_count += 1
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.object
    
    def visibility(self):
        #подбор спрайта под угол
        if self.viewing_angles:
            if self.theta < 0:
                self.theta += D_PI
            self.theta = 360 - int(math.degrees(self.theta))
            for angles in self.sprite_angles:
                if self.theta in angles:
                    return self.sprite_positions[angles]
        return self.object
    
    def npc_acting(self):
        sprite_object = self.action[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.action.rotate()
            self.animation_count = 0
        return sprite_object

