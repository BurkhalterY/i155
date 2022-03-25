import pygame
from joystick import refresh_joysticks, Joystick
from player import Player

pygame.init()

PLAYER_1_COLOR = (0, 0, 255)
PLAYER_2_COLOR = (255, 255, 0)
BG_COLOR = (0, 0, 0)

width = 500
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TRON BATTLE 1V1 OMG")

playing = True

j1 = Joystick(0)
j2 = Joystick(1)

p1 = Player(30, width / 2 - 30 / 2, 0, 0, PLAYER_1_COLOR)
p2 = Player(width - 30 * 2, width / 2 - 30 / 2, 0, 0, PLAYER_2_COLOR)

screen.fill(BG_COLOR)
while playing:
    refresh_joysticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            j1.add_event(pygame.JOYAXISMOTION, p1.move)
            j2.add_event(pygame.JOYAXISMOTION, p2.move)

    # draw players
    pygame.draw.rect(screen, p1.color, pygame.Rect(p1.x, p1.y, p1.size, p1.size))
    pygame.draw.rect(screen, p2.color, pygame.Rect(p2.x, p2.y, p2.size, p2.size))

    pygame.display.flip()

pygame.quit()
