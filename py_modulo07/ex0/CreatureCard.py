from __future__ import annotations

from typing import Any

from ex0.Card import Card, CardType


class CreatureCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, attack: int, health: int) -> None: # noqa
        super().__init__(name, cost, rarity)

        if not isinstance(attack, int) or attack <= 0:
            raise ValueError("Creature attack must be a positive integer.")
        if not isinstance(health, int) or health <= 0:
            raise ValueError("Creature health must be a positive integer.")

        self.attack: int = attack
        self.health: int = health

    @property
    def card_type(self) -> CardType:
        return CardType.CREATURE

    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        battlefield = game_state.get("battlefield")
        if isinstance(battlefield, list):
            battlefield.append(self.name)

        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Creature summoned to battlefield",
        }

    def get_card_info(self) -> dict[str, Any]:
        info = super().get_card_info()
        info.update({"attack": self.attack, "health": self.health})
        return info

    def attack_target(self, target: Any) -> dict[str, Any]:
        target_name = str(target)
        return {
            "attacker": self.name,
            "target": target_name,
            "damage_dealt": self.attack,
            "combat_resolved": True,
        }
