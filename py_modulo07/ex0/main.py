from __future__ import annotations

from ex0.CreatureCard import CreatureCard


def main() -> None:
    print("\n=== DataDeck Card Foundation ===\n")
    print("Testing Abstract Base Class Design:\n")

    fire_dragon = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)

    print("CreatureCard Info:")
    print(fire_dragon.get_card_info())

    available_mana = 6
    print(f"\nPlaying {fire_dragon.name} with {available_mana} mana available:") # noqa
    print(f"Playable: {fire_dragon.is_playable(available_mana)}")

    game_state: dict = {"battlefield": []}
    if fire_dragon.is_playable(available_mana):
        result = fire_dragon.play(game_state)
        print(f"Play result: {result}")

    print(f"\n{fire_dragon.name} attacks Goblin Warrior:")
    attack_result = fire_dragon.attack_target("Goblin Warrior")
    print(f"Attack result: {attack_result}")

    low_mana = 3
    print(f"\nTesting insufficient mana ({low_mana} available):")
    print(f"Playable: {fire_dragon.is_playable(low_mana)}")

    print("\nAbstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
