from __future__ import annotations


def spell_combiner(spell1: callable, spell2: callable) -> callable:
    return lambda *args, **kwargs: (spell1(*args, **kwargs), spell2(*args, **kwargs)) # noqa


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    return lambda *args, **kwargs: base_spell(*args, **kwargs) * multiplier # noqa


def conditional_caster(condition: callable, spell: callable) -> callable:
    return lambda *args, **kwargs: (
        spell(*args, **kwargs) if condition(*args, **kwargs) else "Spell fizzled" # noqa
    )


def spell_sequence(spells: list[callable]) -> callable:
    return lambda *args, **kwargs: list(map(lambda s: s(*args, **kwargs), spells)) # noqa


def main() -> None:
    def fireball(target: str) -> str:
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        return f"Heals {target}"

    def damage(base: int) -> int:
        return base

    def is_alive(hp: int) -> bool:
        return hp > 0

    def revive(hp: int) -> str:
        return "Revive cast!"

    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    r1, r2 = combined("Dragon")
    print(f"Combined spell result: {r1}, {r2}")

    print("\nTesting power amplifier...")
    mega_damage = power_amplifier(damage, 3)
    print(f"Original: {damage(10)}, Amplified: {mega_damage(10)}")

    print("\nTesting conditional caster...")
    safe_revive = conditional_caster(is_alive, revive)
    print(safe_revive(10))
    print(safe_revive(0))

    print("\nTesting spell sequence...")
    seq = spell_sequence([fireball, heal, revive])
    print(seq("Knight"))


if __name__ == "__main__":
    main()
