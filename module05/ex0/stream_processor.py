from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    def __init__(self, name: str) -> None:
        self.name: str = name

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if not isinstance(data, list) or len(data) == 0:
            return False
        return all(isinstance(x, (int, float)) for x in data)

    def process(self, data: Any) -> str:
        if not self.validate(data):
            print(f"Validation: numeric data not verified: {data}")
            raise ValueError("Invalid numeric data")
        else:
            print("Validation: Numeric data verified")

        print("Initializing Numeric Processor...")
        print(f"Processing data: {data}")

        total = sum(data)
        avg = total / len(data)

        return f"Processed {len(data)} numeric values, sum={total}, avg={avg}"


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("Invalid text data")
        else:
            print("Validation: Text data verified")

        print("Initializing Text Processor...")
        print(f'Processing data: "{data}"')

        chars = len(data)
        words = len(data.split())

        return f"Processed text: {chars} characters, {words} words"


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        super().__init__("Log Processor")
        self.allowed_levels = {"INFO", "ERROR"}

    def validate(self, data: Any) -> bool:
        if not isinstance(data, str):
            return False
        if ":" not in data:
            return False

        level, message = data.split(":", 1)
        level = level.strip().upper()
        message = message.strip()

        return level in self.allowed_levels and len(message) > 0

    def process(self, data: Any) -> str:
        if not self.validate(data):
            raise ValueError("Invalid log entry")
        else:
            print("Validation: Log entry verified")

        print("Initializing Log Processor...")
        print(f'Processing data: "{data}"')

        level, message = data.split(":", 1)
        level = level.strip().upper()
        message = message.strip()

        if level == "ERROR":
            return f"[ALERT] {level} level detected: {message}"
        else:
            return f"[INFO] {level} level detected: {message}"


print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

tests = [
    (NumericProcessor(), [1, 2, 3, 4, 5]),
    (TextProcessor(), "Hello Nexus World"),
    (LogProcessor(), "ERROR: Connection timeout"),
    (LogProcessor(), "INFO: System ready"),
    (NumericProcessor(), "abc"),
]

for processor, data in tests:
    try:
        result = processor.process(data)
        print(processor.format_output(result))
        print()
    except ValueError as e:
        print(f"Error: {e}", end="")
        print("")

print("\n=== Polymorphic Processing Demo ===")
