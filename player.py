import pygame.event

class Player:
    def __init__(self, x, y, dir_x, dir_y, color):
        self.x = x
        self.y = y
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color
        self.speed = 2
        self.size = 10

    def move(self):
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

    def change_direction(self, event):
        print(event)
        if event.axis == 0:
            self.dir_x = round(event.value)
        elif event.axis == 1:
            self.dir_y = round(event.value)
