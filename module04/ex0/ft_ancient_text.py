def data_recovery_system() -> None:

    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    try:
        print("Accessing Storage Vault: ancient_fragment.txt\n") # noqa
        text = open("ancient_fragment.txt")
        text_content = text.read()
        print(text_content)
        print("Data recovery completed!")
        text.close()
    except: # noqa
        print("ERROR: Storage vault not found.\n")


data_recovery_system()
