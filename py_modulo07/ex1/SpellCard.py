from __future__ import annotations

from typing import Any

from ex0.Card import Card


class SpellCard(Card):
    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        super().__init__(name, cost, rarity)

        if not isinstance(effect_type, str) or not effect_type.strip():
            raise ValueError("effect_type must be a non-empty string")
        self.effect_type = effect_type.strip().lower()

    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(game_state, dict):
            raise TypeError("game_state must be a dict")

        game_state.setdefault("graveyard", [])
        game_state.setdefault("battle_log", [])

        game_state["graveyard"].append(self.name)

        effect_result = self.resolve_effect(game_state.get("targets", []))

        result = {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": effect_result.get("effect", "Spell resolved"),
        }
        game_state["battle_log"].append(result)
        return result

    def resolve_effect(self, targets: list) -> dict:
        if not isinstance(targets, list):
            raise TypeError("targets must be a list")

        if self.effect_type == "damage":
            return {"effect": "Deal 3 damage to target"}
        if self.effect_type == "heal":
            return {"effect": "Heal 3 health to target"}
        if self.effect_type == "buff":
            return {"effect": "Give +1/+1 to a creature"}
        if self.effect_type == "debuff":
            return {"effect": "Give -1/-1 to a creature"}
        return {"effect": f"Unknown spell effect type: {self.effect_type}"}

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update({"type": "Spell", "effect_type": self.effect_type})
        return info
