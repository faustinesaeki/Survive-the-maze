import pygame
from settings import *
from ray_casting import ray_casting
from map import mini_map
from random import randrange
import sys

class Drawing:   #для отрисовки элемента
    def __init__(self, screen, screen_map, clock):
        self.screen = screen
        self.screen_map = screen_map
        self.clock = clock
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.font_win = pygame.font.SysFont('font/font.ttf', 96, bold=True)
        self.textures = {1: pygame.image.load('textures/1.jpg').convert(),
                         2: pygame.image.load('textures/2.jpg').convert(),
                         3: pygame.image.load('textures/3.png').convert(),
                        'S': pygame.image.load('textures/sky.png').convert()
                         }
        
        self.menu_trigger = True
        self.menu_picture = pygame.image.load('textures/bg.png').convert()

    def background(self, angle): #отрисовка заднего фона
        sky_offset = -10 * math.degrees(angle) % WIDTH #отрисовка неба, которое зависит от угла поворота игрока
        self.screen.blit(self.textures['S'], (sky_offset, 0))
        self.screen.blit(self.textures['S'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['S'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.screen, FLOOR, (0, H_H, WIDTH, H_H))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True): #сортировка по глубине от дальних, отрисовка приколов
            if obj[0]:
                _, object, object_pos = obj #удаление лишних значений для спрайтов
                self.screen.blit(object, object_pos)

    def mini_map(self, player): #миникарта
        self.screen_map.fill(BACK_MINI)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.screen_map, MINI_PL, (map_x, map_y), (map_x + 12 * math.cos(player.angle),
                                                 map_y + 12 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.screen_map, MINI_PL, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.screen_map, BLACK, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.screen_map, MAP_POS)

    def win(self):
        render = self.font_win.render(f'CONGRATULATIONS!\npress esc - to leave, f1 to retry', 1, (randrange(40,120),0,0))
        rect = pygame.Rect(0,0,1000,300)
        rect.center = H_W, H_H
        pygame.draw.rect(self.screen, BLACK, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx - 400, rect.centery - 90))
        pygame.display.flip()
        self.clock.tick(15)

    def defeat(self):
        render = self.font_win.render(f'TRY AGAIN\n(press f1)', 1, (randrange(40,120),0,0))
        rect = pygame.Rect(0,0,1000,300)
        rect.center = H_W, H_H
        pygame.draw.rect(self.screen, BLACK, rect, border_radius=50)
        self.screen.blit(render, (rect.centerx-50, rect.centery - 90))
        pygame.display.flip()
        self.clock.tick(15)

    def menu(self):
        x = 0
        button_font = pygame.font.Font('font/font.ttf', 72)
        label_font = pygame.font.Font('font/font.ttf', 100)
        start = button_font.render('START', 1, pygame.Color('white'))
        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = H_W, H_H
        exit = button_font.render('EXIT', 1, pygame.Color('white'))
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = H_W, H_H + 200

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.menu_picture, (0, 0), (x % WIDTH, H_H, WIDTH, HEIGHT))
            x += 1

            pygame.draw.rect(self.screen, BLACK, button_start, border_radius=25, width=10)
            self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))

            pygame.draw.rect(self.screen, BLACK, button_exit, border_radius=25, width=10)
            self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

            color = randrange(40)
            label = label_font.render('Surive the Maze', 1, (color, color, color))
            self.screen.blit(label, (15, -30))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLACK, button_start, border_radius=25)
                self.screen.blit(start, (button_start.centerx - 130, button_start.centery - 70))
                if mouse_click[0]:
                    self.menu_trigger = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, BLACK, button_exit, border_radius=25)
                self.screen.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            self.clock.tick(20)