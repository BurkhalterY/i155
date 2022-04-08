import pygame
from joystick import Joystick
from player import Player
import os

pygame.init()
os.environ["DISPLAY"] = ":0"
pygame.display.init()

PLAYER_1_COLOR = (0, 0, 255)
PLAYER_2_COLOR = (255, 255, 0)
BG_COLOR = (0, 0, 0)

screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("TRON BATTLE 1V1 OMG")

playing = True

size = width / 50
offset = 30

p1_default_x = width - offset * 2
p1_default_y = height / 2 - offset / 2
p2_default_x = size * 2
p2_default_y = height / 2 - offset / 2
p1 = Player(p1_default_x, p1_default_y, 0, 0, size, PLAYER_1_COLOR)
p2 = Player(p2_default_x, p2_default_y, 0, 0, size, PLAYER_2_COLOR)

screen.fill(BG_COLOR)

j1 = Joystick(0)
j2 = Joystick(1)

#j1.add_event(pygame.JOYAXISMOTION, lambda event: p1.move())
#j2.add_event(pygame.JOYAXISMOTION, lambda event: p2.move())
j1.add_event(pygame.JOYAXISMOTION, lambda event: p1.change_direction(event))
j2.add_event(pygame.JOYAXISMOTION, lambda event: p2.change_direction(event))

clock = pygame.time.Clock()

def reset():
    print('reset')
    # Player 1
    # p1.x = p1_default_x
    # p1.y = p1_default_y
    # p1.dir_x = 0
    # p1.dir_y = 0

    # Player 2
    # p2.x = p2_default_x
    # p2.y = p2_default_y
    # p2.dir_x = 0
    # p2.dir_y = 0

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

    if -1 != p1.rect.collidelist(p2.rects) or -1 != p1.rect.collidelist(p1.rects[:-20]):
        print("p1 meurt")
        reset()

    if -1 != p2.rect.collidelist(p1.rects) or -1 != p2.rect.collidelist(p2.rects[:-20]):
        print("p2 meurt")
        reset()

    # draw players
    p1.draw(screen)
    p2.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
