class GardenError(Exception):
    """Base class for garden-related errors."""
    pass


class PlantError(GardenError):
    """Error related to plant problems."""
    pass


class WaterError(GardenError):
    """Error related to watering problems."""
    pass


def check_plant():
    """Simulate a plant-related error."""
    raise PlantError("The tomato plant is wilting!")


def check_water():
    """Simulate a watering-related error."""
    raise WaterError("Not enough water in the tank!")


def test_custom_errors():
    """Demonstrate custom garden error handling."""
    print("=== Custom Garden Errors Demo ===\n")

    print("Testing PlantError...")
    try:
        check_plant()
    except PlantError as err:
        print(f"Caught PlantError: {err}\n")

    print("Testing WaterError...")
    try:
        check_water()
    except WaterError as err:
        print(f"Caught WaterError: {err}\n")

    print("Testing catching all garden errors...")
    for func in (check_plant, check_water):
        try:
            func()
        except GardenError as err:
            print(f"Caught a garden error: {err}")

    print("\nAll custom error types work correctly!")


test_custom_errors()
