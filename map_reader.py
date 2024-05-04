STARTING_READING = "starting_reading"
BORDERS = "borders"
GATES = "gates"
STARTING_POINT = "start"

def read_map_txt(filename="map.txt"):
    from pygame import Vector2
    from neat_and_pygame import Wall, Gate
    borders = []
    gates = []
    starting_point = (0, 0)

    mode = STARTING_READING

    with open('maps/' + filename, 'r+') as f:
        for line in f:
            if mode == STARTING_READING:
                if line.startswith(BORDERS):
                    mode = BORDERS
                if line.startswith(GATES):
                    mode = GATES
                if line.startswith(STARTING_POINT):
                    values = line.strip().split(",")
                    starting_point = Vector2(int(values[1]), int(values[2]))

            elif mode == BORDERS:
                if line == "\n":
                    mode = STARTING_READING
                else:
                    x1, x2, y1, y2 = tuple(map(int, line.strip().split(",")))
                    borders.append(Wall(x1, x2, y1, y2))
            elif mode == GATES:
                if line == "\n":
                    mode = STARTING_READING
                else:
                    num, x1, x2, y1, y2 = tuple(map(int, line.strip().split(",")))
                    gates.append(Gate(num, x1, x2, y1, y2))
    
    return borders, gates, starting_point
            
if __name__ == "__main__":
    borders, gates, starting_point = read_map_txt()
    print(len(borders))
    print(len(gates))
    print(starting_point)
