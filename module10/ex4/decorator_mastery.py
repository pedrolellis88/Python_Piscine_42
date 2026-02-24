from __future__ import annotations

from functools import wraps
import time


def spell_timer(func: callable) -> callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> callable:
    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            power = None

            if "power" in kwargs:
                power = kwargs["power"]
            else:
                if len(args) >= 1 and isinstance(args[0], int):
                    power = args[0]
                elif len(args) >= 2 and isinstance(args[1], int):
                    power = args[1]
                elif len(args) >= 3 and isinstance(args[2], int):
                    power = args[2]

            if not isinstance(power, int) or power < min_power:
                return "Insufficient power for this spell"

            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> callable:
    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        return f"Spell casting failed after {max_attempts} attempts" # noqa
                    attempt += 1
                    print(f"Spell failed, retrying... (attempt {attempt}/{max_attempts})") # noqa

            return f"Spell casting failed after {max_attempts} attempts"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        if name.strip() == "":
            return False
        return all(ch.isalpha() or ch == " " for ch in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


def main() -> None:
    print("\nTesting spell timer...")

    @spell_timer
    def fireball() -> str:
        time.sleep(0.101)
        return "Fireball cast!"

    result = fireball()
    print("Result:", result)

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Ari"))
    print(MageGuild.validate_mage_name("X1"))

    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))


if __name__ == "__main__":
    main()
