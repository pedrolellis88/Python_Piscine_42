from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Union

from ex0.Card import Card


NameOrPower = Union[str, int, None]


class CardFactory(ABC):
    @abstractmethod
    def create_creature(self, name_or_power: NameOrPower = None) -> Card:
        raise NotImplementedError

    @abstractmethod
    def create_spell(self, name_or_power: NameOrPower = None) -> Card:
        raise NotImplementedError

    @abstractmethod
    def create_artifact(self, name_or_power: NameOrPower = None) -> Card:
        raise NotImplementedError

    @abstractmethod
    def create_themed_deck(self, size: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_supported_types(self) -> dict:
        raise NotImplementedError
