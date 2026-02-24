from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

Stats = Dict[str, Union[str, int, float]]


class DataStream(ABC):
    def __init__(self, stream_id: str, stream_type: str) -> None:
        self.stream_id: str = stream_id
        self.stream_type: str = stream_type
        self._stats: Stats = {
            "stream_id": self.stream_id,
            "type": self.stream_type,
            "processed": 0,
        }

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        raise NotImplementedError

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None,
    ) -> List[Any]:
        return data_batch

    def get_stats(self) -> Stats:
        return dict(self._stats)


class SensorStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "Environmental Data")
        print("Initializing Sensor Stream...")
        print(f"Stream ID: {self.stream_id} | Type: {self.stream_type}")

    def _safe_float(self, raw: str) -> Optional[float]:
        try:
            return float(raw)
        except ValueError:
            return None

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None,
    ) -> List[Any]:
        if criteria != "high_priority":
            return data_batch

        filtered: List[Any] = []
        for item in data_batch:
            if not isinstance(item, str):
                continue
            if not item.lower().startswith("temp:"):
                continue

            raw_value = item.split(":", 1)[1].strip()
            value = self._safe_float(raw_value)
            if value is None:
                continue

            if value >= 28.0:
                filtered.append(item)

        return filtered

    def process_batch(self, data_batch: List[Any]) -> str:
        batch_str = ", ".join(str(x) for x in data_batch)
        print(f"Processing sensor batch: [{batch_str}]")

        pairs: List[List[str]] = [
            item.split(":", 1)
            for item in data_batch
            if isinstance(item, str) and ":" in item
        ]
        if len(pairs) == 0:
            raise ValueError("Invalid sensor batch (expected 'key:value' strings).") # noqa

        readings: List[float] = []
        temps: List[float] = []

        for key, raw_value in pairs:
            val = self._safe_float(raw_value.strip())
            if val is None:
                continue

            readings.append(val)
            if key.strip().lower() == "temp":
                temps.append(val)

        if len(readings) == 0:
            raise ValueError("No numeric sensor readings found.")

        if len(temps) > 0:
            avg_temp = sum(temps) / len(temps)
        else:
            avg_temp = sum(readings) / len(readings)

        self._stats["processed"] = len(readings)
        self._stats["avg_temp"] = avg_temp

        return (
            f"Sensor analysis: {len(readings)} readings processed, "
            f"avg temp: {avg_temp}°C"
        )


class TransactionStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "Financial Data")
        print("Initializing Transaction Stream...")
        print(f"Stream ID: {self.stream_id} | Type: {self.stream_type}")

    def _safe_float(self, raw: str) -> Optional[float]:
        try:
            return float(raw)
        except ValueError:
            return None

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None,
    ) -> List[Any]:
        if criteria != "high_priority":
            return data_batch

        ops: List[List[str]] = [
            op.split(":", 1)
            for op in data_batch
            if isinstance(op, str) and ":" in op
        ]

        filtered: List[str] = []
        for action, raw_value in ops:
            val = self._safe_float(raw_value.strip())
            if val is None:
                continue
            if abs(val) >= 120.0:
                filtered.append(f"{action.strip()}:{raw_value.strip()}")

        return filtered

    def process_batch(self, data_batch: List[Any]) -> str:
        batch_str = ", ".join(str(x) for x in data_batch)
        print(f"Processing transaction batch: [{batch_str}]")

        ops: List[List[str]] = [
            op.split(":", 1)
            for op in data_batch
            if isinstance(op, str) and ":" in op
        ]
        if len(ops) == 0:
            raise ValueError("Invalid transaction batch (expected 'buy:value'/'sell:value').") # noqa

        buys: List[float] = []
        sells: List[float] = []

        for action, raw_value in ops:
            val = self._safe_float(raw_value.strip())
            if val is None:
                continue

            action_norm = action.strip().lower()
            if action_norm == "buy":
                buys.append(val)
            elif action_norm == "sell":
                sells.append(val)

        processed = len(buys) + len(sells)
        if processed == 0:
            raise ValueError("No valid buy/sell operations found.")

        net_flow = sum(buys) - sum(sells)

        self._stats["processed"] = processed
        self._stats["net_flow"] = net_flow

        sign = "+" if net_flow >= 0 else "-"
        return (
            f"Transaction analysis: {processed} operations, net flow: "
            f"{sign}{abs(int(net_flow))} units"
        )


class EventStream(DataStream):
    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "System Events")
        print("Initializing Event Stream...")
        print(f"Stream ID: {self.stream_id} | Type: {self.stream_type}")

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None,
    ) -> List[Any]:
        if criteria != "high_priority":
            return data_batch

        events: List[str] = [str(e) for e in data_batch]
        return [e for e in events if "error" in e.lower()]

    def process_batch(self, data_batch: List[Any]) -> str:
        batch_str = ", ".join(str(x) for x in data_batch)
        print(f"Processing event batch: [{batch_str}]")

        events: List[str] = [
            str(e).strip()
            for e in data_batch
            if str(e).strip() != ""
        ]
        if len(events) == 0:
            raise ValueError("Invalid event batch (empty).")

        errors: List[str] = [e for e in events if "error" in e.lower()]

        self._stats["processed"] = len(events)
        self._stats["errors"] = len(errors)

        return f"Event analysis: {len(events)} events, {len(errors)} error detected" # noqa


class StreamProcessor:
    def process_mixed(
        self,
        streams: List[DataStream],
        batches: List[List[Any]],
    ) -> None:
        print("=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...")
        print()

        print("Batch 1 Results:")
        for stream, batch in zip(streams, batches):
            try:
                stats = stream.get_stats()
                processed = int(stats.get("processed", 0))

                if isinstance(stream, SensorStream):
                    print(f"- Sensor data: {processed} readings processed")
                elif isinstance(stream, TransactionStream):
                    print(f"- Transaction data: {processed} operations processed") # noqa
                elif isinstance(stream, EventStream):
                    print(f"- Event data: {processed} events processed")
                else:
                    print(f"- {stream.stream_type}: {processed} items processed") # noqa

            except ValueError as exc:
                print(f"- {stream.stream_type}: Error ({exc})")

    def filter_demo(
        self,
        streams: List[DataStream],
        batches: List[List[Any]],
        criteria: str,
    ) -> None:
        print()
        print(f"Stream filtering active: {criteria}")

        filtered_batches: List[List[Any]] = [
            stream.filter_data(batch, criteria)
            for stream, batch in zip(streams, batches)
        ]

        sensor_alerts = len(filtered_batches[0]) if len(filtered_batches) > 0 else 0 # noqa
        large_tx = len(filtered_batches[1]) if len(filtered_batches) > 1 else 0

        print(
            f"Filtered results: {sensor_alerts} critical sensor alerts, "
            f"{large_tx} large transaction"
        )


def main() -> None:
    try:
        print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
        print()
        sensor_batch = ["temp:22.5", "humidity:65", "pressure:1013"]
        trans_batch = ["buy:100", "sell:150", "buy:75"]
        event_batch = ["login", "error", "logout"]

        sensor = SensorStream("SENSOR_001")
        print(sensor.process_batch(sensor_batch))
        print()
        trans = TransactionStream("TRANS_001")
        print(trans.process_batch(trans_batch))
        print()
        event = EventStream("EVENT_001")
        print(event.process_batch(event_batch))
        print()
        processor = StreamProcessor()

        processor.process_mixed(
            [sensor, trans, event],
            [
                ["temp:21.0", "temp:23.0"],
                ["buy:50", "sell:10", "buy:25", "sell:5"],
                ["login", "logout", "ping"],
            ],
        )

        processor.filter_demo(
            [sensor, trans, event],
            [
                ["temp:29.1", "temp:28.0", "humidity:60"],
                ["buy:80", "sell:150", "buy:30"],
                ["login", "error", "logout"],
            ],
            "high_priority",
        )

        print()
        print("All streams processed successfully. Nexus throughput optimal.")

    except ValueError as exc:
        print(f"Error: {exc}")


main()
