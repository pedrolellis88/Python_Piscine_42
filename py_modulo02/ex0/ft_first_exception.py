def check_temperature(temp_str):
    """Validate a temperature string and print the appropriate message.
    Accepts plant-safe range from 0 to 40 (inclusive).
    """
    try:
        temp = int(temp_str)
        if 0 <= temp <= 40:
            print(f"Temperature {temp}°C is perfect for plants!")
            return temp
        elif temp < 0:
            print(f"Error: {temp} is too cold for plants (min  0°C)")
        elif temp > 40:
            print(f"Error: {temp} is too hot for plants (max 40°C)")

    except:
        print(f"Error: '{temp_str}' is not a valid number")


def test_temperature_input():
    """Run basic test cases for check_temperature."""
    print("=== Garden Temperature Checker ===\n")

    for value in ("25", "abc", "100", "-50"):
        print(f"Testing temperature: {value}")
        check_temperature(value)
        print("")

    print("All tests completed - program didn't crash!")


test_temperature_input()
