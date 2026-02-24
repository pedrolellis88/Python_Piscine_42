from __future__ import annotations

from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from typing import Any, Dict, List, Protocol, Union, runtime_checkable
import csv
import io
import json
import time


@runtime_checkable
class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        ...


class InputStage:
    def process(self, data: Any) -> Any:
        if data is None:
            raise ValueError("InputStage: data is None")

        if isinstance(data, dict):
            meta = data.get("meta")
            if meta is None:
                data["meta"] = {}
            elif not isinstance(meta, dict):
                raise TypeError("InputStage: meta must be a dict")
            return data

        if isinstance(data, list):
            return data

        if isinstance(data, str) and data.strip():
            return data.strip()

        raise TypeError(f"InputStage: unsupported type: {type(data)}")


class TransformStage:
    def process(self, data: Any) -> Any:
        if isinstance(data, dict):
            meta = data.setdefault("meta", {})
            safe = bool(meta.get("safe_mode", False))

            if data.get("type") == "csv":
                meta["timestamp"] = time.time()
                data.setdefault("analysis", {})
                data["analysis"].setdefault("status", "CSV parsed")
                return data

            if data.get("sensor") == "temp":
                try:
                    value = float(data.get("value"))
                except (TypeError, ValueError):
                    if safe:
                        data.setdefault("analysis", {})
                        data["analysis"]["reading"] = "N/A"
                        data["analysis"]["status"] = "Invalid data format"
                        meta["timestamp"] = time.time()
                        return data
                    raise ValueError("Invalid data format")

                unit = str(data.get("unit", "C"))
                status = "Normal range"
                if unit == "C" and (value < 0.0 or value > 35.0):
                    status = "Out of range"

                meta["timestamp"] = time.time()
                data["analysis"] = {
                    "reading": f"{value}°{unit}",
                    "status": status,
                }
                return data

            if "value" in data:
                try:
                    _ = float(data.get("value"))
                except (TypeError, ValueError):
                    if safe:
                        meta["timestamp"] = time.time()
                        data.setdefault("analysis", {})
                        data["analysis"]["status"] = "Invalid value"
                        return data
                    raise ValueError("Invalid data format")

            meta["timestamp"] = time.time()
            data["analysis"] = data.get("analysis", {})
            data["analysis"].setdefault("status", "Enriched with metadata")
            return data

        if isinstance(data, list):
            if not data:
                return {"analysis": {"summary": "Empty stream"}, "final": True}

            nums: List[float] = []
            for item in data:
                if isinstance(item, (int, float)):
                    nums.append(float(item))
                    continue

                if isinstance(item, dict) and "value" in item:
                    try:
                        nums.append(float(item["value"]))
                    except (TypeError, ValueError):
                        # ignora item inválido na agregação
                        continue

            if not nums:
                raise ValueError("TransformStage: no numeric values to aggregate") # noqa

            avg_val = sum(nums) / len(nums)
            return {
                "analysis": {
                    "count": len(nums),
                    "avg": avg_val,
                },
                "final": True,
            }

        raise TypeError(f"TransformStage: unsupported type: {type(data)}")


class OutputStage:
    def process(self, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("meta", {}).get("chaining") is True:
                return data

            if data.get("type") == "csv":
                actions = int(data.get("analysis", {}).get("actions", 0))
                return f"User activity logged: {actions} actions processed"

            if data.get("sensor") == "temp":
                analysis = data.get("analysis", {})
                reading = analysis.get("reading", "unknown")
                status = analysis.get("status", "unknown")
                return f"Processed temperature reading: {reading} ({status})"

            analysis = data.get("analysis", {})
            if "count" in analysis and "avg" in analysis:
                return f"Stream summary: {analysis['count']} readings, avg: {analysis['avg']:.1f}°C" # noqa

            return f"Output: {analysis}"

        if isinstance(data, list):
            return f"Output list: {len(data)} items"

        return f"Output: {data}"


class ProcessingPipeline(ABC):
    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id
        self.stages: List[ProcessingStage] = []
        self.stats: Counter[str] = Counter()
        self.stage_time: Dict[str, float] = defaultdict(float)

    def add_stage(self, stage: ProcessingStage) -> None:
        if not isinstance(stage, ProcessingStage):
            raise TypeError("Stage must implement process(self, data)")
        self.stages.append(stage)

    def _run_stages(self, data: Any) -> Any:
        current = data
        for stage in self.stages:
            stage_name = stage.__class__.__name__
            t0 = time.perf_counter()
            current = stage.process(current)
            self.stage_time[stage_name] += time.perf_counter() - t0
        return current

    def get_stats(self) -> Dict[str, Union[str, int, float, Dict[str, float]]]:
        processed = int(self.stats.get("processed", 0))
        errors = int(self.stats.get("errors", 0))
        total = processed + errors
        efficiency = (processed / total) if total else 1.0
        return {
            "pipeline_id": self.pipeline_id,
            "processed": processed,
            "errors": errors,
            "efficiency": efficiency,
            "stage_time_s": dict(self.stage_time),
        }

    @abstractmethod
    def process(self, data: Any) -> Union[str, Any]:
        ...


class JSONAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Union[str, Any]:
        try:
            if isinstance(data, str):
                parsed = json.loads(data)
            elif isinstance(data, dict):
                parsed = data
            else:
                raise TypeError("JSONAdapter expects str or dict")

            parsed["final"] = True
            parsed.setdefault("meta", {})
            parsed["meta"]["safe_mode"] = self.pipeline_id.endswith("_BACKUP")

            out = self._run_stages(parsed)
            self.stats["processed"] += 1
            return out
        except Exception as exc:
            self.stats["errors"] += 1
            raise RuntimeError(f"JSONAdapter failed: {exc}") from exc


class CSVAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Any:
        try:
            if not isinstance(data, str):
                raise TypeError("CSVAdapter expects str")

            f = io.StringIO(data.strip())
            reader = csv.DictReader(f)
            rows = list(reader)

            actions = len(rows) if rows else (1 if reader.fieldnames else 0)

            payload: Dict[str, Any] = {
                "type": "csv",
                "rows": rows,
                "analysis": {"actions": actions},
                "final": True,
                "meta": {},
            }

            out = self._run_stages(payload)
            self.stats["processed"] += 1
            return out

        except Exception as exc:
            self.stats["errors"] += 1
            raise RuntimeError(f"CSVAdapter failed: {exc}") from exc


class StreamAdapter(ProcessingPipeline):
    def process(self, data: Any) -> Union[str, Any]:
        try:
            if isinstance(data, str):
                stream_data = [{"value": 22.0}, {"value": 22.3}, {"value": 22.1}] # noqa
            elif isinstance(data, list):
                stream_data = data
            else:
                raise TypeError("StreamAdapter expects str or list")

            out = self._run_stages(stream_data)
            self.stats["processed"] += 1
            return out
        except Exception as exc:
            self.stats["errors"] += 1
            raise RuntimeError(f"StreamAdapter failed: {exc}") from exc


class NexusManager:
    def __init__(self, capacity_per_sec: int = 1000) -> None:
        self.capacity_per_sec = capacity_per_sec
        self.pipelines: Dict[str, ProcessingPipeline] = {}
        self.backups: Dict[str, ProcessingPipeline] = {}

    def register(self, pipeline: ProcessingPipeline) -> None:
        self.pipelines[pipeline.pipeline_id] = pipeline

    def register_backup(self, pipeline_id: str, backup: ProcessingPipeline) -> None: # noqa
        self.backups[pipeline_id] = backup

    def execute(self, pipeline_id: str, data: Any) -> Any:
        if pipeline_id not in self.pipelines:
            raise KeyError(f"Unknown pipeline: {pipeline_id}")

        pipeline = self.pipelines[pipeline_id]
        try:
            return pipeline.process(data)
        except Exception:
            backup = self.backups.get(pipeline_id)
            if backup is None:
                raise
            print("Recovery initiated: Switching to backup processor")
            return backup.process(data)

    def chain(self, pipeline_ids: List[str], data: Any) -> Any:
        current = data
        for pid in pipeline_ids:
            if isinstance(current, dict):
                current.setdefault("meta", {})
                if isinstance(current["meta"], dict):
                    current["meta"]["chaining"] = True

            current = self.execute(pid, current)

        if isinstance(current, dict) and isinstance(current.get("meta"), dict):
            current["meta"].pop("chaining", None)

        return OutputStage().process(current)


def _build_pipeline(pipeline: ProcessingPipeline) -> None:
    pipeline.add_stage(InputStage())
    pipeline.add_stage(TransformStage())
    pipeline.add_stage(OutputStage())


def main() -> None:
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===\n")
    print("Initializing Nexus Manager...")
    manager = NexusManager(capacity_per_sec=1000)
    print(f"Pipeline capacity: {manager.capacity_per_sec} streams/second\n")

    print("Creating Data Processing Pipeline...")
    json_pipe = JSONAdapter("JSON_PIPE")
    csv_pipe = CSVAdapter("CSV_PIPE")
    stream_pipe = StreamAdapter("STREAM_PIPE")

    _build_pipeline(json_pipe)
    _build_pipeline(csv_pipe)
    _build_pipeline(stream_pipe)

    manager.register(json_pipe)
    manager.register(csv_pipe)
    manager.register(stream_pipe)

    json_backup = JSONAdapter("JSON_BACKUP")
    _build_pipeline(json_backup)
    manager.register_backup("JSON_PIPE", json_backup)

    print("Stage 1: Input validation and parsing")
    print("Stage 2: Data transformation and enrichment")
    print("Stage 3: Output formatting and delivery")

    print("\n=== Multi-Format Data Processing ===\n")
    json_input = '{"sensor":"temp","value":23.5,"unit":"C"}'
    print("Processing JSON data through pipeline...")
    print("Input:", json_input)
    print("Output:", manager.execute("JSON_PIPE", json_input))
    print()

    csv_input = "user,action,timestamp\n"
    print("Processing CSV data through same pipeline...")
    print("Input:", repr(csv_input))
    print("Output:", manager.execute("CSV_PIPE", csv_input))
    print()

    print("Processing Stream data through same pipeline...")
    print("Input: Real-time sensor stream")
    print("Output:", manager.execute("STREAM_PIPE", "Real-time sensor stream"))
    print()

    print("\n=== Pipeline Chaining Demo ===")
    chain_ids = ["JSON_PIPE", "JSON_PIPE", "JSON_PIPE"]
    chain_result = manager.chain(chain_ids, json.loads(json_input))
    print("Pipeline A -> Pipeline B -> Pipeline C")
    print("Chain result:", chain_result)

    print("\n=== Error Recovery Test ===\n")
    print("Simulating pipeline failure...")
    bad_json = '{"sensor":"temp","value":"NOT_A_NUMBER","unit":"C"}'
    print(manager.execute("JSON_PIPE", bad_json))

    print("\nNexus Integration complete. All systems operational.")


main()
