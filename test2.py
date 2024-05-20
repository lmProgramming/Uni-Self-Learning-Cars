from cython.vector_math import find_lines_intersection

print(find_lines_intersection((0, 0), (1, 1), (0, 1), (1, 0)))
print(find_lines_intersection((0, 0), (1, 1), (0, 1), (1, 1)))
print(find_lines_intersection((0, 0), (1, 1), (0.01, 0), (1, 2)))