from __future__ import annotations

from abc import ABC, abstractmethod


class Rankable(ABC):
    @abstractmethod
    def calculate_rating(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def update_wins(self, wins: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_losses(self, losses: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_rank_info(self) -> dict:
        raise NotImplementedError
