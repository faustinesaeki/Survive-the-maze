import pygame
from settings import *
from player import Player
from sprite import *
from ray_casting import ray_casting_walls
from drawing import Drawing
from interaction import Interaction

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_map = pygame.Surface(MINIMAP_RES)

sprites = Sprites()
clock = pygame.time.Clock()
start = 12000 #время в милисекундах
player = Player(sprites)
drawing = Drawing(screen, screen_map, clock)
interaction = Interaction(player, sprites, drawing)

drawing.menu()
pygame.mouse.set_visible(False)

interaction.play_music()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill(BLACK)

    drawing.background(player.angle)
    walls = ray_casting_walls(player, drawing.textures)
    drawing.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    drawing.mini_map(player)
    interaction.npc_action()
    start -= 1
    if start <= 0:
        interaction.win()
    interaction.check_defeat()
    pygame.display.flip()
    clock.tick(FPS)