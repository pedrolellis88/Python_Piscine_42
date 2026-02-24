import sys
import math


def distance(p1, p2):
    """Calculates the Euclidean distance between two 3D points.""" # noqa
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def parse_coordinates(text):
    """Parses a coordinate string in the format x,y,z into a tuple.""" # noqa
    parts = text.split(",")

    if len(parts) != 3:
        return "invalid_format"

    try:
        x = float(parts[0])
    except: # noqa
        return parts[0]

    try:
        y = float(parts[1])
    except: # noqa
        return parts[1]

    try:
        z = float(parts[2])
    except: # noqa
        return parts[2]

    return (x, y, z)


def test():
    """Demonstrates coordinate parsing, distance calculation, and tuple unpacking.""" # noqa
    print("=== Game Coordinate System ===\n")

    origin = tuple()
    position = tuple()
    origin = (0, 0, 0)
    position = (10, 20, 5)
    print("Example:")
    print(f"Position created: {position}")
    dist = distance(origin, position)
    print(f"Distance between {origin} and {position}: {dist}\n")

    if len(sys.argv) > 1:
        coord_text = sys.argv[1]
    else:
        coord_text = "3,4,0"

    print(f'Parsing coordinates: "{coord_text}"')
    parsed = parse_coordinates(coord_text)
    try:
        x, y, z = parsed
        print(f"Parsed position: {parsed}")
        dist2 = distance(origin, parsed)
        print(f"Distance between {origin} and {parsed}: {dist2}")
    except: # noqa
        if parsed == "invalid_format":
            print("Error details - invalid coordinate format (expected: x,y,z)") # noqa

        else:
            print(f"Error parsing coordinates: invalid literal for int() with base 10: {parsed}") # noqa
            print(f'Error details - Type: ValueError, Args: ("invalid literal for int() with base 10: {parsed}"',) # noqa

    print("\nUnpacking demonstration:")
    player_pos = (3, 4, 0)
    x, y, z = player_pos
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}")


test()
