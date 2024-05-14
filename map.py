import pygame as pg
from pygame.math import Vector2

class Wall:
    def __init__(self, x1, y1, x2, y2, thickness=6):
        self.start_position = Vector2(x1, y1)
        self.end_position = Vector2(x2, y2)
        self.thickness = thickness

    def draw(self, win):
        pg.draw.line(win, (0, 0, 0), self.start_position, self.end_position, self.thickness)

class Gate:
    def __init__(self, num, x1, y1, x2, y2, thickness=6):
        self.start_position = Vector2(x1, y1)
        self.end_position = Vector2(x2, y2)
        self.thickness = thickness
        self.num = num

    def get_centre_position(self):
        return self.start_position + (self.end_position - self.start_position) / 2

    def check_if_inside(self, position):
        if self.start_position.x < self.end_position.x:
            x1 = self.start_position.x
            x2 = self.end_position.x
        else:
            x1 = self.end_position.x
            x2 = self.start_position.x
        
        if self.start_position.y < self.end_position.y:
            y1 = self.start_position.y
            y2 = self.end_position.y
        else:
            y1 = self.end_position.y
            y2 = self.start_position.y

        return position.x > x1 and \
               position.y > y1 and \
               position.x < x2 and \
               position.y < y2

    def draw(self, win):
        pg.draw.line(win, (0, 0, 255), self.start_position, self.end_position, self.thickness)
        
