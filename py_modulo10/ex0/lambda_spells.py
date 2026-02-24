from __future__ import annotations


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda artifact: artifact["power"], reverse=True) # noqa


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    powers = list(map(lambda mage: mage["power"], mages))
    return {
        "max_power": max(powers),
        "min_power": min(powers),
        "avg_power": round(sum(powers) / len(powers), 2),
    }


def main() -> None:
    artifacts = [
        {"name": "Fire Staff", "power": 92, "type": "staff"},
        {"name": "Crystal Orb", "power": 85, "type": "orb"},
        {"name": "Ancient Tome", "power": 40, "type": "book"},
    ]

    mages = [
        {"name": "Astra", "power": 12, "element": "fire"},
        {"name": "Boreal", "power": 7, "element": "ice"},
        {"name": "Cinder", "power": 30, "element": "lightning"},
    ]

    spells = ["fireball", "heal", "shield"]

    print("\nTesting artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    if len(sorted_artifacts) >= 2:
        a0 = sorted_artifacts[0]
        a1 = sorted_artifacts[1]
        print(
            f"{a0['name']} ({a0['power']} power) comes before "
            f"{a1['name']} ({a1['power']} power)"
        )

    print("\nTesting power filter...")
    strong = power_filter(mages, 10)
    print("Filtered strong mages (power > 10):", list(map(lambda m: m["name"], strong))) # noqa

    print("\nTesting spell transformer...")
    transformed = spell_transformer(spells)
    print("".join(transformed))

    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(stats)


if __name__ == "__main__":
    main()
