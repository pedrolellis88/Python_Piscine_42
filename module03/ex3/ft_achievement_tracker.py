def achievement_tracker():
    """Tracks and compares player achievements using set operations."""
    print("=== Achievement Tracker System ===\n")

    alice = set(["first_kill", "level_10", "treasure_hunter", "speed_demon"]) # noqa
    bob = set(["first_kill", "level_10", "boss_slayer", "collector"])
    charlie = set(["level_10", "treasure_hunter", "boss_slayer", "speed_demon", "perfectionist"]) # noqa

    print(f"Player alice achievements: {alice}")
    print(f"Player bob achievements: {bob}")
    print(f"Player charlie achievements: {charlie}")

    print("\n=== Achievement Analytics ===")

    all_achievements = alice.union(bob).union(charlie)
    print(f"All unique achievements: {all_achievements}")
    print(f"Total unique achievements: {len(all_achievements)}")

    common_all = alice.intersection(bob).intersection(charlie)
    print(f"\nCommon to all players: {common_all}")

    bob_or_charlie = bob.union(charlie)
    alice_or_charlie = alice.union(charlie)
    alice_or_bob = alice.union(bob)
    rare = alice.difference(bob_or_charlie)
    rare = rare.union(bob.difference(alice_or_charlie))
    rare = rare.union(charlie.difference(alice_or_bob))
    print(f"Rare achievements (1 player): {rare}")

    alice_bob_common = alice.intersection(bob)
    print(f"\nAlice vs Bob common: {alice_bob_common}")
    alice_unique = alice.difference(bob)
    print(f"Alice has that Bob doesn't: {alice_unique}")
    bob_unique = bob.difference(alice)
    print(f"Bob has that Alice doesn't: {bob_unique}")

    alice_charlie_common = alice.intersection(charlie)
    print(f"\nAlice vs Charlie common: {alice_charlie_common}")
    alice_unique = alice.difference(charlie)
    print(f"Alice has that Charlie doesn't: {alice_unique}")
    charlie_unique = charlie.difference(alice)
    print(f"Charlie has that Alice doesn't: {charlie_unique}")

    bob_charlie_common = bob.intersection(charlie)
    print(f"\nBob vs Charlie common: {bob_charlie_common}")
    bob_unique = bob.difference(charlie)
    print(f"Bob has that Charlie doesn't: {bob_unique}")
    charlie_unique = charlie.difference(bob)
    print(f"Charlie has that Bob doesn't: {charlie_unique}")


achievement_tracker()
