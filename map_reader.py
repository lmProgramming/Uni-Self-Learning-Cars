import enum
from pygame import Vector2
from map import Wall, Gate
from typing import List
import re
class Mode(enum.Enum):
    STARTING_READING = "starting_reading"
    WALLS = "walls"
    GATES = "gates"
    STARTING_POINT = "start"

def read_map_txt(filename="map.txt") -> tuple[list, list, Vector2]:
    walls: List[Wall] = []
    gates: List[Gate] = []
    starting_point: Vector2 = Vector2(0, 0)

    mode = Mode.STARTING_READING

    with open('maps/' + filename, 'r+') as f:
        for line in f:
            if mode == Mode.STARTING_READING:
                if line.startswith(Mode.WALLS.value):
                    mode = Mode.WALLS
                if line.startswith(Mode.GATES.value):
                    mode = Mode.GATES
                if line.startswith(Mode.STARTING_POINT.value):
                    match: re.Match[str] | None = re.fullmatch(r"start: (?P<x_pos>\d+);(?P<y_pos>\d+)", line)
                    if match:
                        starting_point = Vector2(int(match.group("x_pos")), int(match.group("y_pos")))    
                    else:
                        raise ValueError("Invalid starting point")
            elif mode == Mode.WALLS:
                if line == "\n":
                    mode = Mode.STARTING_READING
                else:
                    x1, x2, y1, y2 = tuple(map(int, re.split(';|,', line.strip())))
                    walls.append(Wall(x1, x2, y1, y2))
            elif mode == Mode.GATES:
                if line == "\n":
                    mode = Mode.STARTING_READING
                else:
                    num, x1, x2, y1, y2 = tuple(map(int, re.split(';|,', line.strip())))
                    gates.append(Gate(num, x1, x2, y1, y2))
    
    return walls, gates, starting_point
            
if __name__ == "__main__":
    walls, gates, starting_point = read_map_txt()
    print(len(walls))
    print(len(gates))
    print(starting_point)
