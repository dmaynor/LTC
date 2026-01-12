#!/usr/bin/env python3
"""
Live Triage Scanner (LTS) Benchmark
A mock system triage scanner demonstrating filesystem scanning,
process enumeration, parallel execution, rule engines, and CLI interface.
"""

from __future__ import annotations
import hashlib
import os
import random
import threading
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from queue import Queue, Empty
from typing import (
    Any, Callable, Dict, Generic, Iterator, List, Optional,
    Set, Tuple, TypeVar, Union
)

GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)


class SeverityLevel(Enum):
    INFO = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5


class FindingType(Enum):
    FILE_ANOMALY = auto()
    PROCESS_ANOMALY = auto()
    PERMISSION_ISSUE = auto()
    SUSPICIOUS_PATTERN = auto()
    CONFIGURATION_ISSUE = auto()
    NETWORK_ANOMALY = auto()


class ScanStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class FileInfo:
    path: str
    name: str
    size: int
    modified_time: float
    is_directory: bool
    permissions: int
    owner: str = "root"
    group: str = "root"
    extension: str = ""
    hash_md5: Optional[str] = None

    @classmethod
    def from_path(cls, path: Path) -> Optional[FileInfo]:
        try:
            stat = path.stat()
            return cls(
                path=str(path),
                name=path.name,
                size=stat.st_size,
                modified_time=stat.st_mtime,
                is_directory=path.is_dir(),
                permissions=stat.st_mode,
                extension=path.suffix.lower() if not path.is_dir() else "",
            )
        except (OSError, PermissionError):
            return None

    def compute_hash(self) -> Optional[str]:
        if self.is_directory:
            return None
        try:
            with open(self.path, 'rb') as f:
                return hashlib.md5(f.read(1024 * 1024)).hexdigest()
        except (OSError, PermissionError):
            return None


@dataclass
class ProcessInfo:
    pid: int
    name: str
    cmdline: str
    user: str
    cpu_percent: float
    memory_percent: float
    status: str
    created_time: float
    parent_pid: Optional[int] = None
    children_pids: List[int] = field(default_factory=list)
    open_files_count: int = 0
    connections_count: int = 0


@dataclass
class Finding:
    finding_id: str
    finding_type: FindingType
    severity: SeverityLevel
    title: str
    description: str
    target: str
    evidence: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "type": self.finding_type.name,
            "severity": self.severity.name,
            "title": self.title,
            "description": self.description,
            "target": self.target,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "timestamp": self.timestamp,
        }


@dataclass
class ScanTarget:
    target_type: str
    path: Optional[str] = None
    pattern: Optional[str] = None
    recursive: bool = True
    max_depth: int = 10


@dataclass
class ScanConfiguration:
    targets: List[ScanTarget]
    max_workers: int = 4
    timeout_seconds: float = 300.0
    include_hidden: bool = False
    compute_hashes: bool = False
    enabled_rules: List[str] = field(default_factory=list)


@dataclass
class ScanResult:
    scan_id: str
    status: ScanStatus
    start_time: float
    end_time: Optional[float] = None
    files_scanned: int = 0
    processes_scanned: int = 0
    findings: List[Finding] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        if self.end_time:
            return self.end_time - self.start_time
        return 0.0

    def summary(self) -> Dict[str, Any]:
        severity_counts = {}
        for finding in self.findings:
            sev = finding.severity.name
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        return {
            "scan_id": self.scan_id,
            "status": self.status.name,
            "duration": self.duration,
            "files_scanned": self.files_scanned,
            "processes_scanned": self.processes_scanned,
            "total_findings": len(self.findings),
            "findings_by_severity": severity_counts,
            "errors": len(self.errors),
        }


class Rule(ABC):
    rule_id: str
    name: str
    description: str
    severity: SeverityLevel
    enabled: bool = True

    @abstractmethod
    def evaluate(self, target: Any) -> Optional[Finding]:
        pass

    def create_finding(
        self,
        target: str,
        title: str,
        description: str,
        evidence: Dict[str, Any]
    ) -> Finding:
        return Finding(
            finding_id=f"FND-{self.rule_id}-{int(time.time() * 1000) % 100000}",
            finding_type=FindingType.FILE_ANOMALY,
            severity=self.severity,
            title=title,
            description=description,
            target=target,
            evidence=evidence,
        )


class LargeFileRule(Rule):
    rule_id = "FILE-001"
    name = "Large File Detection"
    description = "Detects unusually large files"
    severity = SeverityLevel.LOW

    def __init__(self, threshold_mb: float = 100.0):
        self.threshold_bytes = threshold_mb * 1024 * 1024

    def evaluate(self, target: FileInfo) -> Optional[Finding]:
        if target.is_directory:
            return None
        if target.size > self.threshold_bytes:
            return self.create_finding(
                target=target.path,
                title=f"Large file detected: {target.name}",
                description=f"File size {target.size / (1024*1024):.2f} MB exceeds threshold",
                evidence={"size_bytes": target.size, "threshold": self.threshold_bytes},
            )
        return None


class SuspiciousExtensionRule(Rule):
    rule_id = "FILE-002"
    name = "Suspicious Extension Detection"
    description = "Detects files with suspicious extensions"
    severity = SeverityLevel.MEDIUM

    SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".cmd", ".ps1", ".vbs", ".dll", ".scr", ".pif"}

    def evaluate(self, target: FileInfo) -> Optional[Finding]:
        if target.is_directory:
            return None
        if target.extension in self.SUSPICIOUS_EXTENSIONS:
            finding = self.create_finding(
                target=target.path,
                title=f"Suspicious file extension: {target.extension}",
                description=f"File {target.name} has potentially dangerous extension",
                evidence={"extension": target.extension, "filename": target.name},
            )
            finding.finding_type = FindingType.SUSPICIOUS_PATTERN
            finding.recommendations = [
                "Verify the file source and legitimacy",
                "Scan with antivirus software",
            ]
            return finding
        return None


class WorldWritableRule(Rule):
    rule_id = "FILE-003"
    name = "World Writable File Detection"
    description = "Detects files with world-writable permissions"
    severity = SeverityLevel.HIGH

    def evaluate(self, target: FileInfo) -> Optional[Finding]:
        if target.permissions & 0o002:
            finding = self.create_finding(
                target=target.path,
                title=f"World-writable file: {target.name}",
                description="File has insecure world-writable permissions",
                evidence={"permissions": oct(target.permissions)},
            )
            finding.finding_type = FindingType.PERMISSION_ISSUE
            finding.recommendations = [
                "Remove world-write permission: chmod o-w <file>",
                "Review file ownership and access requirements",
            ]
            return finding
        return None


class HiddenFileRule(Rule):
    rule_id = "FILE-004"
    name = "Hidden File Detection"
    description = "Detects hidden files in unusual locations"
    severity = SeverityLevel.LOW

    def evaluate(self, target: FileInfo) -> Optional[Finding]:
        if target.name.startswith('.') and not target.is_directory:
            if not target.name in {'.gitignore', '.gitattributes', '.editorconfig'}:
                return self.create_finding(
                    target=target.path,
                    title=f"Hidden file detected: {target.name}",
                    description="Hidden file found that may warrant review",
                    evidence={"filename": target.name},
                )
        return None


class HighCPUProcessRule(Rule):
    rule_id = "PROC-001"
    name = "High CPU Process Detection"
    description = "Detects processes consuming excessive CPU"
    severity = SeverityLevel.MEDIUM

    def __init__(self, threshold_percent: float = 80.0):
        self.threshold = threshold_percent

    def evaluate(self, target: ProcessInfo) -> Optional[Finding]:
        if target.cpu_percent > self.threshold:
            finding = self.create_finding(
                target=f"PID {target.pid}",
                title=f"High CPU usage: {target.name}",
                description=f"Process consuming {target.cpu_percent:.1f}% CPU",
                evidence={
                    "pid": target.pid,
                    "cpu_percent": target.cpu_percent,
                    "cmdline": target.cmdline,
                },
            )
            finding.finding_type = FindingType.PROCESS_ANOMALY
            return finding
        return None


class HighMemoryProcessRule(Rule):
    rule_id = "PROC-002"
    name = "High Memory Process Detection"
    description = "Detects processes consuming excessive memory"
    severity = SeverityLevel.MEDIUM

    def __init__(self, threshold_percent: float = 50.0):
        self.threshold = threshold_percent

    def evaluate(self, target: ProcessInfo) -> Optional[Finding]:
        if target.memory_percent > self.threshold:
            finding = self.create_finding(
                target=f"PID {target.pid}",
                title=f"High memory usage: {target.name}",
                description=f"Process consuming {target.memory_percent:.1f}% memory",
                evidence={
                    "pid": target.pid,
                    "memory_percent": target.memory_percent,
                    "cmdline": target.cmdline,
                },
            )
            finding.finding_type = FindingType.PROCESS_ANOMALY
            return finding
        return None


class SuspiciousProcessRule(Rule):
    rule_id = "PROC-003"
    name = "Suspicious Process Detection"
    description = "Detects processes with suspicious characteristics"
    severity = SeverityLevel.HIGH

    SUSPICIOUS_NAMES = {"nc", "netcat", "ncat", "cryptominer", "xmrig"}

    def evaluate(self, target: ProcessInfo) -> Optional[Finding]:
        name_lower = target.name.lower()
        if name_lower in self.SUSPICIOUS_NAMES:
            finding = self.create_finding(
                target=f"PID {target.pid}",
                title=f"Suspicious process: {target.name}",
                description=f"Process matches known suspicious pattern",
                evidence={
                    "pid": target.pid,
                    "name": target.name,
                    "cmdline": target.cmdline,
                    "user": target.user,
                },
            )
            finding.finding_type = FindingType.SUSPICIOUS_PATTERN
            finding.severity = SeverityLevel.CRITICAL
            finding.recommendations = [
                "Investigate process origin and purpose",
                "Check for unauthorized network connections",
                "Review user account activity",
            ]
            return finding
        return None


class RuleEngine:
    def __init__(self):
        self._file_rules: List[Rule] = []
        self._process_rules: List[Rule] = []
        self._register_default_rules()

    def _register_default_rules(self) -> None:
        self._file_rules = [
            LargeFileRule(),
            SuspiciousExtensionRule(),
            WorldWritableRule(),
            HiddenFileRule(),
        ]
        self._process_rules = [
            HighCPUProcessRule(),
            HighMemoryProcessRule(),
            SuspiciousProcessRule(),
        ]

    def add_file_rule(self, rule: Rule) -> None:
        self._file_rules.append(rule)

    def add_process_rule(self, rule: Rule) -> None:
        self._process_rules.append(rule)

    def evaluate_file(self, file_info: FileInfo) -> List[Finding]:
        findings = []
        for rule in self._file_rules:
            if rule.enabled:
                finding = rule.evaluate(file_info)
                if finding:
                    findings.append(finding)
        return findings

    def evaluate_process(self, process_info: ProcessInfo) -> List[Finding]:
        findings = []
        for rule in self._process_rules:
            if rule.enabled:
                finding = rule.evaluate(process_info)
                if finding:
                    findings.append(finding)
        return findings

    def list_rules(self) -> List[Dict[str, Any]]:
        rules = []
        for rule in self._file_rules + self._process_rules:
            rules.append({
                "rule_id": rule.rule_id,
                "name": rule.name,
                "description": rule.description,
                "severity": rule.severity.name,
                "enabled": rule.enabled,
            })
        return rules


class FileScanner:
    def __init__(self, rule_engine: RuleEngine):
        self.rule_engine = rule_engine
        self._files_scanned = 0
        self._lock = threading.Lock()

    def scan_path(
        self,
        path: Path,
        recursive: bool = True,
        max_depth: int = 10,
        include_hidden: bool = False,
        compute_hashes: bool = False
    ) -> Iterator[Tuple[FileInfo, List[Finding]]]:
        self._files_scanned = 0

        def should_include(p: Path) -> bool:
            if not include_hidden and p.name.startswith('.'):
                return include_hidden
            return True

        def scan_dir(dir_path: Path, depth: int) -> Iterator[Tuple[FileInfo, List[Finding]]]:
            if depth > max_depth:
                return

            try:
                entries = list(dir_path.iterdir())
            except PermissionError:
                return

            for entry in entries:
                if not should_include(entry):
                    continue

                file_info = FileInfo.from_path(entry)
                if file_info is None:
                    continue

                if compute_hashes and not file_info.is_directory:
                    file_info.hash_md5 = file_info.compute_hash()

                with self._lock:
                    self._files_scanned += 1

                findings = self.rule_engine.evaluate_file(file_info)
                yield file_info, findings

                if recursive and file_info.is_directory:
                    yield from scan_dir(entry, depth + 1)

        yield from scan_dir(path, 0)

    @property
    def files_scanned(self) -> int:
        with self._lock:
            return self._files_scanned


class MockProcessEnumerator:
    def __init__(self, rule_engine: RuleEngine):
        self.rule_engine = rule_engine
        self._mock_processes = self._generate_mock_processes()

    def _generate_mock_processes(self) -> List[ProcessInfo]:
        processes = [
            ProcessInfo(1, "systemd", "/sbin/init", "root", 0.1, 0.5, "running", time.time() - 86400),
            ProcessInfo(2, "kthreadd", "[kthreadd]", "root", 0.0, 0.0, "running", time.time() - 86400),
            ProcessInfo(100, "sshd", "/usr/sbin/sshd -D", "root", 0.2, 0.3, "running", time.time() - 3600),
            ProcessInfo(101, "nginx", "/usr/sbin/nginx -g 'daemon off;'", "www-data", 2.5, 1.2, "running", time.time() - 7200),
            ProcessInfo(200, "python3", "python3 app.py", "user", 15.0, 8.5, "running", time.time() - 1800),
            ProcessInfo(201, "node", "node server.js", "user", 5.0, 12.0, "running", time.time() - 900),
            ProcessInfo(300, "postgres", "postgres: main", "postgres", 3.0, 25.0, "running", time.time() - 43200),
            ProcessInfo(400, "redis-server", "redis-server *:6379", "redis", 1.0, 5.0, "running", time.time() - 21600),
            ProcessInfo(500, "stress", "stress --cpu 4", "user", 95.0, 2.0, "running", time.time() - 60),
            ProcessInfo(600, "python3", "python3 memory_hog.py", "user", 10.0, 75.0, "running", time.time() - 120),
        ]
        return processes

    def enumerate(self) -> Iterator[Tuple[ProcessInfo, List[Finding]]]:
        for process in self._mock_processes:
            findings = self.rule_engine.evaluate_process(process)
            yield process, findings

    @property
    def process_count(self) -> int:
        return len(self._mock_processes)


class WorkerPool:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self._executor: Optional[ThreadPoolExecutor] = None
        self._futures: List[Future] = []
        self._results: Queue = Queue()
        self._lock = threading.Lock()

    def start(self) -> None:
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self._futures = []

    def submit(self, fn: Callable, *args, **kwargs) -> Future:
        if self._executor is None:
            raise RuntimeError("Worker pool not started")
        future = self._executor.submit(fn, *args, **kwargs)
        with self._lock:
            self._futures.append(future)
        return future

    def wait_all(self, timeout: Optional[float] = None) -> List[Any]:
        results = []
        with self._lock:
            futures = self._futures.copy()

        for future in as_completed(futures, timeout=timeout):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                results.append(e)

        return results

    def shutdown(self, wait: bool = True) -> None:
        if self._executor:
            self._executor.shutdown(wait=wait)
            self._executor = None

    @property
    def active_count(self) -> int:
        with self._lock:
            return sum(1 for f in self._futures if f.running())

    @property
    def completed_count(self) -> int:
        with self._lock:
            return sum(1 for f in self._futures if f.done())


class TriageScanner:
    def __init__(self, config: Optional[ScanConfiguration] = None):
        self.config = config or ScanConfiguration(targets=[])
        self.rule_engine = RuleEngine()
        self.file_scanner = FileScanner(self.rule_engine)
        self.process_enum = MockProcessEnumerator(self.rule_engine)
        self.worker_pool = WorkerPool(self.config.max_workers)
        self._current_result: Optional[ScanResult] = None

    def scan(self) -> ScanResult:
        scan_id = f"SCAN-{int(time.time() * 1000) % 1000000}"
        self._current_result = ScanResult(
            scan_id=scan_id,
            status=ScanStatus.RUNNING,
            start_time=time.time(),
        )

        try:
            self.worker_pool.start()

            for target in self.config.targets:
                if target.target_type == "filesystem":
                    self._scan_filesystem(target)
                elif target.target_type == "processes":
                    self._scan_processes()

            self.worker_pool.shutdown(wait=True)

            self._current_result.status = ScanStatus.COMPLETED
        except Exception as e:
            self._current_result.status = ScanStatus.FAILED
            self._current_result.errors.append(str(e))

        self._current_result.end_time = time.time()
        return self._current_result

    def _scan_filesystem(self, target: ScanTarget) -> None:
        if not target.path:
            return

        path = Path(target.path)
        if not path.exists():
            self._current_result.errors.append(f"Path not found: {target.path}")
            return

        for file_info, findings in self.file_scanner.scan_path(
            path,
            recursive=target.recursive,
            max_depth=target.max_depth,
            include_hidden=self.config.include_hidden,
            compute_hashes=self.config.compute_hashes,
        ):
            self._current_result.files_scanned += 1
            self._current_result.findings.extend(findings)

    def _scan_processes(self) -> None:
        for process_info, findings in self.process_enum.enumerate():
            self._current_result.processes_scanned += 1
            self._current_result.findings.extend(findings)


class ReportGenerator:
    def __init__(self):
        self._indent = "  "

    def generate_text_report(self, result: ScanResult) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append("LIVE TRIAGE SCANNER REPORT")
        lines.append("=" * 70)
        lines.append("")

        summary = result.summary()
        lines.append("SCAN SUMMARY")
        lines.append("-" * 40)
        lines.append(f"Scan ID:           {summary['scan_id']}")
        lines.append(f"Status:            {summary['status']}")
        lines.append(f"Duration:          {summary['duration']:.2f} seconds")
        lines.append(f"Files Scanned:     {summary['files_scanned']}")
        lines.append(f"Processes Scanned: {summary['processes_scanned']}")
        lines.append(f"Total Findings:    {summary['total_findings']}")
        lines.append(f"Errors:            {summary['errors']}")
        lines.append("")

        if summary['findings_by_severity']:
            lines.append("FINDINGS BY SEVERITY")
            lines.append("-" * 40)
            for sev, count in sorted(summary['findings_by_severity'].items(),
                                     key=lambda x: SeverityLevel[x[0]].value,
                                     reverse=True):
                lines.append(f"  {sev}: {count}")
            lines.append("")

        if result.findings:
            lines.append("DETAILED FINDINGS")
            lines.append("-" * 40)
            for i, finding in enumerate(result.findings, 1):
                lines.append(f"\n[{i}] {finding.title}")
                lines.append(f"    Severity: {finding.severity.name}")
                lines.append(f"    Type:     {finding.finding_type.name}")
                lines.append(f"    Target:   {finding.target}")
                lines.append(f"    {finding.description}")
                if finding.recommendations:
                    lines.append("    Recommendations:")
                    for rec in finding.recommendations:
                        lines.append(f"      - {rec}")

        lines.append("")
        lines.append("=" * 70)
        lines.append("END OF REPORT")
        lines.append("=" * 70)

        return "\n".join(lines)

    def generate_json_report(self, result: ScanResult) -> str:
        data = {
            "scan_id": result.scan_id,
            "status": result.status.name,
            "start_time": result.start_time,
            "end_time": result.end_time,
            "duration": result.duration,
            "files_scanned": result.files_scanned,
            "processes_scanned": result.processes_scanned,
            "findings": [f.to_dict() for f in result.findings],
            "errors": result.errors,
            "summary": result.summary(),
        }
        return self._to_json(data)

    def _to_json(self, obj: Any, depth: int = 0) -> str:
        indent = self._indent * depth
        next_indent = self._indent * (depth + 1)

        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, (int, float)):
            return str(obj)
        elif isinstance(obj, str):
            escaped = obj.replace('\\', '\\\\').replace('"', '\\"')
            escaped = escaped.replace('\n', '\\n').replace('\r', '\\r')
            return f'"{escaped}"'
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [self._to_json(item, depth + 1) for item in obj]
            return "[\n" + next_indent + (",\n" + next_indent).join(items) + "\n" + indent + "]"
        elif isinstance(obj, dict):
            if not obj:
                return "{}"
            pairs = [f'"{k}": {self._to_json(v, depth + 1)}' for k, v in obj.items()]
            return "{\n" + next_indent + (",\n" + next_indent).join(pairs) + "\n" + indent + "}"
        else:
            return f'"{str(obj)}"'


class CLIInterface:
    def __init__(self):
        self.scanner: Optional[TriageScanner] = None
        self.report_generator = ReportGenerator()

    def parse_args(self, args: List[str]) -> Dict[str, Any]:
        parsed = {
            "command": "scan",
            "targets": [],
            "max_workers": 4,
            "recursive": True,
            "include_hidden": False,
            "compute_hashes": False,
            "output_format": "text",
            "output_file": None,
            "list_rules": False,
        }

        i = 0
        while i < len(args):
            arg = args[i]

            if arg in ("-h", "--help"):
                parsed["command"] = "help"
            elif arg in ("-l", "--list-rules"):
                parsed["list_rules"] = True
            elif arg in ("-t", "--target"):
                if i + 1 < len(args):
                    parsed["targets"].append(args[i + 1])
                    i += 1
            elif arg in ("-w", "--workers"):
                if i + 1 < len(args):
                    parsed["max_workers"] = int(args[i + 1])
                    i += 1
            elif arg in ("-r", "--recursive"):
                parsed["recursive"] = True
            elif arg in ("--no-recursive",):
                parsed["recursive"] = False
            elif arg in ("--include-hidden",):
                parsed["include_hidden"] = True
            elif arg in ("--compute-hashes",):
                parsed["compute_hashes"] = True
            elif arg in ("-f", "--format"):
                if i + 1 < len(args):
                    parsed["output_format"] = args[i + 1]
                    i += 1
            elif arg in ("-o", "--output"):
                if i + 1 < len(args):
                    parsed["output_file"] = args[i + 1]
                    i += 1
            elif arg == "--processes":
                parsed["targets"].append("__processes__")
            elif not arg.startswith("-"):
                parsed["targets"].append(arg)

            i += 1

        return parsed

    def run(self, args: List[str]) -> int:
        parsed = self.parse_args(args)

        if parsed["command"] == "help":
            self._print_help()
            return 0

        if parsed["list_rules"]:
            self._list_rules()
            return 0

        targets = []
        for target in parsed["targets"]:
            if target == "__processes__":
                targets.append(ScanTarget(target_type="processes"))
            else:
                targets.append(ScanTarget(
                    target_type="filesystem",
                    path=target,
                    recursive=parsed["recursive"],
                ))

        if not targets:
            targets.append(ScanTarget(target_type="processes"))

        config = ScanConfiguration(
            targets=targets,
            max_workers=parsed["max_workers"],
            include_hidden=parsed["include_hidden"],
            compute_hashes=parsed["compute_hashes"],
        )

        self.scanner = TriageScanner(config)
        result = self.scanner.scan()

        if parsed["output_format"] == "json":
            report = self.report_generator.generate_json_report(result)
        else:
            report = self.report_generator.generate_text_report(result)

        if parsed["output_file"]:
            with open(parsed["output_file"], "w") as f:
                f.write(report)
        else:
            print(report)

        return 0 if result.status == ScanStatus.COMPLETED else 1

    def _print_help(self) -> None:
        help_text = """
Live Triage Scanner (LTS) - System Triage Tool

Usage: lts_scanner.py [OPTIONS] [TARGETS...]

Options:
  -h, --help          Show this help message
  -l, --list-rules    List all available rules
  -t, --target PATH   Add scan target (can be used multiple times)
  -w, --workers N     Number of worker threads (default: 4)
  -r, --recursive     Scan directories recursively (default)
  --no-recursive      Don't scan recursively
  --include-hidden    Include hidden files in scan
  --compute-hashes    Compute file hashes
  -f, --format FMT    Output format: text, json (default: text)
  -o, --output FILE   Write output to file
  --processes         Scan running processes

Examples:
  lts_scanner.py --processes
  lts_scanner.py /home/user --recursive
  lts_scanner.py -t /var/log -f json -o report.json
"""
        print(help_text)

    def _list_rules(self) -> None:
        rule_engine = RuleEngine()
        rules = rule_engine.list_rules()

        print("Available Rules:")
        print("-" * 60)
        for rule in rules:
            status = "ENABLED" if rule["enabled"] else "DISABLED"
            print(f"[{rule['rule_id']}] {rule['name']}")
            print(f"  Severity: {rule['severity']}")
            print(f"  Status:   {status}")
            print(f"  {rule['description']}")
            print()


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

    def assert_greater(self, actual: Any, expected: Any, message: str = "") -> bool:
        if actual > expected:
            return True
        raise AssertionError(f"{message}: Expected {actual} > {expected}")

    def run(self) -> bool:
        print("=" * 60)
        print("LIVE TRIAGE SCANNER TEST HARNESS")
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


def run_lts_benchmark() -> bool:
    harness = TestHarness()

    def test_file_info_creation():
        info = FileInfo(
            path="/test/file.txt",
            name="file.txt",
            size=1024,
            modified_time=time.time(),
            is_directory=False,
            permissions=0o644,
            extension=".txt",
        )
        harness.assert_equal(info.name, "file.txt", "Name")
        harness.assert_equal(info.extension, ".txt", "Extension")
        return True

    def test_process_info_creation():
        info = ProcessInfo(
            pid=100,
            name="test_proc",
            cmdline="/bin/test",
            user="root",
            cpu_percent=5.0,
            memory_percent=10.0,
            status="running",
            created_time=time.time(),
        )
        harness.assert_equal(info.pid, 100, "PID")
        harness.assert_equal(info.name, "test_proc", "Name")
        return True

    def test_finding_creation():
        finding = Finding(
            finding_id="TEST-001",
            finding_type=FindingType.FILE_ANOMALY,
            severity=SeverityLevel.MEDIUM,
            title="Test Finding",
            description="A test finding",
            target="/test/path",
        )
        harness.assert_equal(finding.severity, SeverityLevel.MEDIUM, "Severity")
        data = finding.to_dict()
        harness.assert_equal(data["finding_id"], "TEST-001", "Dict conversion")
        return True

    def test_large_file_rule():
        rule = LargeFileRule(threshold_mb=1.0)
        large_file = FileInfo(
            path="/large.bin",
            name="large.bin",
            size=10 * 1024 * 1024,
            modified_time=time.time(),
            is_directory=False,
            permissions=0o644,
        )
        finding = rule.evaluate(large_file)
        harness.assert_not_none(finding, "Should detect large file")
        return True

    def test_suspicious_extension_rule():
        rule = SuspiciousExtensionRule()
        exe_file = FileInfo(
            path="/test.exe",
            name="test.exe",
            size=1024,
            modified_time=time.time(),
            is_directory=False,
            permissions=0o644,
            extension=".exe",
        )
        finding = rule.evaluate(exe_file)
        harness.assert_not_none(finding, "Should detect .exe")
        harness.assert_equal(finding.severity, SeverityLevel.MEDIUM, "Severity")
        return True

    def test_world_writable_rule():
        rule = WorldWritableRule()
        writable_file = FileInfo(
            path="/writable.txt",
            name="writable.txt",
            size=100,
            modified_time=time.time(),
            is_directory=False,
            permissions=0o777,
        )
        finding = rule.evaluate(writable_file)
        harness.assert_not_none(finding, "Should detect world-writable")
        harness.assert_equal(finding.severity, SeverityLevel.HIGH, "Severity")
        return True

    def test_high_cpu_rule():
        rule = HighCPUProcessRule(threshold_percent=80.0)
        high_cpu = ProcessInfo(
            pid=999,
            name="hog",
            cmdline="./hog",
            user="user",
            cpu_percent=95.0,
            memory_percent=5.0,
            status="running",
            created_time=time.time(),
        )
        finding = rule.evaluate(high_cpu)
        harness.assert_not_none(finding, "Should detect high CPU")
        return True

    def test_rule_engine():
        engine = RuleEngine()
        rules = engine.list_rules()
        harness.assert_greater(len(rules), 5, "Should have multiple rules")

        suspicious_file = FileInfo(
            path="/test.exe",
            name="test.exe",
            size=1024,
            modified_time=time.time(),
            is_directory=False,
            permissions=0o644,
            extension=".exe",
        )
        findings = engine.evaluate_file(suspicious_file)
        harness.assert_greater(len(findings), 0, "Should have findings")
        return True

    def test_mock_process_enumerator():
        engine = RuleEngine()
        enumerator = MockProcessEnumerator(engine)
        harness.assert_greater(enumerator.process_count, 0, "Should have processes")

        findings_count = 0
        for _, findings in enumerator.enumerate():
            findings_count += len(findings)

        harness.assert_greater(findings_count, 0, "Should detect some issues")
        return True

    def test_worker_pool():
        pool = WorkerPool(max_workers=2)
        pool.start()

        def task(x):
            time.sleep(0.01)
            return x * 2

        pool.submit(task, 1)
        pool.submit(task, 2)
        pool.submit(task, 3)

        results = pool.wait_all(timeout=5.0)
        harness.assert_equal(len(results), 3, "Should have 3 results")
        pool.shutdown()
        return True

    def test_triage_scanner():
        config = ScanConfiguration(
            targets=[ScanTarget(target_type="processes")],
            max_workers=2,
        )
        scanner = TriageScanner(config)
        result = scanner.scan()

        harness.assert_equal(result.status, ScanStatus.COMPLETED, "Should complete")
        harness.assert_greater(result.processes_scanned, 0, "Should scan processes")
        return True

    def test_report_generator_text():
        result = ScanResult(
            scan_id="TEST-001",
            status=ScanStatus.COMPLETED,
            start_time=time.time() - 10,
            end_time=time.time(),
            files_scanned=100,
            processes_scanned=50,
            findings=[
                Finding(
                    finding_id="F-001",
                    finding_type=FindingType.FILE_ANOMALY,
                    severity=SeverityLevel.HIGH,
                    title="Test Finding",
                    description="Description",
                    target="/test",
                )
            ],
        )

        generator = ReportGenerator()
        report = generator.generate_text_report(result)

        harness.assert_true("TEST-001" in report, "Should contain scan ID")
        harness.assert_true("Test Finding" in report, "Should contain finding")
        return True

    def test_report_generator_json():
        result = ScanResult(
            scan_id="TEST-002",
            status=ScanStatus.COMPLETED,
            start_time=time.time(),
            end_time=time.time(),
            files_scanned=50,
        )

        generator = ReportGenerator()
        report = generator.generate_json_report(result)

        harness.assert_true('"scan_id"' in report, "Should be JSON")
        harness.assert_true('"TEST-002"' in report, "Should contain scan ID")
        return True

    def test_cli_arg_parsing():
        cli = CLIInterface()

        args = ["--processes", "-w", "8", "-f", "json"]
        parsed = cli.parse_args(args)

        harness.assert_equal(parsed["max_workers"], 8, "Workers")
        harness.assert_equal(parsed["output_format"], "json", "Format")
        harness.assert_true("__processes__" in parsed["targets"], "Processes target")
        return True

    def test_full_scan_pipeline():
        config = ScanConfiguration(
            targets=[ScanTarget(target_type="processes")],
            max_workers=2,
        )
        scanner = TriageScanner(config)
        result = scanner.scan()

        generator = ReportGenerator()
        text_report = generator.generate_text_report(result)
        json_report = generator.generate_json_report(result)

        harness.assert_true(len(text_report) > 100, "Text report generated")
        harness.assert_true(len(json_report) > 100, "JSON report generated")
        harness.assert_equal(result.status, ScanStatus.COMPLETED, "Completed")
        return True

    harness.add_test("FileInfo Creation", test_file_info_creation)
    harness.add_test("ProcessInfo Creation", test_process_info_creation)
    harness.add_test("Finding Creation", test_finding_creation)
    harness.add_test("Large File Rule", test_large_file_rule)
    harness.add_test("Suspicious Extension Rule", test_suspicious_extension_rule)
    harness.add_test("World Writable Rule", test_world_writable_rule)
    harness.add_test("High CPU Rule", test_high_cpu_rule)
    harness.add_test("Rule Engine", test_rule_engine)
    harness.add_test("Mock Process Enumerator", test_mock_process_enumerator)
    harness.add_test("Worker Pool", test_worker_pool)
    harness.add_test("Triage Scanner", test_triage_scanner)
    harness.add_test("Report Generator Text", test_report_generator_text)
    harness.add_test("Report Generator JSON", test_report_generator_json)
    harness.add_test("CLI Argument Parsing", test_cli_arg_parsing)
    harness.add_test("Full Scan Pipeline", test_full_scan_pipeline)

    return harness.run()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != "--test":
        cli = CLIInterface()
        exit(cli.run(sys.argv[1:]))
    else:
        success = run_lts_benchmark()
        exit(0 if success else 1)
