from __future__ import annotations

from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):
    def __init__(self, name: str, cost: int, rarity: str, attack_power: int, health: int, base_rating: int = 1200): # noqa
        super().__init__(name, cost, rarity)

        if not isinstance(attack_power, int) or attack_power <= 0:
            raise ValueError("attack_power must be a positive integer")
        if not isinstance(health, int) or health <= 0:
            raise ValueError("health must be a positive integer")
        if not isinstance(base_rating, int) or base_rating <= 0:
            raise ValueError("base_rating must be a positive integer")

        self.attack_power = attack_power
        self.health = health

        self._rating = base_rating
        self._wins = 0
        self._losses = 0

    def play(self, game_state: dict) -> dict:
        if not isinstance(game_state, dict):
            raise TypeError("game_state must be a dict")

        game_state.setdefault("battlefield", [])
        game_state["battlefield"].append(self.name)

        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Tournament card entered the battlefield",
        }

    def get_card_info(self) -> dict:
        info = super().get_card_info()
        info.update(
            {
                "type": "Tournament",
                "attack": self.attack_power,
                "health": self.health,
                "rating": self._rating,
                "wins": self._wins,
                "losses": self._losses,
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

        self.health -= incoming_damage
        return {
            "defender": self.name,
            "damage_taken": incoming_damage,
            "still_alive": self.health > 0,
        }

    def get_combat_stats(self) -> dict:
        return {"attack_power": self.attack_power, "health": self.health}

    def calculate_rating(self) -> int:
        return int(self._rating)

    def update_wins(self, wins: int) -> None:
        if not isinstance(wins, int) or wins < 0:
            raise ValueError("wins must be an int >= 0")
        self._wins += wins

    def update_losses(self, losses: int) -> None:
        if not isinstance(losses, int) or losses < 0:
            raise ValueError("losses must be an int >= 0")
        self._losses += losses

    def get_rank_info(self) -> dict:
        return {
            "rating": self.calculate_rating(),
            "wins": self._wins,
            "losses": self._losses,
            "record": f"{self._wins}-{self._losses}",
        }

    def get_tournament_stats(self) -> dict:
        return {
            "name": self.name,
            "rating": self.calculate_rating(),
            "wins": self._wins,
            "losses": self._losses,
            "attack_power": self.attack_power,
            "health": self.health,
        }

    def _apply_rating_delta(self, delta: int) -> None:
        self._rating = max(1, self._rating + int(delta))
