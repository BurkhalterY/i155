import pygame
from joystick import Joystick
from player import Player

pygame.init()

PLAYER_1_COLOR = (0, 0, 255)
PLAYER_2_COLOR = (255, 255, 0)
BG_COLOR = (0, 0, 0)

width = 480
height = 320
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TRON BATTLE 1V1 OMG")

playing = True

p1 = Player(40, height / 2 - 30 / 2, 0, 0, PLAYER_1_COLOR)
p2 = Player(width - 30 * 2, height / 2 - 30 / 2, 0, 0, PLAYER_2_COLOR)

screen.fill(BG_COLOR)

j1 = Joystick(0)
j2 = Joystick(1)

#j1.add_event(pygame.JOYAXISMOTION, lambda event: p1.move())
#j2.add_event(pygame.JOYAXISMOTION, lambda event: p2.move())
j1.add_event(pygame.JOYAXISMOTION, lambda event: print(event))

while playing:
    # Initializes the joysticks if they aren't (needed for pygame)
    for i in range(pygame.joystick.get_count()):
        j = pygame.joystick.Joystick(i)
        j.get_init() or j.init()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.JOYAXISMOTION:
            j1._call_event(pygame.JOYAXISMOTION, event)
            j2._call_event(pygame.JOYAXISMOTION, event)
        if event.type == pygame.JOYBALLMOTION:
            j1._call_event(pygame.JOYBALLMOTION, event)
            j2._call_event(pygame.JOYBALLMOTION, event)
        if event.type == pygame.JOYBUTTONDOWN:
            j1._call_event(pygame.JOYBUTTONDOWN, event)
            j2._call_event(pygame.JOYBUTTONDOWN, event)
        if event.type == pygame.JOYBUTTONUP:
            j1._call_event(pygame.JOYBUTTONUP, event)
            j2._call_event(pygame.JOYBUTTONUP, event)
        if event.type == pygame.JOYHATMOTION:
            j1._call_event(pygame.JOYHATMOTION, event)
            j2._call_event(pygame.JOYHATMOTION, event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                p1.dir_x = -1
                p1.dir_y = 0
            elif event.key == pygame.K_RIGHT:
                p1.dir_x = 1
                p1.dir_y = 0
            elif event.key == pygame.K_DOWN:
                p1.dir_x = 0
                p1.dir_y = 1
            elif event.key == pygame.K_UP:
                p1.dir_x = 0
                p1.dir_y = -1
            if event.key == pygame.K_a:
                p2.dir_x = -1
                p2.dir_y = 0
            elif event.key == pygame.K_d:
                p2.dir_x = 1
                p2.dir_y = 0
            elif event.key == pygame.K_s:
                p2.dir_x = 0
                p2.dir_y = 1
            elif event.key == pygame.K_w:
                p2.dir_x = 0
                p2.dir_y = -1

    p1.move()
    p2.move()

    # draw players
    pygame.draw.rect(screen, p1.color, pygame.Rect(p1.x, p1.y, p1.size, p1.size))
    pygame.draw.rect(screen, p2.color, pygame.Rect(p2.x, p2.y, p2.size, p2.size))

    pygame.display.flip()

pygame.quit()
