import pygame.event

class Player:
    def __init__(self, x, y, dir_x, dir_y, size, color):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.size = size
        self.color = color
        self.speed = 3
        self.rect = pygame.Rect(x, y, size, size)
        self.rects = []

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.rect = self.rect.move(self.dir_x * self.speed, self.dir_y * self.speed)
        self.rects.append(self.rect)

    def change_direction(self, axis, value):
        if axis == 0 and not self.dir_x:
            self.dir_x = round(value)
            self.dir_y = 0
        elif axis == 1 and not self.dir_y:
            self.dir_y = round(value)
            self.dir_x = 0

    def draw(self, screen):
        for rect in self.rects:
            pygame.draw.rect(screen, self.color, rect)
