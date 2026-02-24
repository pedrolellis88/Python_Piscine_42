def record_spell(spell_name: str, ingredients: str) -> str:
    from .validator import validate_ingredients  # noqa

    validation_result = validate_ingredients(ingredients)

    if "VALID" in validation_result:
        return f"Spell recorded: {spell_name} ({validation_result})"

    return f"Spell rejected: {spell_name} ({validation_result})"
