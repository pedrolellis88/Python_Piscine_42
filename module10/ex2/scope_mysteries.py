from __future__ import annotations


def mage_counter() -> callable:
    count = 0

    def inner() -> int:
        nonlocal count
        count += 1
        return count

    return inner


def spell_accumulator(initial_power: int) -> callable:
    total = initial_power

    def inner(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return inner


def enchantment_factory(enchantment_type: str) -> callable:
    def inner(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return inner


def memory_vault() -> dict[str, callable]:
    storage: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        storage[key] = value

    def recall(key: str) -> object:
        return storage.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    print("\nTesting mage counter...")
    counter = mage_counter()
    print("Call 1:", counter())
    print("Call 2:", counter())
    print("Call 3:", counter())

    print("\nTesting spell accumulator...")
    acc = spell_accumulator(10)
    print("Add 5:", acc(5))
    print("Add 20:", acc(20))

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 12345)
    vault["store"]("spell", "Fireball")
    print(vault["recall"]("secret"))
    print(vault["recall"]("spell"))
    print(vault["recall"]("missing_key"))


if __name__ == "__main__":
    main()
