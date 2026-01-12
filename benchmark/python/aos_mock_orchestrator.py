#!/usr/bin/env python3
"""
AOS-M Mock Orchestrator Benchmark
A mock orchestration system demonstrating domain models, protocols,
planning, scheduling, tool adapters, encrypted persistence, and reporting.
"""

from __future__ import annotations
import base64
import hashlib
import hmac
import math
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any, Callable, Dict, Generic, List, Optional,
    Protocol, Tuple, TypeVar, Union
)

GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)


class TaskStatus(Enum):
    PENDING = auto()
    QUEUED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class ResourceType(Enum):
    CPU = auto()
    MEMORY = auto()
    GPU = auto()
    NETWORK = auto()
    STORAGE = auto()


class ToolType(Enum):
    COMPILER = auto()
    ANALYZER = auto()
    TRANSFORMER = auto()
    VALIDATOR = auto()
    REPORTER = auto()


@dataclass
class Resource:
    resource_type: ResourceType
    capacity: float
    available: float
    unit: str = "units"

    def allocate(self, amount: float) -> bool:
        if amount <= self.available:
            self.available -= amount
            return True
        return False

    def release(self, amount: float) -> None:
        self.available = min(self.capacity, self.available + amount)

    @property
    def utilization(self) -> float:
        return (self.capacity - self.available) / self.capacity if self.capacity > 0 else 0.0


@dataclass
class ResourceRequirements:
    cpu: float = 0.0
    memory: float = 0.0
    gpu: float = 0.0
    network: float = 0.0
    storage: float = 0.0

    def to_dict(self) -> Dict[ResourceType, float]:
        return {
            ResourceType.CPU: self.cpu,
            ResourceType.MEMORY: self.memory,
            ResourceType.GPU: self.gpu,
            ResourceType.NETWORK: self.network,
            ResourceType.STORAGE: self.storage,
        }


@dataclass
class TaskDefinition:
    task_id: str
    name: str
    tool_type: ToolType
    priority: Priority
    requirements: ResourceRequirements
    dependencies: List[str] = field(default_factory=list)
    timeout_seconds: float = 300.0
    retries: int = 3
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskInstance:
    definition: TaskDefinition
    status: TaskStatus = TaskStatus.PENDING
    attempt: int = 0
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    allocated_resources: Dict[ResourceType, float] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0

    @property
    def is_terminal(self) -> bool:
        return self.status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED)


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    tasks: List[TaskDefinition]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_task(self, task_id: str) -> Optional[TaskDefinition]:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def topological_sort(self) -> List[TaskDefinition]:
        in_degree: Dict[str, int] = {t.task_id: 0 for t in self.tasks}
        graph: Dict[str, List[str]] = {t.task_id: [] for t in self.tasks}

        for task in self.tasks:
            for dep in task.dependencies:
                if dep in graph:
                    graph[dep].append(task.task_id)
                    in_degree[task.task_id] += 1

        queue = [tid for tid, deg in in_degree.items() if deg == 0]
        result = []

        while queue:
            queue.sort(key=lambda x: self.get_task(x).priority.value, reverse=True)
            current = queue.pop(0)
            result.append(self.get_task(current))

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result


@dataclass
class WorkflowInstance:
    definition: WorkflowDefinition
    instance_id: str
    tasks: Dict[str, TaskInstance] = field(default_factory=dict)
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    def __post_init__(self):
        for task_def in self.definition.tasks:
            self.tasks[task_def.task_id] = TaskInstance(definition=task_def)

    @property
    def status(self) -> TaskStatus:
        statuses = [t.status for t in self.tasks.values()]
        if all(s == TaskStatus.COMPLETED for s in statuses):
            return TaskStatus.COMPLETED
        if any(s == TaskStatus.FAILED for s in statuses):
            return TaskStatus.FAILED
        if any(s == TaskStatus.RUNNING for s in statuses):
            return TaskStatus.RUNNING
        if any(s == TaskStatus.QUEUED for s in statuses):
            return TaskStatus.QUEUED
        return TaskStatus.PENDING

    def get_ready_tasks(self) -> List[TaskInstance]:
        ready = []
        for task_id, task in self.tasks.items():
            if task.status != TaskStatus.PENDING:
                continue
            deps_met = all(
                self.tasks[dep].status == TaskStatus.COMPLETED
                for dep in task.definition.dependencies
                if dep in self.tasks
            )
            if deps_met:
                ready.append(task)
        return ready


class ExecutionProtocol(Protocol):
    def execute(self, task: TaskInstance) -> Tuple[bool, Any]:
        ...

    def validate(self, task: TaskInstance) -> bool:
        ...


class ToolAdapter(ABC):
    tool_type: ToolType
    name: str

    @abstractmethod
    def execute(self, task: TaskInstance, context: Dict[str, Any]) -> Tuple[bool, Any]:
        pass

    @abstractmethod
    def validate_input(self, task: TaskInstance) -> bool:
        pass

    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "type": self.tool_type.name,
            "name": self.name,
        }


class CompilerAdapter(ToolAdapter):
    tool_type = ToolType.COMPILER
    name = "MockCompiler"

    def __init__(self):
        self.supported_languages = ["python", "java", "cpp", "rust"]
        self.optimization_levels = ["O0", "O1", "O2", "O3"]

    def execute(self, task: TaskInstance, context: Dict[str, Any]) -> Tuple[bool, Any]:
        language = task.definition.metadata.get("language", "python")
        opt_level = task.definition.metadata.get("optimization", "O2")

        if language not in self.supported_languages:
            return False, f"Unsupported language: {language}"

        compile_time = random.uniform(0.1, 2.0)
        time.sleep(0.001)

        return True, {
            "language": language,
            "optimization": opt_level,
            "compile_time": compile_time,
            "output_size": random.randint(1000, 100000),
            "warnings": random.randint(0, 5),
        }

    def validate_input(self, task: TaskInstance) -> bool:
        return "language" in task.definition.metadata


class AnalyzerAdapter(ToolAdapter):
    tool_type = ToolType.ANALYZER
    name = "MockAnalyzer"

    def __init__(self):
        self.analysis_types = ["static", "dynamic", "security", "performance"]

    def execute(self, task: TaskInstance, context: Dict[str, Any]) -> Tuple[bool, Any]:
        analysis_type = task.definition.metadata.get("analysis_type", "static")

        issues_found = random.randint(0, 20)
        severity_dist = {
            "critical": random.randint(0, max(1, issues_found // 10)),
            "high": random.randint(0, max(1, issues_found // 5)),
            "medium": random.randint(0, issues_found // 2),
            "low": issues_found,
        }

        return True, {
            "analysis_type": analysis_type,
            "issues_found": issues_found,
            "severity_distribution": severity_dist,
            "coverage": random.uniform(0.7, 1.0),
        }

    def validate_input(self, task: TaskInstance) -> bool:
        return True


class TransformerAdapter(ToolAdapter):
    tool_type = ToolType.TRANSFORMER
    name = "MockTransformer"

    def execute(self, task: TaskInstance, context: Dict[str, Any]) -> Tuple[bool, Any]:
        transform_type = task.definition.metadata.get("transform", "optimize")

        return True, {
            "transform": transform_type,
            "input_nodes": random.randint(100, 1000),
            "output_nodes": random.randint(50, 800),
            "reduction_ratio": random.uniform(0.1, 0.5),
        }

    def validate_input(self, task: TaskInstance) -> bool:
        return True


class ValidatorAdapter(ToolAdapter):
    tool_type = ToolType.VALIDATOR
    name = "MockValidator"

    def execute(self, task: TaskInstance, context: Dict[str, Any]) -> Tuple[bool, Any]:
        validation_rules = task.definition.metadata.get("rules", [])

        passed = random.random() > 0.1
        violations = [] if passed else [f"Rule violation {i}" for i in range(random.randint(1, 5))]

        return True, {
            "passed": passed,
            "rules_checked": len(validation_rules) if validation_rules else 10,
            "violations": violations,
        }

    def validate_input(self, task: TaskInstance) -> bool:
        return True


class ReporterAdapter(ToolAdapter):
    tool_type = ToolType.REPORTER
    name = "MockReporter"

    def execute(self, task: TaskInstance, context: Dict[str, Any]) -> Tuple[bool, Any]:
        report_format = task.definition.metadata.get("format", "json")

        return True, {
            "format": report_format,
            "sections": ["summary", "details", "recommendations"],
            "generated_at": time.time(),
        }

    def validate_input(self, task: TaskInstance) -> bool:
        return True


class ToolRegistry:
    def __init__(self):
        self._adapters: Dict[ToolType, ToolAdapter] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register(CompilerAdapter())
        self.register(AnalyzerAdapter())
        self.register(TransformerAdapter())
        self.register(ValidatorAdapter())
        self.register(ReporterAdapter())

    def register(self, adapter: ToolAdapter) -> None:
        self._adapters[adapter.tool_type] = adapter

    def get(self, tool_type: ToolType) -> Optional[ToolAdapter]:
        return self._adapters.get(tool_type)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [adapter.get_capabilities() for adapter in self._adapters.values()]


class ResourcePool:
    def __init__(self):
        self._resources: Dict[ResourceType, Resource] = {}
        self._initialize_defaults()

    def _initialize_defaults(self) -> None:
        self._resources = {
            ResourceType.CPU: Resource(ResourceType.CPU, 100.0, 100.0, "cores"),
            ResourceType.MEMORY: Resource(ResourceType.MEMORY, 1024.0, 1024.0, "GB"),
            ResourceType.GPU: Resource(ResourceType.GPU, 8.0, 8.0, "units"),
            ResourceType.NETWORK: Resource(ResourceType.NETWORK, 10000.0, 10000.0, "Mbps"),
            ResourceType.STORAGE: Resource(ResourceType.STORAGE, 10000.0, 10000.0, "GB"),
        }

    def allocate(self, requirements: ResourceRequirements) -> Optional[Dict[ResourceType, float]]:
        req_dict = requirements.to_dict()

        for res_type, amount in req_dict.items():
            if amount > 0 and self._resources[res_type].available < amount:
                return None

        allocated = {}
        for res_type, amount in req_dict.items():
            if amount > 0:
                self._resources[res_type].allocate(amount)
                allocated[res_type] = amount

        return allocated

    def release(self, allocated: Dict[ResourceType, float]) -> None:
        for res_type, amount in allocated.items():
            self._resources[res_type].release(amount)

    def get_utilization(self) -> Dict[ResourceType, float]:
        return {res_type: res.utilization for res_type, res in self._resources.items()}


class ExecutionPlanner:
    def __init__(self, resource_pool: ResourcePool):
        self.resource_pool = resource_pool

    def create_plan(self, workflow: WorkflowDefinition) -> List[List[TaskDefinition]]:
        sorted_tasks = workflow.topological_sort()

        levels: List[List[TaskDefinition]] = []
        task_levels: Dict[str, int] = {}

        for task in sorted_tasks:
            if not task.dependencies:
                level = 0
            else:
                max_dep_level = max(
                    task_levels.get(dep, 0) for dep in task.dependencies
                )
                level = max_dep_level + 1

            task_levels[task.task_id] = level

            while len(levels) <= level:
                levels.append([])
            levels[level].append(task)

        for level in levels:
            level.sort(key=lambda t: t.priority.value, reverse=True)

        return levels

    def estimate_duration(self, workflow: WorkflowDefinition) -> float:
        levels = self.create_plan(workflow)
        total_duration = 0.0

        for level in levels:
            max_task_duration = max(
                task.timeout_seconds * 0.5 for task in level
            ) if level else 0.0
            total_duration += max_task_duration

        return total_duration


class TaskScheduler:
    def __init__(self, resource_pool: ResourcePool, tool_registry: ToolRegistry):
        self.resource_pool = resource_pool
        self.tool_registry = tool_registry
        self._queue: List[TaskInstance] = []
        self._running: List[TaskInstance] = []
        self._completed: List[TaskInstance] = []

    def enqueue(self, task: TaskInstance) -> bool:
        if task.status != TaskStatus.PENDING:
            return False

        task.status = TaskStatus.QUEUED
        self._queue.append(task)
        self._queue.sort(key=lambda t: t.definition.priority.value, reverse=True)
        return True

    def schedule_next(self) -> Optional[TaskInstance]:
        for i, task in enumerate(self._queue):
            allocated = self.resource_pool.allocate(task.definition.requirements)
            if allocated:
                task.allocated_resources = allocated
                task.status = TaskStatus.RUNNING
                task.start_time = time.time()
                task.attempt += 1
                self._queue.pop(i)
                self._running.append(task)
                return task
        return None

    def execute_task(self, task: TaskInstance) -> bool:
        adapter = self.tool_registry.get(task.definition.tool_type)
        if not adapter:
            task.status = TaskStatus.FAILED
            task.error = f"No adapter for tool type: {task.definition.tool_type}"
            return False

        if not adapter.validate_input(task):
            task.status = TaskStatus.FAILED
            task.error = "Input validation failed"
            return False

        context = {"attempt": task.attempt}
        success, result = adapter.execute(task, context)

        task.end_time = time.time()
        self.resource_pool.release(task.allocated_resources)

        if success:
            task.status = TaskStatus.COMPLETED
            task.result = result
        else:
            if task.attempt < task.definition.retries:
                task.status = TaskStatus.PENDING
                task.allocated_resources = {}
            else:
                task.status = TaskStatus.FAILED
                task.error = str(result)

        self._running = [t for t in self._running if t != task]
        if task.is_terminal:
            self._completed.append(task)

        return success

    def get_status(self) -> Dict[str, int]:
        return {
            "queued": len(self._queue),
            "running": len(self._running),
            "completed": len(self._completed),
        }


class SimpleCrypto:
    def __init__(self, key: bytes):
        self.key = key
        self._key_hash = hashlib.sha256(key).digest()

    def _xor_bytes(self, data: bytes, key: bytes) -> bytes:
        result = bytearray(len(data))
        for i in range(len(data)):
            result[i] = data[i] ^ key[i % len(key)]
        return bytes(result)

    def encrypt(self, plaintext: str) -> str:
        data = plaintext.encode('utf-8')
        nonce = random.randbytes(16)

        stream_key = hashlib.sha256(self._key_hash + nonce).digest()
        encrypted = self._xor_bytes(data, stream_key * ((len(data) // 32) + 1))

        mac = hmac.new(self._key_hash, nonce + encrypted, hashlib.sha256).digest()[:16]

        return base64.b64encode(nonce + mac + encrypted).decode('ascii')

    def decrypt(self, ciphertext: str) -> Optional[str]:
        try:
            data = base64.b64decode(ciphertext.encode('ascii'))
            if len(data) < 32:
                return None

            nonce = data[:16]
            mac = data[16:32]
            encrypted = data[32:]

            expected_mac = hmac.new(self._key_hash, nonce + encrypted, hashlib.sha256).digest()[:16]
            if not hmac.compare_digest(mac, expected_mac):
                return None

            stream_key = hashlib.sha256(self._key_hash + nonce).digest()
            decrypted = self._xor_bytes(encrypted, stream_key * ((len(encrypted) // 32) + 1))

            return decrypted.decode('utf-8')
        except Exception:
            return None


class EncryptedPersistence:
    def __init__(self, crypto: SimpleCrypto):
        self.crypto = crypto
        self._storage: Dict[str, str] = {}

    def store(self, key: str, value: str) -> bool:
        encrypted = self.crypto.encrypt(value)
        self._storage[key] = encrypted
        return True

    def retrieve(self, key: str) -> Optional[str]:
        encrypted = self._storage.get(key)
        if encrypted is None:
            return None
        return self.crypto.decrypt(encrypted)

    def delete(self, key: str) -> bool:
        if key in self._storage:
            del self._storage[key]
            return True
        return False

    def list_keys(self) -> List[str]:
        return list(self._storage.keys())

    def clear(self) -> None:
        self._storage.clear()


@dataclass
class ReportSection:
    title: str
    content: Dict[str, Any]
    subsections: List[ReportSection] = field(default_factory=list)


@dataclass
class Report:
    report_id: str
    title: str
    generated_at: float
    sections: List[ReportSection]
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReportBuilder:
    def __init__(self):
        self._sections: List[ReportSection] = []
        self._metadata: Dict[str, Any] = {}

    def add_section(self, title: str, content: Dict[str, Any]) -> ReportBuilder:
        self._sections.append(ReportSection(title=title, content=content))
        return self

    def add_metadata(self, key: str, value: Any) -> ReportBuilder:
        self._metadata[key] = value
        return self

    def build(self, report_id: str, title: str) -> Report:
        return Report(
            report_id=report_id,
            title=title,
            generated_at=time.time(),
            sections=self._sections.copy(),
            metadata=self._metadata.copy(),
        )

    def reset(self) -> ReportBuilder:
        self._sections.clear()
        self._metadata.clear()
        return self


class ReportFormatter:
    def format_text(self, report: Report) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append(f"REPORT: {report.title}")
        lines.append(f"ID: {report.report_id}")
        lines.append(f"Generated: {report.generated_at}")
        lines.append("=" * 60)

        for section in report.sections:
            lines.append(f"\n## {section.title}")
            lines.append("-" * 40)
            for key, value in section.content.items():
                lines.append(f"  {key}: {value}")

        if report.metadata:
            lines.append("\n## Metadata")
            lines.append("-" * 40)
            for key, value in report.metadata.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)

    def format_json(self, report: Report) -> str:
        def section_to_dict(s: ReportSection) -> Dict[str, Any]:
            return {
                "title": s.title,
                "content": s.content,
                "subsections": [section_to_dict(sub) for sub in s.subsections],
            }

        data = {
            "report_id": report.report_id,
            "title": report.title,
            "generated_at": report.generated_at,
            "sections": [section_to_dict(s) for s in report.sections],
            "metadata": report.metadata,
        }

        return self._to_json(data)

    def _to_json(self, obj: Any, indent: int = 0) -> str:
        space = "  " * indent
        next_space = "  " * (indent + 1)

        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            return f'"{obj}"'
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [self._to_json(item, indent + 1) for item in obj]
            return "[\n" + next_space + (",\n" + next_space).join(items) + "\n" + space + "]"
        elif isinstance(obj, dict):
            if not obj:
                return "{}"
            pairs = [f'"{k}": {self._to_json(v, indent + 1)}' for k, v in obj.items()]
            return "{\n" + next_space + (",\n" + next_space).join(pairs) + "\n" + space + "}"
        else:
            return f'"{str(obj)}"'


class Orchestrator:
    def __init__(self):
        self.resource_pool = ResourcePool()
        self.tool_registry = ToolRegistry()
        self.planner = ExecutionPlanner(self.resource_pool)
        self.scheduler = TaskScheduler(self.resource_pool, self.tool_registry)
        self.crypto = SimpleCrypto(b"orchestrator-secret-key-12345678")
        self.persistence = EncryptedPersistence(self.crypto)
        self.report_builder = ReportBuilder()
        self.report_formatter = ReportFormatter()
        self._workflows: Dict[str, WorkflowInstance] = {}

    def submit_workflow(self, definition: WorkflowDefinition) -> WorkflowInstance:
        instance_id = f"wf-{len(self._workflows) + 1}-{int(time.time() * 1000) % 10000}"
        instance = WorkflowInstance(definition=definition, instance_id=instance_id)
        instance.start_time = time.time()
        self._workflows[instance_id] = instance
        return instance

    def execute_workflow(self, instance: WorkflowInstance) -> bool:
        plan = self.planner.create_plan(instance.definition)

        for level_tasks in plan:
            for task_def in level_tasks:
                task_instance = instance.tasks[task_def.task_id]
                self.scheduler.enqueue(task_instance)

            while True:
                scheduled = self.scheduler.schedule_next()
                if scheduled:
                    self.scheduler.execute_task(scheduled)
                else:
                    break

        instance.end_time = time.time()
        return instance.status == TaskStatus.COMPLETED

    def generate_report(self, instance: WorkflowInstance) -> Report:
        self.report_builder.reset()

        self.report_builder.add_section("Workflow Summary", {
            "workflow_id": instance.definition.workflow_id,
            "instance_id": instance.instance_id,
            "status": instance.status.name,
            "total_tasks": len(instance.tasks),
            "duration": instance.end_time - instance.start_time if instance.end_time else 0,
        })

        task_stats = {"completed": 0, "failed": 0, "other": 0}
        for task in instance.tasks.values():
            if task.status == TaskStatus.COMPLETED:
                task_stats["completed"] += 1
            elif task.status == TaskStatus.FAILED:
                task_stats["failed"] += 1
            else:
                task_stats["other"] += 1

        self.report_builder.add_section("Task Statistics", task_stats)

        utilization = self.resource_pool.get_utilization()
        self.report_builder.add_section("Resource Utilization", {
            res_type.name: f"{util:.1%}" for res_type, util in utilization.items()
        })

        self.report_builder.add_metadata("generator", "AOS-M Mock Orchestrator")
        self.report_builder.add_metadata("version", "1.0.0")

        return self.report_builder.build(
            report_id=f"rpt-{instance.instance_id}",
            title=f"Workflow Execution Report: {instance.definition.name}"
        )

    def persist_workflow_state(self, instance: WorkflowInstance) -> bool:
        state = {
            "instance_id": instance.instance_id,
            "workflow_id": instance.definition.workflow_id,
            "status": instance.status.name,
            "task_count": len(instance.tasks),
        }
        state_str = str(state)
        return self.persistence.store(instance.instance_id, state_str)

    def retrieve_workflow_state(self, instance_id: str) -> Optional[str]:
        return self.persistence.retrieve(instance_id)


@dataclass
class TestCase:
    name: str
    test_func: Callable[[], bool]


class TestHarness:
    def __init__(self):
        self.tests: List[TestCase] = []
        self.passed = 0
        self.failed = 0

    def add_test(self, name: str, test_func: Callable[[], bool]) -> None:
        self.tests.append(TestCase(name=name, test_func=test_func))

    def assert_equal(self, actual: Any, expected: Any, message: str = "") -> bool:
        if actual == expected:
            return True
        raise AssertionError(f"{message}: Expected {expected}, got {actual}")

    def assert_true(self, condition: bool, message: str = "") -> bool:
        if condition:
            return True
        raise AssertionError(f"{message}: Expected True")

    def assert_not_none(self, value: Any, message: str = "") -> bool:
        if value is not None:
            return True
        raise AssertionError(f"{message}: Expected non-None")

    def run(self) -> bool:
        print("=" * 60)
        print("AOS-M MOCK ORCHESTRATOR TEST HARNESS")
        print("=" * 60)

        for test in self.tests:
            try:
                if test.test_func():
                    self.passed += 1
                    print(f"[PASS] {test.name}")
                else:
                    self.failed += 1
                    print(f"[FAIL] {test.name}")
            except AssertionError as e:
                self.failed += 1
                print(f"[FAIL] {test.name}: {str(e)}")
            except Exception as e:
                self.failed += 1
                print(f"[ERROR] {test.name}: {str(e)}")

        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0


def create_sample_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        workflow_id="wf-sample-001",
        name="Sample Analysis Pipeline",
        tasks=[
            TaskDefinition(
                task_id="compile",
                name="Compile Source",
                tool_type=ToolType.COMPILER,
                priority=Priority.HIGH,
                requirements=ResourceRequirements(cpu=4.0, memory=8.0),
                metadata={"language": "python", "optimization": "O2"},
            ),
            TaskDefinition(
                task_id="analyze-static",
                name="Static Analysis",
                tool_type=ToolType.ANALYZER,
                priority=Priority.NORMAL,
                requirements=ResourceRequirements(cpu=2.0, memory=4.0),
                dependencies=["compile"],
                metadata={"analysis_type": "static"},
            ),
            TaskDefinition(
                task_id="analyze-security",
                name="Security Analysis",
                tool_type=ToolType.ANALYZER,
                priority=Priority.HIGH,
                requirements=ResourceRequirements(cpu=2.0, memory=4.0),
                dependencies=["compile"],
                metadata={"analysis_type": "security"},
            ),
            TaskDefinition(
                task_id="transform",
                name="Code Transform",
                tool_type=ToolType.TRANSFORMER,
                priority=Priority.NORMAL,
                requirements=ResourceRequirements(cpu=2.0, memory=2.0),
                dependencies=["analyze-static", "analyze-security"],
                metadata={"transform": "optimize"},
            ),
            TaskDefinition(
                task_id="validate",
                name="Validate Output",
                tool_type=ToolType.VALIDATOR,
                priority=Priority.NORMAL,
                requirements=ResourceRequirements(cpu=1.0, memory=1.0),
                dependencies=["transform"],
            ),
            TaskDefinition(
                task_id="report",
                name="Generate Report",
                tool_type=ToolType.REPORTER,
                priority=Priority.LOW,
                requirements=ResourceRequirements(cpu=0.5, memory=0.5),
                dependencies=["validate"],
                metadata={"format": "json"},
            ),
        ],
    )


def run_aos_benchmark() -> bool:
    harness = TestHarness()

    def test_resource_allocation():
        pool = ResourcePool()
        req = ResourceRequirements(cpu=10.0, memory=100.0)
        allocated = pool.allocate(req)
        harness.assert_not_none(allocated, "Should allocate")
        harness.assert_true(ResourceType.CPU in allocated, "Should have CPU")
        pool.release(allocated)
        return True

    def test_resource_exhaustion():
        pool = ResourcePool()
        req = ResourceRequirements(cpu=1000.0)
        allocated = pool.allocate(req)
        harness.assert_true(allocated is None, "Should fail to allocate")
        return True

    def test_tool_registry():
        registry = ToolRegistry()
        tools = registry.list_tools()
        harness.assert_true(len(tools) == 5, "Should have 5 tools")
        compiler = registry.get(ToolType.COMPILER)
        harness.assert_not_none(compiler, "Should have compiler")
        return True

    def test_workflow_topological_sort():
        workflow = create_sample_workflow()
        sorted_tasks = workflow.topological_sort()
        harness.assert_equal(len(sorted_tasks), 6, "Should have 6 tasks")
        harness.assert_equal(sorted_tasks[0].task_id, "compile", "Compile should be first")
        return True

    def test_execution_planner():
        pool = ResourcePool()
        planner = ExecutionPlanner(pool)
        workflow = create_sample_workflow()
        levels = planner.create_plan(workflow)
        harness.assert_true(len(levels) >= 4, "Should have multiple levels")
        harness.assert_equal(levels[0][0].task_id, "compile", "Level 0 should have compile")
        return True

    def test_task_scheduler():
        pool = ResourcePool()
        registry = ToolRegistry()
        scheduler = TaskScheduler(pool, registry)

        task_def = TaskDefinition(
            task_id="test-task",
            name="Test Task",
            tool_type=ToolType.ANALYZER,
            priority=Priority.NORMAL,
            requirements=ResourceRequirements(cpu=1.0),
        )
        task = TaskInstance(definition=task_def)

        harness.assert_true(scheduler.enqueue(task), "Should enqueue")
        scheduled = scheduler.schedule_next()
        harness.assert_not_none(scheduled, "Should schedule")
        harness.assert_equal(scheduled.status, TaskStatus.RUNNING, "Should be running")
        return True

    def test_crypto_roundtrip():
        crypto = SimpleCrypto(b"test-key-1234567890123456")
        plaintext = "Hello, World! This is a test message."
        encrypted = crypto.encrypt(plaintext)
        decrypted = crypto.decrypt(encrypted)
        harness.assert_equal(decrypted, plaintext, "Should decrypt correctly")
        return True

    def test_encrypted_persistence():
        crypto = SimpleCrypto(b"persistence-key-12345678")
        persistence = EncryptedPersistence(crypto)

        harness.assert_true(persistence.store("key1", "value1"), "Should store")
        retrieved = persistence.retrieve("key1")
        harness.assert_equal(retrieved, "value1", "Should retrieve correctly")

        harness.assert_true(persistence.delete("key1"), "Should delete")
        harness.assert_true(persistence.retrieve("key1") is None, "Should be gone")
        return True

    def test_report_builder():
        builder = ReportBuilder()
        builder.add_section("Test Section", {"key": "value"})
        builder.add_metadata("author", "test")
        report = builder.build("rpt-001", "Test Report")

        harness.assert_equal(report.report_id, "rpt-001", "Report ID")
        harness.assert_equal(len(report.sections), 1, "Should have 1 section")
        harness.assert_equal(report.metadata["author"], "test", "Metadata")
        return True

    def test_report_formatter():
        builder = ReportBuilder()
        builder.add_section("Summary", {"total": 100, "passed": 95})
        report = builder.build("rpt-002", "Formatter Test")

        formatter = ReportFormatter()
        text = formatter.format_text(report)
        harness.assert_true("Summary" in text, "Should contain section title")
        harness.assert_true("100" in text, "Should contain total")

        json_str = formatter.format_json(report)
        harness.assert_true('"report_id"' in json_str, "Should be JSON")
        return True

    def test_full_orchestration():
        orchestrator = Orchestrator()
        workflow = create_sample_workflow()

        instance = orchestrator.submit_workflow(workflow)
        harness.assert_not_none(instance, "Should create instance")

        success = orchestrator.execute_workflow(instance)
        harness.assert_true(success, "Workflow should complete")
        harness.assert_equal(instance.status, TaskStatus.COMPLETED, "Status should be completed")

        report = orchestrator.generate_report(instance)
        harness.assert_not_none(report, "Should generate report")

        orchestrator.persist_workflow_state(instance)
        state = orchestrator.retrieve_workflow_state(instance.instance_id)
        harness.assert_not_none(state, "Should retrieve state")

        return True

    def test_tool_adapter_execution():
        registry = ToolRegistry()

        task_def = TaskDefinition(
            task_id="compiler-test",
            name="Compiler Test",
            tool_type=ToolType.COMPILER,
            priority=Priority.NORMAL,
            requirements=ResourceRequirements(),
            metadata={"language": "rust", "optimization": "O3"},
        )
        task = TaskInstance(definition=task_def)

        compiler = registry.get(ToolType.COMPILER)
        success, result = compiler.execute(task, {})

        harness.assert_true(success, "Should succeed")
        harness.assert_equal(result["language"], "rust", "Language should match")
        return True

    def test_workflow_instance_status():
        workflow = create_sample_workflow()
        instance = WorkflowInstance(definition=workflow, instance_id="test-instance")

        harness.assert_equal(instance.status, TaskStatus.PENDING, "Initial status")

        instance.tasks["compile"].status = TaskStatus.COMPLETED
        instance.tasks["analyze-static"].status = TaskStatus.RUNNING
        harness.assert_equal(instance.status, TaskStatus.RUNNING, "Running status")

        for task in instance.tasks.values():
            task.status = TaskStatus.COMPLETED
        harness.assert_equal(instance.status, TaskStatus.COMPLETED, "Completed status")
        return True

    harness.add_test("Resource Allocation", test_resource_allocation)
    harness.add_test("Resource Exhaustion", test_resource_exhaustion)
    harness.add_test("Tool Registry", test_tool_registry)
    harness.add_test("Workflow Topological Sort", test_workflow_topological_sort)
    harness.add_test("Execution Planner", test_execution_planner)
    harness.add_test("Task Scheduler", test_task_scheduler)
    harness.add_test("Crypto Roundtrip", test_crypto_roundtrip)
    harness.add_test("Encrypted Persistence", test_encrypted_persistence)
    harness.add_test("Report Builder", test_report_builder)
    harness.add_test("Report Formatter", test_report_formatter)
    harness.add_test("Full Orchestration", test_full_orchestration)
    harness.add_test("Tool Adapter Execution", test_tool_adapter_execution)
    harness.add_test("Workflow Instance Status", test_workflow_instance_status)

    return harness.run()


if __name__ == "__main__":
    success = run_aos_benchmark()
    exit(0 if success else 1)
