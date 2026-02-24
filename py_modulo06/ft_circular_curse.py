import alchemy.grimoire

print("=== Circular Curse Breaking ===")

print("\nTesting ingredient validation:")
print(
    f'validate_ingredients("fire air"): '
    f'{alchemy.grimoire.validate_ingredients("fire air")}'
)
print(
    f'validate_ingredients("dragon scales"): '
    f'{alchemy.grimoire.validate_ingredients("dragon scales")}'
)

print("\nTesting spell recording with validation:")
print(
    f'record_spell("Fireball", "fire air"): '
    f'{alchemy.grimoire.record_spell("Fireball", "fire air")}'
)
print(
    f'record_spell("Dark Magic", "shadow"): '
    f'{alchemy.grimoire.record_spell("Dark Magic", "shadow")}'
)

print("\nTesting late import technique:")
print(
    f'record_spell("Lightning", "air"): '
    f'{alchemy.grimoire.record_spell("Lightning", "air")}'
)

print("\nCircular dependency curse avoided using late imports!")
print("All spells processed safely!")
