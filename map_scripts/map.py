import pygame as pg
from pygame.math import Vector2
from vector_math import point_left_or_right_of_line # type: ignore

WALL_COLOR = pg.Color(79, 82, 178)
GATE_COLOR = pg.Color(216, 216, 216)

class Wall:
    def __init__(self, x1, y1, x2, y2, thickness=2) -> None:
        self.start_position = Vector2(x1, y1)
        self.end_position = Vector2(x2, y2)
        self.thickness = thickness

    def draw(self, win) -> None:
        pg.draw.line(win, WALL_COLOR, self.start_position, self.end_position, self.thickness)

class Gate:
    def __init__(self, num: int, x1, y1, x2, y2, thickness=2) -> None:
        self.start_position = Vector2(x1, y1)
        self.end_position = Vector2(x2, y2)
        self.thickness: int = thickness
        self.num: int = num

    def get_centre_position(self) -> Vector2:
        return self.start_position + (self.end_position - self.start_position) / 2
    
    def calculate_side(self, point: Vector2) -> int:
        return point_left_or_right_of_line(self.start_position, self.end_position, point)        

    def check_if_inside(self, position) -> bool:
        x1: float
        x2: float
        y1: float
        y2: float
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

    def draw(self, win) -> None:
        pg.draw.line(win, GATE_COLOR, self.start_position, self.end_position, self.thickness)
        
