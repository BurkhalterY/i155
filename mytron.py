import pygame
from joystick import Joystick
from player import Player
import os


os.environ["DISPLAY"] = ":0"
pygame.init()
pygame.display.init()
pygame.joystick.init()

PLAYER_1_COLOR = (0, 0, 255)
PLAYER_2_COLOR = (255, 255, 0)
BG_COLOR = (0, 0, 0)
MSG_COLOG = (255, 0, 0)

screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)
screen_rect = screen.get_rect()
width, height = pygame.display.get_surface().get_size()
pygame.display.set_caption("TRON BATTLE 1V1 OMG")

size = width / 50
p1_default_x = size * 4
p2_default_x = width - size * 5
p1_default_y = p2_default_y = (height - size) / 2

pygame.font.init()
font_msg = pygame.font.SysFont('monospace', 24, bold=True)
font_scores = pygame.font.SysFont('monospace', 48, bold=True)

clock = pygame.time.Clock()


class Tron:
    def __init__(self):
        self.playing = True
        self.joysticks_count = 0
        self.p1_score = 0
        self.p2_score = 0
        self.j1 = None
        self.j2 = None
        self.reset()
        self.run()

    def reset(self):
        self.p1 = Player(p1_default_x, p1_default_y, 1, 0, size, PLAYER_1_COLOR)
        self.p2 = Player(p2_default_x, p2_default_y, -1, 0, size, PLAYER_2_COLOR)

    def check_joysticks(self):
        disconnected = False
        while True:
            self.joystick_count = pygame.joystick.get_count()
            if self.joystick_count >= 2:
                # Initializes the joysticks if they aren't (needed for pygame)
                if self.j1 is None and self.j2 is None:
                    self.j1 = Joystick(0)
                    self.j2 = Joystick(1)

                    self.j1.add_event(pygame.JOYAXISMOTION, lambda event: self.p1.change_direction(event.axis, event.value))
                    self.j2.add_event(pygame.JOYAXISMOTION, lambda event: self.p2.change_direction(event.axis, event.value))
                return
            if not disconnected:
                disconnected = True
                text_surface = font_msg.render('Veuillez connecter 2 joysticks pour jouer.', False, MSG_COLOG)
                text_rect = text_surface.get_rect(center=(width / 2, height / 2))
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False

    def run(self):
        screen.fill(BG_COLOR)

        while self.playing:
            self.check_joysticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                if event.type == pygame.JOYAXISMOTION:
                    self.j1.call_event(pygame.JOYAXISMOTION, event)
                    self.j2.call_event(pygame.JOYAXISMOTION, event)
                if event.type == pygame.JOYBALLMOTION:
                    self.j1.call_event(pygame.JOYBALLMOTION, event)
                    self.j2.call_event(pygame.JOYBALLMOTION, event)
                if event.type == pygame.JOYBUTTONDOWN:
                    self.j1.call_event(pygame.JOYBUTTONDOWN, event)
                    self.j2.call_event(pygame.JOYBUTTONDOWN, event)
                if event.type == pygame.JOYBUTTONUP:
                    self.j1.call_event(pygame.JOYBUTTONUP, event)
                    self.j2.call_event(pygame.JOYBUTTONUP, event)
                if event.type == pygame.JOYHATMOTION:
                    self.j1.call_event(pygame.JOYHATMOTION, event)
                    self.j2.call_event(pygame.JOYHATMOTION, event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.p1.change_direction(0, -1)
                    elif event.key == pygame.K_d:
                        self.p1.change_direction(0, 1)
                    elif event.key == pygame.K_s:
                        self.p1.change_direction(1, 1)
                    elif event.key == pygame.K_w:
                        self.p1.change_direction(1, -1)
                    if event.key == pygame.K_LEFT:
                        self.p2.change_direction(0, -1)
                    elif event.key == pygame.K_RIGHT:
                        self.p2.change_direction(0, 1)
                    elif event.key == pygame.K_DOWN:
                        self.p2.change_direction(1, 1)
                    elif event.key == pygame.K_UP:
                        self.p2.change_direction(1, -1)

            self.p1.move()
            self.p2.move()

            p1_is_dead = -1 != self.p1.rect.collidelist(self.p2.rects) \
                   or -1 != self.p1.rect.collidelist(self.p1.rects[:-20]) \
                   or not screen_rect.contains(self.p1.rect)

            p2_is_dead = -1 != self.p2.rect.collidelist(self.p1.rects) \
                      or -1 != self.p2.rect.collidelist(self.p2.rects[:-20]) \
                      or not screen_rect.contains(self.p2.rect)

            if p1_is_dead or p2_is_dead:
                self.reset()
            if p1_is_dead and not p2_is_dead:
                self.p2_score += 1
            if p2_is_dead and not p1_is_dead:
                self.p1_score += 1

            screen.fill(BG_COLOR)

            # draw players
            self.p1.draw(screen)
            self.p2.draw(screen)

            text_surface = font_scores.render(str(self.p1_score), False, PLAYER_1_COLOR)
            text_rect = text_surface.get_rect(center=(p1_default_x, 48))
            screen.blit(text_surface, text_rect)

            text_surface = font_scores.render(str(self.p2_score), False, PLAYER_2_COLOR)
            text_rect = text_surface.get_rect(center=(p2_default_x, 48))
            screen.blit(text_surface, text_rect)

            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
