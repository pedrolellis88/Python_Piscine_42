from __future__ import annotations

from abc import ABC, abstractmethod


class Combatable(ABC):
    @abstractmethod
    def attack(self, target) -> dict:
        raise NotImplementedError

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_combat_stats(self) -> dict:
        raise NotImplementedError
