def crisis_handler(filename: str) -> None:
    if filename == "standard_archive.txt":
        print(f"ROUTINE ACCESS: Attempting access to '{filename}'...")
    else:
        print(f"CRISIS ALERT: Attempting access to '{filename}'...")

    try:
        with open(filename, "r") as f:
            content = f.read().strip()

        preview = content if content else "(empty archive)"
        print(f"SUCCESS: Archive recovered - \"{preview}\"")
        print("STATUS: Normal operations resumed\n")

    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable\n")

    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained\n")

    except Exception:
        print("RESPONSE: Unexpected system anomaly detected")
        print("STATUS: Crisis contained, system stable\n")


def ft_crisis_response() -> None:
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")

    test_files = [
        "classified_data.txt",
        "standard_archive.txt",
        "corrupted_archive.txt"
    ]

    for name in test_files:
        crisis_handler(name)

    print("All crisis scenarios handled successfully. Archives secure.")


ft_crisis_response()
