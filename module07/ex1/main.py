from __future__ import annotations

from ex0.CreatureCard import CreatureCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck
from ex1.SpellCard import SpellCard


def main() -> None:
    print("\n=== DataDeck Deck Builder ===\n")
    print("Building deck with different card types...")

    deck = Deck()
    # name, cost, rarity, attack(Creature) or effect_type(Spell) or durability & effect(Artifact) # noqa
    fire_dragon = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    lightning_bolt = SpellCard("Lightning Bolt", 3, "Common", "damage")
    mana_crystal = ArtifactCard("Mana Crystal", 2, "Rare", 3, "+1 mana per turn") # noqa

    deck.add_card(fire_dragon)
    deck.add_card(lightning_bolt)
    deck.add_card(mana_crystal)

    print("Deck stats:", deck.get_deck_stats())

    deck.shuffle()
    print("\nDrawing and playing cards:")

    game_state = {"targets": ["Enemy"]}

    while True:
        try:
            card = deck.draw_card()
        except IndexError:
            break

        info = card.get_card_info()
        print(f"\nDrew: {card.name} ({info.get('type', 'Unknown')})")
        result = card.play(game_state)
        print("Play result:", result)

    print("\nPolymorphism in action: Same interface, different card behaviors!") # noqa


if __name__ == "__main__":
    main()
