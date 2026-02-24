def garden_operations():
    """Demonstrate common Python error types in a garden context."""
    print("Testing ValueError...")
    try:
        int("abc")
    except ValueError:
        print("Caught ValueError: invalid literal for int()\n")

    print("Testing ZeroDivisionError...")
    try:
        _ = 10 / 0
    except ZeroDivisionError:
        print("Caught ZeroDivisionError: division by zero\n")

    print("Testing FileNotFoundError...")
    try:
        with open("missing.txt", "r") as f:
            _ = f.read()
    except FileNotFoundError:
        print("Caught FileNotFoundError: missing.txt\n")

    print("Testing KeyError...")
    try:
        plants = {"tomato": 5, "lettuce": 3}
        plant_name = "missing_plant"
        _ = plants[plant_name]
    except KeyError:
        print(f"Caught KeyError: '{plant_name}'\n")


def test_error_types():
    """Run the garden error demos and show recovery after multiple failures."""
    print("=== Garden Error Types Demo ===")
    garden_operations()
    print("Testing multiple errors together...")
    tests = ("value", "zero", "file", "key")
    for case in tests:
        try:
            if case == "value":
                int('abc')
            elif case == "zero":
                _ = 10 / 0
            elif case == "file":
                with open("missing.txt", "r") as f:
                    _ = f.read()
            else:
                plants = {"tomato": 5, "lettuce": 3}
                _ = plants["missing_plant"]

        except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError):
            verifier = True
    if verifier:
        print("Caught an error, but program continues!\n")
    print("All error types tested successfully!")


test_error_types()
