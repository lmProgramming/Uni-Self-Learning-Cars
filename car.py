import pygame as pg
from pygame.math import Vector2
import math
from typing import List

class Car:
    WHEEL_TURN = 60

    def __init__(self, x, y, starting_angle):
        self.position: Vector2 = Vector2(x, y)
        self.angle = starting_angle
        self.speed = 0
        self.acceleration = 0.3
        self.back_acceleration_multiplier = 1 / 3
        self.lines: List[CarRay] = []
        self.dead = False
        self.last_gate = None
        self.direction = None
        self.genome = None
        self.saved_inputs = []

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

    def get_line_distances(self, borders, refresh):
        if refresh:
            outputs = []

            for line in self.lines:
                lowest_distance = line.base_dist
                for border in borders:
                    _, _, _, distance = line.check_intersection(border)
                    lowest_distance = min(lowest_distance, distance)
                outputs.append(lowest_distance / line.base_dist)     

                col = int(255 * (lowest_distance / line.base_dist))
                line.color = pg.Color(255, col, col)
                
                if lowest_distance < RAY_DISTANCE_KILL:
                    self.die()

            self.saved_inputs = outputs
        return self.saved_inputs           

    def get_centre_position(self):
        return self.position + Vector2(CAR_WIDTH / 2, CAR_HEIGHT / 2)

    def move_forward(self, force):
        normalized_force = force * 2 - 1

        self.speed += normalized_force * self.acceleration * (1 if force >= 0 else self.back_acceleration_multiplier)

    def generate_rays(self):
        for i in range(RAY_COUNT):
            self.lines.append(CarRay(self, 360 / RAY_COUNT * i - 90, RAY_LENGTH))

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

        # self.velocity = Point(self.velocity.x * 0.96, self.velocity.y * 0.96)
        
        delta_y = -self.speed * math.cos(math.radians(self.angle))
        delta_x = self.speed * math.sin(math.radians(self.angle))

        self.position += Vector2(delta_x, delta_y)

    def get_desired_movement(self):
        return 0, 0

    def check_intersections(self, borders, win):
        ...

    def draw(self, win):
        rotated_image = pg.transform.rotate(CAR_IMG, -self.angle)
        new_rect = rotated_image.get_rect(center=CAR_IMG.get_rect(topleft=(self.position.x, self.position.y)).center)
        win.blit(rotated_image, new_rect.topleft)