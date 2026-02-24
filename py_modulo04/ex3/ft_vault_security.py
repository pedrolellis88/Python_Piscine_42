def ft_vault_security() -> None:
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols\n")

    print("SECURE EXTRACTION:")
    with open("classified_data.txt", "r") as f:
        content = f.read()
    print(content, end="")

    print("\nSECURE PRESERVATION:")
    with open("security_protocols.txt", "r") as f:
        text = f.read()
    print(text, end="")

    print("Vault automatically sealed upon completion\n")
    print("All vault operations completed with maximum security.")


ft_vault_security()
