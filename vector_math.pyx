from pygame.math import Vector2
import math
from typing import List

def find_lines_intersection(object A, object B, object C, object D):
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

def find_closest_line_intersection(object A, object B, List[object] C, List[object] D, float default_intersection_length):
    cdef int num_lines = len(C)
    cdef int i
    cdef float closest_intersection_length = default_intersection_length
    cdef object closest_intersection_position = None

    cdef float length
    for i in range(num_lines):
        intersection = find_lines_intersection(A, B, C[i], D[i])
        if intersection is not None:
            length = intersection.distance_to(A)
            if length < closest_intersection_length:
                closest_intersection_length = length
                closest_intersection_position = intersection

    return closest_intersection_position, closest_intersection_length

def point_left_or_right_of_line(line_start: Vector2, line_end: Vector2, point: Vector2) -> int:
    cross_product = (line_end.x - line_start.x) * (point.y - line_start.y) - (line_end.y - line_start.y) * (point.x - line_start.x)

    if cross_product > 0:
        return -1
    elif cross_product < 0:
        return 1
    else:
        return 0

def position_from_length_and_angle(float angle, float length):
    cdef float delta_y = length * math.cos(math.radians(angle))
    cdef float delta_x = length * math.sin(math.radians(angle))

    return Vector2(delta_x, delta_y)