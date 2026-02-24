from __future__ import annotations

from ex2.EliteCard import EliteCard


def main() -> None:
    print("\n=== DataDeck Ability System ===\n")

    # name, cost, rarity, attack_power, health, max_mana
    elite = EliteCard("Arcane Warrior", 4, "Epic", 5, 10, 10)

    print("EliteCard capabilities:")
    print("- Card:", ["play", "get_card_info", "is_playable"])
    print("- Combatable:", ["attack", "defend", "get_combat_stats"])
    print("- Magical:", ["cast_spell", "channel_mana", "get_magic_stats"])

    print(f"\nPlaying {elite.name} (Elite Card):\n")
    print("Combat phase:")
    print("Attack result:", elite.attack("Enemy"))
    print("Defense result:", elite.defend(5))

    print("\nMagic phase:")
    print("Mana channel:", elite.channel_mana(7))
    print("Spell cast:", elite.cast_spell("Fireball", ["Enemy1", "Enemy2"]))

    print("\nMultiple interface implementation successful!")


if __name__ == "__main__":
    main()
