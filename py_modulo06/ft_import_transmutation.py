print("=== Import Transmutation Mastery ===")

print("\nMethod 1 - Full module import:")
import alchemy.elements # noqa
print(f"alchemy.elements.create_fire(): {alchemy.elements.create_fire()}")

print("\nMethod 2 - Specific function import:")
from alchemy.elements import create_water # noqa
print(f"create_water(): {create_water()}")

print("\nMethod 3 - Aliased import:")
from alchemy.potions import healing_potion as heal # noqa
print(f"heal(): {heal()}")

print("\nMethod 4 - Multiple imports:")
from alchemy.elements import create_earth, create_fire # noqa
from alchemy.potions import strength_potion # noqa
print(f"create_earth(): {create_earth()}")
print(f"create_fire(): {create_fire()}")
print(f"strength_potion(): {strength_potion()}")

print("\nAll import transmutation methods mastered!")
