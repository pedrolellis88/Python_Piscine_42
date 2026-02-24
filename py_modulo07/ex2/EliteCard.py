from __future__ import annotations

from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical
from typing import Any


class EliteCard(Card, Combatable, Magical):
    def __init__(self, name: str, cost: int, rarity: str, attack_power: int, health: int, max_mana: int): # noqa
        super().__init__(name, cost, rarity)

        if not isinstance(attack_power, int) or attack_power <= 0:
            raise ValueError("attack_power must be a positive integer")
        if not isinstance(health, int) or health <= 0:
            raise ValueError("health must be a positive integer")
        if not isinstance(max_mana, int) or max_mana < 0:
            raise ValueError("max_mana must be >= 0")

        self.attack_power = attack_power
        self.health = health
        self.max_mana = max_mana
        self.current_mana = 0

    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(game_state, dict):
            raise TypeError("game_state must be a dict")

        game_state.setdefault("battlefield", [])
        game_state.setdefault("battle_log", [])

        game_state["battlefield"].append(self.name)

        result = {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Elite card deployed to battlefield",
        }
        game_state["battle_log"].append(result)
        return result

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update(
            {
                "type": "Elite",
                "attack": self.attack_power,
                "health": self.health,
                "max_mana": self.max_mana,
                "current_mana": self.current_mana,
            }
        )
        return info

    def attack(self, target) -> dict:
        target_name = getattr(target, "name", None) or str(target)

        return {
            "attacker": self.name,
            "target": target_name,
            "damage": self.attack_power,
            "combat_type": "melee",
        }

    def defend(self, incoming_damage: int) -> dict:
        if not isinstance(incoming_damage, int) or incoming_damage < 0:
            raise ValueError("incoming_damage must be an int >= 0")

        blocked = min(3, incoming_damage)
        taken = incoming_damage - blocked
        self.health -= taken

        return {
            "defender": self.name,
            "damage_taken": taken,
            "damage_blocked": blocked,
            "still_alive": self.health > 0,
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack_power": self.attack_power,
            "health": self.health,
        }

    def channel_mana(self, amount: int) -> dict:
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be an int >= 0")

        self.current_mana = min(self.max_mana, self.current_mana + amount)
        return {"channeled": amount, "total_mana": self.current_mana}

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        if not isinstance(spell_name, str) or not spell_name.strip():
            raise ValueError("spell_name must be a non-empty string")
        if not isinstance(targets, list):
            raise TypeError("targets must be a list")

        mana_cost = 4
        if self.current_mana < mana_cost:
            return {
                "caster": self.name,
                "spell": spell_name.strip(),
                "targets": targets,
                "mana_used": 0,
                "success": False,
                "reason": "Not enough mana",
            }

        self.current_mana -= mana_cost
        return {
            "caster": self.name,
            "spell": spell_name.strip(),
            "targets": targets,
            "mana_used": mana_cost,
            "success": True,
        }

    def get_magic_stats(self) -> dict:
        return {
            "max_mana": self.max_mana,
            "current_mana": self.current_mana,
        }
