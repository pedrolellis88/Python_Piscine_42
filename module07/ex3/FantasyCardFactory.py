from __future__ import annotations

import random

from ex0.Card import Card
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex3.CardFactory import CardFactory, NameOrPower


class FantasyCardFactory(CardFactory):
    def create_creature(self, name_or_power: NameOrPower = None) -> Card:
        if isinstance(name_or_power, str):
            name = name_or_power
            if name.lower() == "dragon":
                return CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
            if name.lower() == "goblin":
                return CreatureCard("Goblin Warrior", 2, "Common", 2, 2)
            return CreatureCard(name, 3, "Rare", 4, 4)

        if isinstance(name_or_power, int):
            power = max(1, name_or_power)
            return CreatureCard("Summoned Beast", 3, "Rare", power, power)

        return random.choice(
            [
                CreatureCard("Fire Dragon", 5, "Legendary", 7, 5),
                CreatureCard("Goblin Warrior", 2, "Common", 2, 2),
            ]
        )

    def create_spell(self, name_or_power: NameOrPower = None) -> Card:
        if isinstance(name_or_power, str):
            name = name_or_power.lower()
            if name in ("fireball", "fire"):
                return SpellCard("Fireball", 4, "Rare", "damage")
            if name in ("lightning", "lightning bolt"):
                return SpellCard("Lightning Bolt", 3, "Common", "damage")
            return SpellCard(name_or_power, 2, "Common", "buff")

        if isinstance(name_or_power, int):
            if name_or_power % 2 == 0:
                return SpellCard("Healing Light", 2, "Common", "heal")
            return SpellCard("Battle Cry", 2, "Common", "buff")

        return random.choice(
            [
                SpellCard("Fireball", 4, "Rare", "damage"),
                SpellCard("Lightning Bolt", 3, "Common", "damage"),
            ]
        )

    def create_artifact(self, name_or_power: NameOrPower = None) -> Card:
        if isinstance(name_or_power, str):
            name = name_or_power.lower()
            if name in ("mana_ring", "ring", "mana ring"):
                return ArtifactCard("Mana Ring", 2, "Rare", 3, "+1 mana per turn") # noqa
            if name in ("mana_crystal", "crystal", "mana crystal"):
                return ArtifactCard("Mana Crystal", 2, "Rare", 3, "+1 mana per turn") # noqa
            return ArtifactCard(name_or_power, 1, "Common", 2, "Minor aura")

        if isinstance(name_or_power, int):
            dur = max(1, name_or_power)
            return ArtifactCard("Ancient Relic", 2, "Rare", dur, "Permanent: mysterious power") # noqa

        return random.choice(
            [
                ArtifactCard("Mana Ring", 2, "Rare", 3, "+1 mana per turn"),
                ArtifactCard("Mana Crystal", 2, "Rare", 3, "+1 mana per turn"),
            ]
        )

    def create_themed_deck(self, size: int) -> dict:
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")

        cards = []
        for _ in range(size):
            pick = random.choice(["creature", "spell", "artifact"])
            if pick == "creature":
                cards.append(self.create_creature())
            elif pick == "spell":
                cards.append(self.create_spell())
            else:
                cards.append(self.create_artifact())

        return {"theme": "fantasy", "size": size, "cards": cards}

    def get_supported_types(self) -> dict:
        return {
            "creatures": ["dragon", "goblin"],
            "spells": ["fireball", "lightning_bolt"],
            "artifacts": ["mana_ring", "mana_crystal"],
        }
