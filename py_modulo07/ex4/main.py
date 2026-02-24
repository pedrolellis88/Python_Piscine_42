from __future__ import annotations

from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print("\n=== DataDeck Tournament Platform ===\n")
    print("Registering Tournament Cards...\n")

    platform = TournamentPlatform()
    # name, cost, rarity, atack_power, health, base_rating
    fire_dragon = TournamentCard("Fire Dragon", 5, "Legendary", 7, 5, 1200)
    ice_wizard = TournamentCard("Ice Wizard", 4, "Epic", 5, 6, 1150)

    dragon_id = platform.register_card(fire_dragon)
    wizard_id = platform.register_card(ice_wizard)

    print(f"{fire_dragon.name} (ID: {dragon_id}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print("- Rating:", fire_dragon.get_rank_info()["rating"])
    print("- Record:", fire_dragon.get_rank_info()["record"])

    print(f"\n{ice_wizard.name} (ID: {wizard_id}):")
    print("- Interfaces: [Card, Combatable, Rankable]")
    print("- Rating:", ice_wizard.get_rank_info()["rating"])
    print("- Record:", ice_wizard.get_rank_info()["record"])

    print("\nCreating tournament match...")
    p_match = platform.create_match(dragon_id, wizard_id)
    print("Match result:", p_match)

    print("\nTournament Leaderboard:")
    leaderboard = platform.get_leaderboard()
    for i, row in enumerate(leaderboard, start=1):
        print(f"{i}. {row['name']} - Rating: {row['rating']} ({row['wins']}-{row['losses']})") # noqa

    print("\nPlatform Report:")
    print(platform.generate_tournament_report())

    print("\n=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")


if __name__ == "__main__":
    main()
