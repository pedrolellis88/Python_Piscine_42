def check_plant_health(plant_name, water_level, sunlight_hours):
    """Check plant health inputs and raise errors for invalid values."""
    s_h = sunlight_hours
    w_l = water_level
    try:
        if not plant_name:
            raise ValueError("Plant name cannot be empty")
        elif water_level > 10:
            raise ValueError(f"Water level {w_l} is too high (max 10)")
        elif water_level < 1:
            raise ValueError(f"Water level {w_l} is too low (min 1)")
        elif sunlight_hours < 2:
            raise ValueError(f"Sunlight hours {s_h} is too low (min 2)")
        elif sunlight_hours > 12:
            raise ValueError(f"Sunlight hours {s_h} is too high (max 12)")

        print(f"Plant '{plant_name}' is healthy!")

    except ValueError as err:
        print(f"Error: {err}")


def test_plant_checks():
    """Demonstrate plant health checks with good and bad inputs."""
    print("=== Garden Plant Health Checker ===\n")
    print("Testing good values...")
    check_plant_health('tomato', 3, 10)
    print("")
    print("Testing empty plant name...")
    check_plant_health("", 3, 10)
    print("")
    print("Testing bad water level...")
    check_plant_health('tomato', 15, 10)
    print("")
    print("Testing bad sunlight hours...")
    check_plant_health('tomato', 3, 0)
    print("\nAll error raising tests completed!")


test_plant_checks()
