from pygame.math import Vector2

def find_lines_intersection(A: Vector2, B: Vector2, C: Vector2, D: Vector2):
    CmP = Vector2(C.x - A.x, C.y - A.y)
    r = Vector2(B.x - A.x, B.y - A.y)
    s = Vector2(D.x - C.x, D.y - C.y)

    CmPxr = CmP.x * r.y - CmP.y * r.x
    CmPxs = CmP.x * s.y - CmP.y * s.x
    rxs = r.x * s.y - r.y * s.x

    if CmPxr == 0.0:
        return ((C.x - A.x < 0.0) != (C.x - B.x < 0.0)) or ((C.y - A.y < 0.0) != (C.y - B.y < 0.0));

    if rxs == 0.0:
        return False; # Lines are parallel.

    rxsr = 1.0 / rxs
    t = CmPxs * rxsr
    u = CmPxr * rxsr

    return (t >= 0.0) and (t <= 1.0) and (u >= 0.0) and (u <= 1.0)
