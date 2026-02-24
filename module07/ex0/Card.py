from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Any

from enum import Enum


class CardType(str, Enum):
    CREATURE = "Creature"
    UNKNOWN = "Unknown"


class Card(ABC):
    def __init__(self, name: str, cost: int, rarity: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Card name must be a non-empty string.")
        if not isinstance(cost, int) or cost < 0:
            raise ValueError("Card cost must be a non-negative integer.")
        if not isinstance(rarity, str) or not rarity.strip():
            raise ValueError("Card rarity must be a non-empty string.")

        self.name: str = name.strip()
        self.cost: int = cost
        self.rarity: str = rarity.strip()

    @property
    def card_type(self) -> CardType:
        return CardType.UNKNOWN

    @abstractmethod
    def play(self, game_state: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def get_card_info(self) -> dict:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "type": self.card_type.value,
        }

    def is_playable(self, available_mana: int) -> bool:
        if not isinstance(available_mana, int) or available_mana < 0:
            return False
        return available_mana >= self.cost
