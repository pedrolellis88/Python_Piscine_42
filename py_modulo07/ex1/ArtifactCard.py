from __future__ import annotations

from ex0.Card import Card

from typing import Any


class ArtifactCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, durability: int, effect: str): # noqa
        super().__init__(name, cost, rarity)

        if not isinstance(durability, int) or durability <= 0:
            raise ValueError("durability must be a positive integer")
        if not isinstance(effect, str) or not effect.strip():
            raise ValueError("effect must be a non-empty string")

        self.durability = durability
        self.effect = effect.strip()

    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(game_state, dict):
            raise TypeError("game_state must be a dict")

        game_state.setdefault("artifacts_in_play", [])
        game_state.setdefault("battle_log", [])

        game_state["artifacts_in_play"].append(self.name)

        result = {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": f"Permanent: {self.effect}",
        }
        game_state["battle_log"].append(result)
        return result

    def activate_ability(self) -> dict:
        if self.durability <= 0:
            return {"activated": False, "reason": "Artifact destroyed"}

        self.durability -= 1
        return {
            "activated": True,
            "effect": self.effect,
            "durability_left": self.durability,
        }

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update(
            {
                "type": "Artifact",
                "durability": self.durability,
                "effect": self.effect,
            }
        )
        return info
