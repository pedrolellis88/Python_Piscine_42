def ft_archive_creation() -> None:
    filename = "new_discovery.txt"

    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
    print(f"Initializing new storage unit: {filename}")

    file = open(filename, "w")

    print("Storage unit created successfully...\n")
    print("Inscribing preservation data...\n")

    entries = [
        "[ENTRY 001] New quantum algorithm discovered",
        "[ENTRY 002] Efficiency increased by 347%",
        "[ENTRY 003] Archived by Data Archivist trainee",
    ]

    for line in entries:
        file.write(line + "\n")
        print(line)

    file.close()

    print("\nData inscription complete. Storage unit sealed.")
    print(f"Archive '{filename}' ready for long-term preservation.")


ft_archive_creation()
