class GardenError(Exception):
    """Base class for garden-related errors."""
    pass


class PlantError(GardenError):
    """Error related to plant problems."""
    pass


class WaterError(GardenError):
    """Error related to watering problems."""
    pass


class GardenManager:
    """Simple garden management system"""
    def add_plant(self, garden, name):
        """Add a plant to the garden dictionary."""
        if not name:
            raise PlantError("Plant name cannot be empty!\n")

        garden[name] = {"water": 5, "sun": 8}
        print(f"Added {name} successfully")

    def water_plants(self, garden):
        """Water all plants, always cleaning up the watering system."""
        print("Opening watering system")

        try:
            if not garden:
                raise WaterError("Not enough water in tank")

            for plant_name in garden:
                print(f"Watering {plant_name} - success")

        except WaterError as err:
            print(f"Caught GardenError: {err}")

        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self, garden, name):
        """Check health data of a plant and raise errors when invalid."""
        if name not in garden:
            raise PlantError(f"Plant '{name}' does not exist")

        water = garden[name]["water"]
        sun = garden[name]["sun"]

        if water < 1:
            raise PlantError(f"Water level {water} is too low (min 1)")
        if water > 10:
            raise PlantError(f"Water level {water} is too high (max 10)")
        if sun < 2:
            raise PlantError(f"Sunlight hours {sun} is too low (min 2)")
        if sun > 12:
            raise PlantError(f"Sunlight hours {sun} is too high (max 12)")

        print(f"{name}: healthy (water: {water}, sun: {sun})")


def test_garden_management():
    """Demonstrate all error handling concepts together."""
    print("=== Garden Management System ===\n")

    manager = GardenManager()
    garden = {}
    print("Adding plants to garden...")
    try:
        manager.add_plant(garden, "tomato")
        manager.add_plant(garden, "lettuce")
        manager.add_plant(garden, "")
    except PlantError as err:
        print(f"Error adding plant: {err}")

    print("Watering plants...")
    manager.water_plants(garden)

    print("\nChecking plant health...")
    try:
        manager.check_plant_health(garden, "tomato")
        garden["lettuce"]["water"] = 15
        manager.check_plant_health(garden, "lettuce")
    except PlantError as err:
        print(f"Error checking lettuce: {err}")

    print("\nTesting error recovery...")
    try:
        raise WaterError("Not enough water in tank")
    except GardenError as err:
        print(f"Caught GardenError: {err}")
        print("System recovered and continuing...")

    print("\nGarden management system test complete!")


test_garden_management()
