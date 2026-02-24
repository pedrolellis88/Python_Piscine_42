from __future__ import annotations

from ex3.GameStrategy import GameStrategy


class AggressiveStrategy(GameStrategy):
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        available_mana = 6
        cards_played = []
        mana_used = 0
        damage_dealt = 0

        sorted_hand = sorted(hand, key=lambda c: getattr(c, "cost", 999))

        game_state = {"targets": ["Enemy Player"]}

        for card in sorted_hand:
            cost = getattr(card, "cost", 0)
            if cost <= (available_mana - mana_used):
                play_result = card.play(game_state)
                cards_played.append(play_result.get("card_played", getattr(card, "name", "Unknown"))) # noqa
                mana_used += int(play_result.get("mana_used", cost))

                info = {}
                try:
                    info = card.get_card_info()
                except Exception:
                    info = {}

                ctype = info.get("type", card.__class__.__name__)
                if ctype in ("Spell", "SpellCard") and "Deal" in str(play_result.get("effect", "")): # noqa
                    damage_dealt += 3
                if ctype in ("Creature", "CreatureCard") and "attack" in info:
                    damage_dealt += int(info.get("attack", 0))

                if ctype in ("Creature", "CreatureCard"):
                    battlefield.append(card)

        targets_attacked = ["Enemy Player"] if damage_dealt > 0 else []

        return {
            "strategy": self.get_strategy_name(),
            "actions": {
                "cards_played": cards_played,
                "mana_used": mana_used,
                "targets_attacked": targets_attacked,
                "damage_dealt": damage_dealt,
            },
        }

    def get_strategy_name(self) -> str:
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        if not isinstance(available_targets, list):
            raise TypeError("available_targets must be a list")

        if "Enemy Player" in available_targets:
            return ["Enemy Player"] + [t for t in available_targets if t != "Enemy Player"] # noqa
        return available_targets
