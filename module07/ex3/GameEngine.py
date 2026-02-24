from __future__ import annotations

from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:
    def __init__(self) -> None:
        self._factory: CardFactory | None = None
        self._strategy: GameStrategy | None = None

        self._hand = []
        self._battlefield = []

        self._turns_simulated = 0
        self._total_damage = 0
        self._cards_created = 0

    def configure_engine(self, factory: CardFactory, strategy: GameStrategy) -> None: # noqa
        if factory is None or strategy is None:
            raise ValueError("factory and strategy must not be None")
        self._factory = factory
        self._strategy = strategy

    def _ensure_configured(self) -> None:
        if self._factory is None or self._strategy is None:
            raise RuntimeError("Engine not configured. Call configure_engine(factory, strategy).") # noqa

    def simulate_turn(self) -> dict:
        self._ensure_configured()

        self._hand = [
            self._factory.create_creature("dragon"),
            self._factory.create_creature("goblin"),
            self._factory.create_spell("lightning bolt"),
        ]
        self._cards_created += len(self._hand)

        execution = self._strategy.execute_turn(self._hand, self._battlefield) # noqa
        self._turns_simulated += 1

        damage = int(execution.get("actions", {}).get("damage_dealt", 0))
        self._total_damage += damage

        return {
            "hand": [f"{c.name} ({c.cost})" for c in self._hand],
            "turn_execution": execution,
            "game_report": self.get_engine_status(),
        }

    def get_engine_status(self) -> dict:
        self._ensure_configured()
        return {
            "turns_simulated": self._turns_simulated,
            "strategy_used": self._strategy.get_strategy_name(),
            "total_damage": self._total_damage,
            "cards_created": self._cards_created,
        }
