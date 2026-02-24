from __future__ import annotations

import random
from typing import Dict, List

from ex4.TournamentCard import TournamentCard


class TournamentPlatform:
    def __init__(self) -> None:
        self._cards: Dict[str, TournamentCard] = {}
        self._matches_played = 0

    def register_card(self, card: TournamentCard) -> str:
        if not isinstance(card, TournamentCard):
            raise TypeError("card must be a TournamentCard")

        base = "".join(ch.lower() if ch.isalnum() else "_" for ch in card.name).strip("_") # noqa
        if not base:
            base = "card"

        idx = 1
        card_id = f"{base}_{idx:03d}"
        while card_id in self._cards:
            idx += 1
            card_id = f"{base}_{idx:03d}"

        self._cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:
        if card1_id not in self._cards or card2_id not in self._cards:
            raise KeyError("Both card IDs must be registered on the platform") # noqa
        if card1_id == card2_id:
            raise ValueError("card1_id and card2_id must be different")

        c1 = self._cards[card1_id]
        c2 = self._cards[card2_id]

        s1 = c1.calculate_rating() + (c1.attack_power * 10) + random.randint(-20, 20) # noqa
        s2 = c2.calculate_rating() + (c2.attack_power * 10) + random.randint(-20, 20) # noqa

        if s1 == s2:
            winner_id, loser_id = (card1_id, card2_id) if card1_id < card2_id else (card2_id, card1_id) # noqa
        else:
            winner_id, loser_id = (card1_id, card2_id) if s1 > s2 else (card2_id, card1_id) # noqa

        winner = self._cards[winner_id]
        loser = self._cards[loser_id]

        winner.update_wins(1)
        loser.update_losses(1)

        winner._apply_rating_delta(+16)
        loser._apply_rating_delta(-16)

        self._matches_played += 1

        return {
            "winner": winner_id,
            "loser": loser_id,
            "winner_rating": winner.calculate_rating(),
            "loser_rating": loser.calculate_rating(),
        }

    def get_leaderboard(self) -> list:
        items: List[tuple[str, TournamentCard]] = list(self._cards.items()) # noqa
        items.sort(key=lambda kv: kv[1].calculate_rating(), reverse=True)

        leaderboard = []
        for card_id, card in items:
            info = card.get_tournament_stats()
            info.update({"id": card_id})
            leaderboard.append(info)
        return leaderboard

    def generate_tournament_report(self) -> dict:
        if not self._cards:
            return {
                "total_cards": 0,
                "matches_played": self._matches_played,
                "avg_rating": 0,
                "platform_status": "active",
            }

        ratings = [c.calculate_rating() for c in self._cards.values()]
        avg_rating = sum(ratings) / len(ratings)

        return {
            "total_cards": len(self._cards),
            "matches_played": self._matches_played,
            "avg_rating": int(round(avg_rating)),
            "platform_status": "active",
        }
