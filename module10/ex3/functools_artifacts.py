from __future__ import annotations

from functools import lru_cache, partial, reduce, singledispatch
import operator
from typing import Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    ops: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }

    if operation not in ops:
        raise ValueError("Unsupported operation")

    if not spells:
        raise ValueError("spells list cannot be empty")

    return reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable[[int, str, str], str]) -> dict[str, Callable[[str], str]]: # noqa
    return {
        "fire_enchant": partial(base_enchantment, 50, "fire"),
        "ice_enchant": partial(base_enchantment, 50, "ice"),
        "lightning_enchant": partial(base_enchantment, 50, "lightning"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[object], object]:
    @singledispatch
    def dispatch(value: object) -> object:
        return "Unknown spell"

    @dispatch.register
    def _(value: int) -> str:
        return f"Damage spell: {value}"

    @dispatch.register
    def _(value: str) -> str:
        return f"Enchantment spell: {value}"

    @dispatch.register
    def _(value: list) -> list[object]:
        return list(map(dispatch, value))

    return dispatch


def main() -> None:
    print("\nTesting spell reducer...")
    spells = [10, 20, 30, 40]
    print("Sum:", spell_reducer(spells, "add"))
    print("Product:", spell_reducer(spells, "multiply"))
    print("Max:", spell_reducer(spells, "max"))
    print("Min:", spell_reducer(spells, "min"))

    print("\nTesting partial enchanter...")

    def base_enchantment(power: int, element: str, target: str) -> str:
        return f"{element.title()} enchant ({power}) on {target}"

    enchants = partial_enchanter(base_enchantment)
    print(enchants["fire_enchant"]("Sword"))
    print(enchants["ice_enchant"]("Shield"))
    print(enchants["lightning_enchant"]("Armor"))

    print("\nTesting memoized fibonacci...")
    print("Fib(10):", memoized_fibonacci(10))
    print("Fib(15):", memoized_fibonacci(15))

    print("\nTesting spell dispatcher...")
    dispatch = spell_dispatcher()
    print(dispatch(12))
    print(dispatch("Flaming"))
    print(dispatch([10, "Frozen", 3]))


if __name__ == "__main__":
    main()
