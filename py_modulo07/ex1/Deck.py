from __future__ import annotations

import random
from typing import List

from ex0.Card import Card


class Deck:
    def __init__(self):
        self._cards: List[Card] = []

    def add_card(self, card: Card) -> None:
        if not isinstance(card, Card):
            raise TypeError("card must be an instance of Card")
        self._cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        if not isinstance(card_name, str) or not card_name.strip():
            raise ValueError("card_name must be a non-empty string")

        needle = card_name.strip()
        for i, card in enumerate(self._cards):
            if card.name == needle:
                self._cards.pop(i)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self._cards)

    def draw_card(self) -> Card:
        if not self._cards:
            raise IndexError("Cannot draw from an empty deck")
        return self._cards.pop(0)

    def get_deck_stats(self) -> dict:
        total = len(self._cards)
        if total == 0:
            return {
                "total_cards": 0,
                "creatures": 0,
                "spells": 0,
                "artifacts": 0,
                "avg_cost": 0.0,
            }

        creatures = 0
        spells = 0
        artifacts = 0
        total_cost = 0

        for card in self._cards:
            info = card.get_card_info()
            ctype = info.get("type", "Unknown")
            total_cost += int(info.get("cost", 0))

            if ctype == "Creature":
                creatures += 1
            elif ctype == "Spell":
                spells += 1
            elif ctype == "Artifact":
                artifacts += 1

        avg_cost = total_cost / total
        return {
            "total_cards": total,
            "creatures": creatures,
            "spells": spells,
            "artifacts": artifacts,
            "avg_cost": round(avg_cost, 2),
        }
