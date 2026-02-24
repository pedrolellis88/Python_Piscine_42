from __future__ import annotations

from ex3.AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.GameEngine import GameEngine


def main() -> None:
    print("\n=== DataDeck Game Engine ===\n")
    print("Configuring Fantasy Card Game...")

    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()

    engine = GameEngine()
    engine.configure_engine(factory=factory, strategy=strategy)

    print("Factory:", factory.__class__.__name__)
    print("Strategy:", strategy.get_strategy_name())
    print("Available types:", factory.get_supported_types())

    print("\nSimulating aggressive turn...")
    result = engine.simulate_turn()

    print("Hand:", result["hand"])
    print("\nTurn execution:")
    print("Strategy:", result["turn_execution"]["strategy"])
    print("Actions:", result["turn_execution"]["actions"])

    print("\nGame Report:")
    print(result["game_report"])

    print("\nAbstract Factory + Strategy Pattern: Maximum flexibility achieved!") # noqa


if __name__ == "__main__":
    main()
