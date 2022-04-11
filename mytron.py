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
MSG_COLOG = (255, 0,0)

screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("TRON BATTLE 1V1 OMG")

size = width / 50
offset = 30

p1_default_x = width - offset * 2
p1_default_y = height / 2 - offset / 2
p2_default_x = size * 2
p2_default_y = height / 2 - offset / 2

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 24, bold=True)

clock = pygame.time.Clock()


class Tron:
    def __init__(self):
        self.playing = True
        self.joysticks_count = 0
        self.reset()
        self.run()

    def reset(self):
        screen.fill(BG_COLOR)
        self.p1 = Player(p1_default_x, p1_default_y, -1, 0, size, PLAYER_1_COLOR)
        self.p2 = Player(p2_default_x, p2_default_y, 1, 0, size, PLAYER_2_COLOR)

    def check_joysticks(self):
        # pygame.joystick.quit()
        # pygame.joystick.init()
        disconnected = False
        while True:
            self.joystick_count = pygame.joystick.get_count()
            if self.joystick_count >= 2:
                # Initializes the joysticks if they aren't (needed for pygame)
                for i in range(self.joystick_count):
                    j = pygame.joystick.Joystick(i)
                    j.get_init() or j.init()
                if disconnected:
                    screen.fill(BG_COLOR)
                return
            disconnected = True
            text_surface = myfont.render("Veuillez connecter 2 joysticks pour jouer.", False, MSG_COLOG)
            text_rect = text_surface.get_rect(center=(width / 2, height / 2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False

    def run(self):
        # j1 = Joystick(0)
        # j2 = Joystick(1)

        #j1.add_event(pygame.JOYAXISMOTION, lambda event: self.p1.move())
        #j2.add_event(pygame.JOYAXISMOTION, lambda event: self.p2.move())
        # j1.add_event(pygame.JOYAXISMOTION, lambda event: self.p1.change_direction(event))
        # j2.add_event(pygame.JOYAXISMOTION, lambda event: self.p2.change_direction(event))

        while self.playing:
            clock.tick(60)
            self.check_joysticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
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
                        self.p1.dir_x = -1
                        self.p1.dir_y = 0
                    elif event.key == pygame.K_RIGHT:
                        self.p1.dir_x = 1
                        self.p1.dir_y = 0
                    elif event.key == pygame.K_DOWN:
                        self.p1.dir_x = 0
                        self.p1.dir_y = 1
                    elif event.key == pygame.K_UP:
                        self.p1.dir_x = 0
                        self.p1.dir_y = -1
                    if event.key == pygame.K_a:
                        self.p2.dir_x = -1
                        self.p2.dir_y = 0
                    elif event.key == pygame.K_d:
                        self.p2.dir_x = 1
                        self.p2.dir_y = 0
                    elif event.key == pygame.K_s:
                        self.p2.dir_x = 0
                        self.p2.dir_y = 1
                    elif event.key == pygame.K_w:
                        self.p2.dir_x = 0
                        self.p2.dir_y = -1

            self.p1.move()
            self.p2.move()

            if -1 != self.p1.rect.collidelist(self.p2.rects) or -1 != self.p1.rect.collidelist(self.p1.rects[:-20]):
                print("p1 meurt")
                self.reset()

            if -1 != self.p2.rect.collidelist(self.p1.rects) or -1 != self.p2.rect.collidelist(self.p2.rects[:-20]):
                print("p2 meurt")
                self.reset()

            # draw players
            self.p1.draw(screen)
            self.p2.draw(screen)

            pygame.display.flip()
        pygame.quit()
