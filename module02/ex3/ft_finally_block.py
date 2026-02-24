def water_plants(plant_list):
    """Simulate watering plants and always clean up the watering system."""
    print("Opening watering system")
    try:
        for plant in plant_list:
            plant_name = plant.strip()
            print(f"Watering {plant_name}")
    except:
        print("Error : Cannot water None - invalid plant!")

    finally:
        print("Closing watering system (cleanup)")


def test_watering_system():
    """Test the watering system with valid and invalid plant lists."""
    print("=== Garden Watering System ===\n")
    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print("Watering completed sucessfully!\n")
    print("Testing with error...")
    water_plants(["tomato", None, "carrots"])
    print("\nCleanup always happens, even with errors!")


test_watering_system()
