import pygame as pg
from pygame.key import ScancodeWrapper
from pygame.math import Vector2
import math
from typing import List
import os
import vector_math
from abc import ABC, abstractmethod
from neat import DefaultGenome

CAR_IMG = pg.image.load(os.path.join("imgs", "car_img.png"))

CAR_WIDTH = CAR_IMG.get_width()
CAR_HEIGHT = CAR_IMG.get_height()

RAY_DISTANCE_KILL = 10

WHEEL_TURN = 60
WHEEL_TURN_SPEED = 3    

class Car(ABC):
    def __init__(self, x, y, starting_angle) -> None:
        self.position = Vector2(x, y)
        self.angle = starting_angle
        self.speed = 0
        self.acceleration = 0.3
        self.back_acceleration_multiplier: float = 1 / 3
        self.lines: List[CarRay] = []
        self.dead = False
        self.last_gate = None
        self.direction = None
        self.rect: pg.Rect = pg.Rect(x, y, CAR_WIDTH, CAR_HEIGHT)

    def die(self):
        self.dead = True

    def check_if_in_next_gate(self, gates):
        if self.last_gate is None:
            return self.check_if_in_gate(gates, 0, dir=1) or self.check_if_in_gate(gates, -1, dir=-1)
        return self.check_if_in_gate(gates, (abs(self.last_gate) + self.direction) % len(gates), dir)

    def check_if_in_gate(self, gates, gate_num, dir):
        gate = gates[gate_num]

        if gate.check_if_inside(self.get_centre_position()):
            if self.direction is None:
                self.direction = dir
            self.last_gate = gate.num
            return True
        return False
    
    def get_shortest_last_distance(self) -> float:
        return min([line.last_distance for line in self.lines])            

    def calculate_line_distances(self, walls) -> list[float]:        
        results = []

        for line in self.lines:
            lowest_distance: float = line.length
            lowest_point: Vector2 | None = None
            for wall in walls:
                _, point, distance = line.find_distance_to_wall(wall)
                if distance < lowest_distance:                    
                    lowest_distance = distance
                    lowest_point = point
                
            results.append(lowest_distance / line.length)    
            
            line.set_last_distance(lowest_distance)      
            line.set_last_point(lowest_point)      
                
        return results
    
    @abstractmethod    
    def get_reward(self, reward: float):
        ...
        
    @abstractmethod            
    def get_score(self):
        ...
    
    def check_if_hit_wall(self):
        if min([line.last_distance for line in self.lines]) < RAY_DISTANCE_KILL:
            self.die()
    
    @abstractmethod
    def get_desired_movement(self) -> Vector2:
        ...

    def get_centre_position(self):
        return self.position + Vector2(CAR_WIDTH / 2, CAR_HEIGHT / 2)

    def move_forward(self, force):
        normalized_force = force * 2 - 1

        self.speed += normalized_force * self.acceleration * (1 if force >= 0 else self.back_acceleration_multiplier)

    def generate_rays(self, ray_count, ray_length) -> None:
        for i in range(0, 360, 360 // ray_count):
            self.lines.append(CarRay(self, i, ray_length))

    def steer(self, way):
        wheel_turn_coefficient = math.sqrt(abs(self.speed))

        if way < 0.5:
            self.angle -= WHEEL_TURN_SPEED * (0.5 - way) * wheel_turn_coefficient
        if way > 0.5:
            self.angle += WHEEL_TURN_SPEED * (way - 0.5) * wheel_turn_coefficient

    def move(self):
        self.speed *= 0.94

        if self.angle < -180:
            self.angle = 180
        if self.angle > 180:
            self.angle = -180
        
        delta_y = -self.speed * math.cos(math.radians(self.angle))
        delta_x = self.speed * math.sin(math.radians(self.angle))

        self.position += Vector2(delta_x, delta_y)

    def check_intersections(self, walls, win):
        ...

    def draw(self, win):
        rotated_image = pg.transform.rotate(CAR_IMG, -self.angle)
        self.rect = rotated_image.get_rect(center=CAR_IMG.get_rect(topleft=(self.position.x, self.position.y)).center)
        win.blit(rotated_image, self.rect.topleft)
        
class AICar(Car):    
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.genome: DefaultGenome
        
    def set_neural_net(self, neural_net):
        self.neural_net = neural_net
    
    def get_desired_movement(self) -> Vector2:      
        inputs: List[float] = [ray.last_distance for ray in self.lines]  
        outputs = self.neural_net.activate(inputs)
        
        return outputs
    
    def get_reward(self, reward: float):
        self.genome.fitness += reward
        
    def get_score(self):
        return self.genome.fitness
    
class HumanCar(Car):
    def __init__(self, *args):
        super().__init__(*args)
        self.score = 0
        
    def get_desired_movement(self) -> Vector2:
        keys: ScancodeWrapper = pg.key.get_pressed()
        
        outputs = Vector2(0.5, 0.5)                    
        if keys[pg.K_w]:
            outputs.x += 0.5
        if keys[pg.K_s]:
            outputs.x -= 0.5

        if keys[pg.K_a]:
            outputs.y -= 0.5
        if keys[pg.K_d]:
            outputs.y += 0.5
            
        return outputs
    
    def get_reward(self, reward: float):
        if reward > 1:
            print("high reward")
            
        self.score += reward
    
    def get_score(self):
        return self.score

class CarRay:
    def __init__(self, car: Car, angle_bias: float, length: float) -> None:
        self.car: Car = car
        self.angle_bias: float = angle_bias
        self.length: float = length
        self.color = pg.Color(0, 0, 0, 255)
        self.last_distance: float = 0
        self.last_point: Vector2 | None = None

    def get_origin_position(self):
        return self.car.get_centre_position()
    
    def get_end_position(self):
        return self.get_origin_position() + vector_math.position_from_length_and_angle(-self.car.angle + self.angle_bias, self.length)

    def find_distance_to_wall(self, wall) -> tuple[bool, Vector2, float]:
        point: Vector2 = vector_math.find_lines_intersection(self.get_origin_position(), self.get_end_position(), wall.start_position, wall.end_position)

        distance: float = self.length if point is None else point.distance_to(self.get_origin_position())

        return point is not None, point, distance
    
    def draw_debug(self, win) -> None:       
        pg.draw.line(win, self.color, self.get_origin_position(), self.last_point if self.last_point is not None else self.get_end_position(), 3)
    
    def set_debug_color(self) -> None:        
        color_value = int(255 * (self.last_distance / self.length))
        self.color = pg.Color(255, color_value, color_value)  

    def set_last_distance(self, distance: float) -> None:
        self.last_distance: float = distance
        
    def set_last_point(self, point: Vector2) -> None:
        self.last_point = point
        
    def draw(self, win) -> None:      
        pg.draw.line(win, self.color, self.get_origin_position(), self.get_end_position(), 3)
        