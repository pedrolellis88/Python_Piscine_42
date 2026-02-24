from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.telepathic and self.witness_count < 3: # noqa
            raise ValueError("Telepathic contact requires at least 3 witnesses") # noqa

        if self.signal_strength > 7.0:
            if self.message_received is None or self.message_received.strip() == "": # noqa
                raise ValueError(
                    "Strong signals (> 7.0) should include received messages"
                )

        return self


def print_contact(contact: AlienContact) -> None:
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")

    if contact.message_received is not None:
        print(f"Message: '{contact.message_received}'")


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)

    print("Valid contact report:")
    valid = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-01-15T10:30:00",
        location="Area 51, Nevada",
        contact_type=ContactType.radio,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=False,
    )
    print_contact(valid)

    print("=" * 38)
    print("Expected validation error:")

    try:
        AlienContact(
            contact_id="AC_2024_999",
            timestamp="2024-01-15T10:30:00",
            location="Sector 7",
            contact_type=ContactType.telepathic,
            signal_strength=6.0,
            duration_minutes=10,
            witness_count=1,
            message_received=None,
            is_verified=False,
        )
    except ValidationError as exc:
        errors = exc.errors(include_url=False)
        print(errors[0]["msg"])


if __name__ == "__main__":
    main()
