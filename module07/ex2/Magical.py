from __future__ import annotations

from abc import ABC, abstractmethod


class Magical(ABC):
    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        raise NotImplementedError

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_magic_stats(self) -> dict:
        raise NotImplementedError
