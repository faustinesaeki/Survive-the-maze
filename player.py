from settings import *
import pygame
import math
from map import collision_walls

class Player:
    def __init__(self, sprites):
        self.x, self.y = pl_position
        self.sprites = sprites
        self.angle = pl_angle
        self.sensitivity = 0.0001
        self.side = 50 #сторона "квадрата игрока"
        self.rect =  pygame.Rect(*pl_position, self.side, self.side)
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]
        self.collision_list = collision_walls + self.collision_sprites

    @property #возвращает поизицию по х и у
    def pos(self):
        return (self.x, self.y)
    
    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy() #формирование следующего шага, который будет смотреть столкновение со стеной
        next_rect.move_ip(dx, dy)
        slams_against_the_wall = next_rect.collidelistall(self.collision_list)

        if len(slams_against_the_wall): #поиск стороны столкновения
            delta_x, delta_y = 0, 0
            for slam_index in slams_against_the_wall:
                slam_rect = self.collision_list[slam_index]
                if dx > 0: #пересечения со стенами
                    delta_x += next_rect.right - slam_rect.left
                else:
                    delta_x += slam_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - slam_rect.top
                else:
                    delta_y += slam_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10: #суммарная величина пересечений по двум осям, я вам запрещаю заходить в текстуры
                dx,dy = 0,0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy


    
    def movement(self):
        self.keys_control()
        # self.mouse_control()
        self.rect.center = self.x, self.y #перемещение центра "квадрата", за который может выступить игрок
        self.angle %= D_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()
        if keys[pygame.K_w]:
            dx = pl_speed * cos_a
            dy = pl_speed * sin_a
            self.detect_collision(dx,dy)
        if keys[pygame.K_s]:
            dx = -pl_speed * cos_a
            dy = -pl_speed * sin_a
            self.detect_collision(dx,dy)
        if keys[pygame.K_a]:
            dx = pl_speed * sin_a
            dy = -pl_speed * cos_a
            self.detect_collision(dx,dy)
        if keys[pygame.K_d]:
            dx = -pl_speed * sin_a
            dy = pl_speed * cos_a
            self.detect_collision(dx,dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.03
        if keys[pygame.K_RIGHT]:
            self.angle += 0.03

    # def mouse_control (self):
    #     if pygame.mouse.get_focused():
    #         difference = pygame.mouse.get_pos()[0] #расчёт разницы между положением текущей координаты х и середины экрана
    #         pygame.mouse.set_pos((H_W, H_H)) #возвращение курсора назад в центр экрана
    #         self.angle += difference * self.sensitivity #прибавление разницы к углу с учётом чувствительности мыши