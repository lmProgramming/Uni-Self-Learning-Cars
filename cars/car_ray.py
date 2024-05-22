import pygame as pg
from pygame.math import Vector2
from typing import List, Callable
import vector_math
from maps.map import Wall

class CarRay:
    def __init__(self, car, angle_bias: float, length: float, processing_function: Callable[[float, float], float]) -> None:
        self.car = car
        self.angle_bias: float = angle_bias
        self.length: float = length
        self.color = pg.Color(0, 0, 0, 255)
        self.last_distance: float = 0
        self.last_point: Vector2 | None = None
        self.processing_function: Callable[[float, float], float] = processing_function
        self.processed_last_distance: float 

    def get_origin_position(self):
        return self.car.get_centre_position()
    
    def get_end_position(self):
        return self.get_origin_position() + vector_math.position_from_length_and_angle(-self.car.angle + self.angle_bias, self.length)

    def find_distance_to_wall(self, wall: Wall) -> tuple[bool, Vector2, float]:
        point: Vector2 = vector_math.find_lines_intersection(self.get_origin_position(), self.get_end_position(), wall.start_position, wall.end_position)

        distance: float = self.length if point is None else point.distance_to(self.get_origin_position())

        return point is not None, point, distance
    
    def draw_debug(self, win) -> None:       
        pg.draw.line(win, self.color, self.get_origin_position(), self.last_point if self.last_point is not None else self.get_end_position(), 3)
    
    def set_debug_color(self) -> None:        
        color_value = int(255 * (self.processed_last_distance))
        self.color = pg.Color(255, color_value, color_value)  

    def set_last_distance(self, distance: float) -> None:
        self.last_distance = distance
        self.processed_last_distance = self.processing_function(distance, self.length)
        
    def set_last_point(self, point: Vector2 | None) -> None:
        self.last_point = point
        
    def draw(self, win) -> None:      
        pg.draw.line(win, self.color, self.get_origin_position(), self.get_end_position(), 3)