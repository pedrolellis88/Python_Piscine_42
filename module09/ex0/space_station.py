from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def print_station(station: SpaceStation) -> None:
    status = "Operational" if station.is_operational else "Not operational"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")
    if station.notes is not None:
        print(f"Notes: {station.notes}")


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    print("Valid station created:")
    valid_station = SpaceStation(
        station_id="LGW125",
        name='Titan Mining Outpost',
        crew_size=6,
        power_level=76.4,
        oxygen_level=95.5,
        last_maintenance="2023-07-11T00:00:00",
        is_operational=True,
        notes=None
    )
    print_station(valid_station)
    print("=" * 40)

    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="BAD1",
            name="Broken Station",
            crew_size=25,  # error
            power_level=10000.0,  # error
            oxygen_level=50.0,
            last_maintenance="2024-01-15T10:30:00",
        )
    except ValidationError as exc:
        errors = exc.errors(include_url=False)
        print(errors[0]["msg"])


if __name__ == "__main__":
    main()
