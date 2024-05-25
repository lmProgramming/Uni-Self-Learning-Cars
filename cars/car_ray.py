import pygame as pg
from pygame.math import Vector2
from typing import List, Callable
import vector_math
from map_scripts.map import Wall
from pygame_tools import lerp_color, aaline

CLOSE_COLOR = pg.Color(193, 0, 0, 255)
FAR_COLOR = pg.Color(0, 0, 0, 0)
RAY_WIDTH = 3

class CarRay:
    def __init__(self, car, angle_bias: float, length: float, processing_function: Callable[[float, float], float]) -> None:
        self.car = car
        self.angle_bias: float = angle_bias
        self.length: float = length
        self.color: pg.Color = FAR_COLOR
        self.last_distance: float = 0
        self.last_point: Vector2 | None = None
        self.processing_function: Callable[[float, float], float] = processing_function
        self.processed_last_distance: float = 1

    def get_origin_position(self):
        return self.car.get_centre_position()
    
    def get_end_position(self):
        return self.get_origin_position() + vector_math.position_from_length_and_angle(-self.car.angle + self.angle_bias, self.length)

    def find_distance_to_wall(self, wall: Wall) -> tuple[bool, Vector2, float]:
        point: Vector2 = vector_math.find_lines_intersection(
            self.get_origin_position(), 
            self.get_end_position(), 
            wall.start_position, 
            wall.end_position)

        distance: float = self.length if point is None else point.distance_to(self.get_origin_position())

        return point is not None, point, distance
    
    def find_distance_to_walls_quick(self, walls: List[Wall]) -> tuple[Vector2, float]:  
        wall_start_positions: List[Vector2] = [wall.start_position for wall in walls]
        wall_end_positions: List[Vector2] = [wall.end_position for wall in walls]
        intersection_point, closest_distance = vector_math.find_closest_line_intersection(
            self.get_origin_position(), 
            self.get_end_position(), 
            wall_start_positions, 
            wall_end_positions, 
            self.length)
        return intersection_point, closest_distance
    
    def draw_debug(self, win) -> None:       
        print(self.get_debug_color())
        aaline(win, self.get_debug_color(), self.get_origin_position(), self.last_point if self.last_point is not None else self.get_end_position(), RAY_WIDTH)
    
    def get_debug_color(self) -> pg.Color:    
        return lerp_color(CLOSE_COLOR, FAR_COLOR, self.processed_last_distance)

    def set_last_distance(self, distance: float) -> None:
        self.last_distance = distance
        self.processed_last_distance = self.processing_function(distance, self.length)
        
    def set_last_point(self, point: Vector2 | None) -> None:
        self.last_point = point
        
    def draw(self, win) -> None:      
        pg.draw.line(win, self.color, self.get_origin_position(), self.get_end_position(), RAY_WIDTH)