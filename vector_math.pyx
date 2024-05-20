from pygame.math import Vector2
import math

def find_lines_intersection(A: Vector2, B: Vector2, C: Vector2, D: Vector2):
    cdef float s10_x = B[0] - A[0]
    cdef float s10_y = B[1] - A[1]
    cdef float s32_x = D[0] - C[0]
    cdef float s32_y = D[1] - C[1]

    cdef float denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0:
        return None

    cdef bint denom_is_positive = denom > 0

    cdef float s02_x = A[0] - C[0]
    cdef float s02_y = A[1] - C[1]

    cdef float s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive:
        return None

    cdef float t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive:
        return None

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive:
         return None

    cdef float t = t_numer / denom

    point = Vector2(A[0] + (t * s10_x), A[1] + (t * s10_y))

    return point

def find_intersection_points(Vector2 starting_point, Vector2 wall_starting_points, Vector2 wall_ending_points):
    ...

def position_from_length_and_angle(float angle, float length):
    cdef float delta_y = length * math.cos(math.radians(angle))
    cdef float delta_x = length * math.sin(math.radians(angle))

    return Vector2(delta_x, delta_y)

# python setup.py build_ext --inplace