#!/usr/bin/env python3
"""
Complex Task Suite (CTS) Benchmark
A comprehensive benchmark implementing structured data processing,
aggregation, rule engines, error handling, and serialization.
"""

from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any, Callable, Dict, Generic, List, Optional,
    Tuple, TypeVar, Union
)

GLOBAL_SEED = 42
random.seed(GLOBAL_SEED)

class Status(Enum):
    ACTIVE = auto()
    INACTIVE = auto()
    PENDING = auto()
    ARCHIVED = auto()

class Category(Enum):
    ALPHA = auto()
    BETA = auto()
    GAMMA = auto()
    DELTA = auto()

class ErrorSeverity(Enum):
    RECOVERABLE = auto()
    FATAL = auto()

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Result(Generic[T, E]):
    value: Optional[T] = None
    error: Optional[E] = None

    @property
    def is_ok(self) -> bool:
        return self.error is None

    @property
    def is_err(self) -> bool:
        return self.error is not None

    @staticmethod
    def ok(value: T) -> Result[T, E]:
        return Result(value=value, error=None)

    @staticmethod
    def err(error: E) -> Result[T, E]:
        return Result(value=None, error=error)

    def map(self, func: Callable[[T], Any]) -> Result:
        if self.is_ok:
            return Result.ok(func(self.value))
        return Result.err(self.error)

    def and_then(self, func: Callable[[T], Result]) -> Result:
        if self.is_ok:
            return func(self.value)
        return Result.err(self.error)

    def unwrap(self) -> T:
        if self.is_err:
            raise ValueError(f"Called unwrap on error: {self.error}")
        return self.value

    def unwrap_or(self, default: T) -> T:
        return self.value if self.is_ok else default

@dataclass
class ValidationError:
    field: str
    message: str
    severity: ErrorSeverity = ErrorSeverity.RECOVERABLE
    row_index: Optional[int] = None

@dataclass
class ProcessingError:
    code: str
    message: str
    severity: ErrorSeverity
    cause: Optional[ProcessingError] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def chain(self, new_message: str, new_code: str) -> ProcessingError:
        return ProcessingError(
            code=new_code,
            message=new_message,
            severity=self.severity,
            cause=self,
            context=self.context.copy()
        )

    def with_context(self, key: str, value: Any) -> ProcessingError:
        new_ctx = self.context.copy()
        new_ctx[key] = value
        return ProcessingError(
            code=self.code,
            message=self.message,
            severity=self.severity,
            cause=self.cause,
            context=new_ctx
        )

    def root_cause(self) -> ProcessingError:
        current = self
        while current.cause is not None:
            current = current.cause
        return current

    def error_chain(self) -> List[ProcessingError]:
        chain = []
        current: Optional[ProcessingError] = self
        while current is not None:
            chain.append(current)
            current = current.cause
        return chain

@dataclass
class Record:
    id: int
    name: str
    value: float
    quantity: int
    status: Status
    category: Category
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    valid_records: List[Record]
    invalid_count: int
    errors: List[ValidationError]

@dataclass
class AggregationStats:
    count: int
    min_value: float
    max_value: float
    sum_value: float
    mean_value: float
    min_quantity: int
    max_quantity: int
    sum_quantity: int

@dataclass
class GroupSummary:
    key: str
    stats: AggregationStats
    records: List[Record]
    labels: List[str] = field(default_factory=list)
    score: float = 0.0

@dataclass
class AggregationReport:
    groups: Dict[str, GroupSummary]
    total_records: int
    total_groups: int
    global_stats: AggregationStats

class FieldValidator:
    @staticmethod
    def validate_required(value: Any, field_name: str) -> Optional[ValidationError]:
        if value is None or (isinstance(value, str) and not value.strip()):
            return ValidationError(
                field=field_name,
                message=f"Field '{field_name}' is required",
                severity=ErrorSeverity.FATAL
            )
        return None

    @staticmethod
    def validate_numeric_range(
        value: float,
        field_name: str,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> Optional[ValidationError]:
        if min_val is not None and value < min_val:
            return ValidationError(
                field=field_name,
                message=f"Field '{field_name}' value {value} is below minimum {min_val}",
                severity=ErrorSeverity.RECOVERABLE
            )
        if max_val is not None and value > max_val:
            return ValidationError(
                field=field_name,
                message=f"Field '{field_name}' value {value} exceeds maximum {max_val}",
                severity=ErrorSeverity.RECOVERABLE
            )
        return None

    @staticmethod
    def validate_enum_membership(
        value: str,
        field_name: str,
        enum_class: type
    ) -> Optional[ValidationError]:
        valid_names = [e.name for e in enum_class]
        if value.upper() not in valid_names:
            return ValidationError(
                field=field_name,
                message=f"Field '{field_name}' value '{value}' not in {valid_names}",
                severity=ErrorSeverity.FATAL
            )
        return None

class CSVParser:
    def __init__(self, delimiter: str = ","):
        self.delimiter = delimiter

    def parse_line(self, line: str) -> List[str]:
        fields = []
        current_field = []
        in_quotes = False

        for char in line:
            if char == '"':
                in_quotes = not in_quotes
            elif char == self.delimiter and not in_quotes:
                fields.append("".join(current_field).strip())
                current_field = []
            else:
                current_field.append(char)

        fields.append("".join(current_field).strip())
        return fields

    def parse(self, data: str) -> Tuple[List[str], List[List[str]]]:
        lines = [line.strip() for line in data.strip().split("\n") if line.strip()]
        if not lines:
            return [], []

        headers = self.parse_line(lines[0])
        rows = [self.parse_line(line) for line in lines[1:]]
        return headers, rows

class DataIngestor:
    EMBEDDED_CSV = """id,name,value,quantity,status,category,tags
1,ItemAlpha,100.50,10,ACTIVE,ALPHA,"tag1;tag2"
2,ItemBeta,200.75,20,INACTIVE,BETA,"tag2;tag3"
3,ItemGamma,-50.00,5,PENDING,GAMMA,"tag1"
4,ItemDelta,1500.00,0,ACTIVE,DELTA,""
5,,150.25,15,ACTIVE,ALPHA,"tag3"
6,ItemEpsilon,75.00,-5,ARCHIVED,INVALID,"tag1;tag2"
7,ItemZeta,999.99,100,ACTIVE,BETA,"tag2"
8,ItemEta,50.00,25,UNKNOWN,GAMMA,"tag1;tag3"
9,ItemTheta,300.00,30,ACTIVE,ALPHA,""
10,ItemIota,450.50,45,PENDING,DELTA,"tag2;tag3;tag4"
"""

    def __init__(self):
        self.parser = CSVParser()
        self.validator = FieldValidator()

    def ingest(self) -> Result[ValidationResult, ProcessingError]:
        try:
            headers, rows = self.parser.parse(self.EMBEDDED_CSV)
            return self._process_rows(headers, rows)
        except Exception as e:
            return Result.err(ProcessingError(
                code="PARSE_ERROR",
                message=f"Failed to parse CSV: {str(e)}",
                severity=ErrorSeverity.FATAL
            ))

    def _process_rows(
        self,
        headers: List[str],
        rows: List[List[str]]
    ) -> Result[ValidationResult, ProcessingError]:
        valid_records = []
        errors = []

        for row_idx, row in enumerate(rows):
            record_result = self._parse_record(headers, row, row_idx)
            if record_result.is_ok:
                validation_errors = self._validate_record(record_result.value, row_idx)
                fatal_errors = [e for e in validation_errors if e.severity == ErrorSeverity.FATAL]

                if fatal_errors:
                    errors.extend(validation_errors)
                else:
                    valid_records.append(record_result.value)
                    errors.extend([e for e in validation_errors if e.severity == ErrorSeverity.RECOVERABLE])
            else:
                errors.append(ValidationError(
                    field="row",
                    message=record_result.error.message,
                    severity=ErrorSeverity.FATAL,
                    row_index=row_idx
                ))

        return Result.ok(ValidationResult(
            valid_records=valid_records,
            invalid_count=len(rows) - len(valid_records),
            errors=errors
        ))

    def _parse_record(
        self,
        headers: List[str],
        row: List[str],
        row_idx: int
    ) -> Result[Record, ProcessingError]:
        if len(row) != len(headers):
            return Result.err(ProcessingError(
                code="COLUMN_MISMATCH",
                message=f"Row {row_idx} has {len(row)} columns, expected {len(headers)}",
                severity=ErrorSeverity.FATAL
            ))

        data = dict(zip(headers, row))

        try:
            record_id = int(data.get("id", "0"))
            name = data.get("name", "")
            value = float(data.get("value", "0"))
            quantity = int(data.get("quantity", "0"))
            status_str = data.get("status", "ACTIVE").upper()
            category_str = data.get("category", "ALPHA").upper()
            tags_str = data.get("tags", "")

            status = Status[status_str] if status_str in Status.__members__ else Status.ACTIVE
            category = Category[category_str] if category_str in Category.__members__ else Category.ALPHA
            tags = [t.strip() for t in tags_str.split(";") if t.strip()]

            return Result.ok(Record(
                id=record_id,
                name=name,
                value=value,
                quantity=quantity,
                status=status,
                category=category,
                tags=tags,
                metadata={"row_index": row_idx}
            ))
        except (ValueError, KeyError) as e:
            return Result.err(ProcessingError(
                code="PARSE_FIELD_ERROR",
                message=f"Failed to parse fields in row {row_idx}: {str(e)}",
                severity=ErrorSeverity.FATAL
            ))

    def _validate_record(self, record: Record, row_idx: int) -> List[ValidationError]:
        errors = []

        name_error = self.validator.validate_required(record.name, "name")
        if name_error:
            name_error.row_index = row_idx
            errors.append(name_error)

        value_error = self.validator.validate_numeric_range(
            record.value, "value", min_val=0.0, max_val=10000.0
        )
        if value_error:
            value_error.row_index = row_idx
            errors.append(value_error)

        quantity_error = self.validator.validate_numeric_range(
            record.quantity, "quantity", min_val=0, max_val=1000
        )
        if quantity_error:
            quantity_error.row_index = row_idx
            errors.append(quantity_error)

        return errors

class StatefulAggregator:
    def __init__(self):
        self._groups: Dict[str, List[Record]] = {}
        self._running_totals: Dict[str, Tuple[float, int]] = {}

    def add_record(self, record: Record, group_key: str) -> None:
        if group_key not in self._groups:
            self._groups[group_key] = []
            self._running_totals[group_key] = (0.0, 0)

        self._groups[group_key].append(record)
        current_value, current_qty = self._running_totals[group_key]
        self._running_totals[group_key] = (
            current_value + record.value,
            current_qty + record.quantity
        )

    def compute_stats(self, records: List[Record]) -> AggregationStats:
        if not records:
            return AggregationStats(
                count=0,
                min_value=0.0,
                max_value=0.0,
                sum_value=0.0,
                mean_value=0.0,
                min_quantity=0,
                max_quantity=0,
                sum_quantity=0
            )

        values = [r.value for r in records]
        quantities = [r.quantity for r in records]

        return AggregationStats(
            count=len(records),
            min_value=min(values),
            max_value=max(values),
            sum_value=sum(values),
            mean_value=sum(values) / len(values),
            min_quantity=min(quantities),
            max_quantity=max(quantities),
            sum_quantity=sum(quantities)
        )

    def aggregate_by_category(self, records: List[Record]) -> AggregationReport:
        self._groups.clear()
        self._running_totals.clear()

        for record in records:
            self.add_record(record, record.category.name)

        groups = {}
        for key, group_records in self._groups.items():
            groups[key] = GroupSummary(
                key=key,
                stats=self.compute_stats(group_records),
                records=group_records
            )

        return AggregationReport(
            groups=groups,
            total_records=len(records),
            total_groups=len(groups),
            global_stats=self.compute_stats(records)
        )

    def get_running_total(self, group_key: str) -> Tuple[float, int]:
        return self._running_totals.get(group_key, (0.0, 0))

@dataclass
class RuleCondition:
    field: str
    operator: str
    value: Any

@dataclass
class RuleAction:
    action_type: str
    params: Dict[str, Any]

@dataclass
class Rule:
    name: str
    conditions: List[RuleCondition]
    actions: List[RuleAction]
    priority: int = 0

class DeclarativeRuleEngine:
    RULES_DATA: List[Dict[str, Any]] = [
        {
            "name": "high_value_item",
            "conditions": [
                {"field": "value", "operator": ">=", "value": 500.0}
            ],
            "actions": [
                {"action_type": "add_label", "params": {"label": "HIGH_VALUE"}},
                {"action_type": "add_score", "params": {"score": 10.0}}
            ],
            "priority": 1
        },
        {
            "name": "low_quantity_alert",
            "conditions": [
                {"field": "quantity", "operator": "<", "value": 10}
            ],
            "actions": [
                {"action_type": "add_label", "params": {"label": "LOW_STOCK"}},
                {"action_type": "add_score", "params": {"score": -5.0}}
            ],
            "priority": 2
        },
        {
            "name": "active_alpha_bonus",
            "conditions": [
                {"field": "status", "operator": "==", "value": "ACTIVE"},
                {"field": "category", "operator": "==", "value": "ALPHA"}
            ],
            "actions": [
                {"action_type": "add_label", "params": {"label": "PRIORITY"}},
                {"action_type": "add_score", "params": {"score": 15.0}}
            ],
            "priority": 0
        },
        {
            "name": "tagged_item",
            "conditions": [
                {"field": "tags", "operator": "contains", "value": "tag1"}
            ],
            "actions": [
                {"action_type": "add_label", "params": {"label": "TAGGED"}}
            ],
            "priority": 3
        }
    ]

    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self) -> List[Rule]:
        rules = []
        for rule_data in self.RULES_DATA:
            conditions = [
                RuleCondition(**cond) for cond in rule_data["conditions"]
            ]
            actions = [
                RuleAction(**action) for action in rule_data["actions"]
            ]
            rules.append(Rule(
                name=rule_data["name"],
                conditions=conditions,
                actions=actions,
                priority=rule_data.get("priority", 0)
            ))
        return sorted(rules, key=lambda r: r.priority)

    def _get_field_value(self, record: Record, field: str) -> Any:
        if field == "status":
            return record.status.name
        elif field == "category":
            return record.category.name
        elif hasattr(record, field):
            return getattr(record, field)
        return None

    def _evaluate_condition(self, record: Record, condition: RuleCondition) -> bool:
        field_value = self._get_field_value(record, condition.field)

        if field_value is None:
            return False

        op = condition.operator
        target = condition.value

        if op == "==":
            return field_value == target
        elif op == "!=":
            return field_value != target
        elif op == ">":
            return field_value > target
        elif op == ">=":
            return field_value >= target
        elif op == "<":
            return field_value < target
        elif op == "<=":
            return field_value <= target
        elif op == "contains":
            if isinstance(field_value, list):
                return target in field_value
            return target in str(field_value)
        elif op == "in":
            return field_value in target

        return False

    def _apply_action(
        self,
        summary: GroupSummary,
        action: RuleAction
    ) -> GroupSummary:
        if action.action_type == "add_label":
            label = action.params.get("label", "")
            if label and label not in summary.labels:
                summary.labels.append(label)
        elif action.action_type == "add_score":
            score = action.params.get("score", 0.0)
            summary.score += score
        elif action.action_type == "set_score":
            summary.score = action.params.get("score", 0.0)

        return summary

    def evaluate_record(self, record: Record) -> Tuple[List[str], float]:
        labels = []
        score = 0.0

        for rule in self.rules:
            all_match = all(
                self._evaluate_condition(record, cond)
                for cond in rule.conditions
            )

            if all_match:
                for action in rule.actions:
                    if action.action_type == "add_label":
                        label = action.params.get("label", "")
                        if label and label not in labels:
                            labels.append(label)
                    elif action.action_type == "add_score":
                        score += action.params.get("score", 0.0)

        return labels, score

    def apply_rules_to_report(self, report: AggregationReport) -> AggregationReport:
        for key, summary in report.groups.items():
            for record in summary.records:
                labels, score = self.evaluate_record(record)
                for label in labels:
                    if label not in summary.labels:
                        summary.labels.append(label)
                summary.score += score

        return report

class ErrorPropagator:
    def __init__(self):
        self.error_log: List[ProcessingError] = []

    def wrap_operation(
        self,
        operation: Callable[[], T],
        context: str
    ) -> Result[T, ProcessingError]:
        try:
            result = operation()
            return Result.ok(result)
        except Exception as e:
            error = ProcessingError(
                code="OPERATION_FAILED",
                message=f"Operation failed in {context}: {str(e)}",
                severity=ErrorSeverity.RECOVERABLE
            )
            self.error_log.append(error)
            return Result.err(error)

    def propagate(
        self,
        result: Result[T, ProcessingError],
        new_context: str
    ) -> Result[T, ProcessingError]:
        if result.is_err:
            chained = result.error.chain(
                f"Error propagated through {new_context}",
                "PROPAGATED_ERROR"
            )
            self.error_log.append(chained)
            return Result.err(chained)
        return result

    def recover_or_fail(
        self,
        result: Result[T, ProcessingError],
        recovery: Callable[[], T]
    ) -> Result[T, ProcessingError]:
        if result.is_err:
            if result.error.severity == ErrorSeverity.RECOVERABLE:
                try:
                    recovered = recovery()
                    return Result.ok(recovered)
                except Exception as e:
                    fatal = ProcessingError(
                        code="RECOVERY_FAILED",
                        message=f"Recovery failed: {str(e)}",
                        severity=ErrorSeverity.FATAL,
                        cause=result.error
                    )
                    return Result.err(fatal)
            return result
        return result

class JSONSerializer:
    def __init__(self, indent: int = 2):
        self.indent = indent

    def serialize(self, obj: Any) -> str:
        return self._to_json(obj, 0)

    def _to_json(self, obj: Any, depth: int) -> str:
        indent_str = " " * (self.indent * depth)
        next_indent = " " * (self.indent * (depth + 1))

        if obj is None:
            return "null"
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif isinstance(obj, (int, float)):
            if math.isnan(obj) or math.isinf(obj):
                return "null"
            return str(obj)
        elif isinstance(obj, str):
            escaped = obj.replace("\\", "\\\\").replace('"', '\\"')
            escaped = escaped.replace("\n", "\\n").replace("\r", "\\r")
            escaped = escaped.replace("\t", "\\t")
            return f'"{escaped}"'
        elif isinstance(obj, Enum):
            return f'"{obj.name}"'
        elif isinstance(obj, list):
            if not obj:
                return "[]"
            items = [self._to_json(item, depth + 1) for item in obj]
            return "[\n" + next_indent + (",\n" + next_indent).join(items) + "\n" + indent_str + "]"
        elif isinstance(obj, dict):
            if not obj:
                return "{}"
            pairs = []
            for k, v in obj.items():
                key_str = self._to_json(str(k), depth + 1)
                val_str = self._to_json(v, depth + 1)
                pairs.append(f"{key_str}: {val_str}")
            return "{\n" + next_indent + (",\n" + next_indent).join(pairs) + "\n" + indent_str + "}"
        elif hasattr(obj, "__dataclass_fields__"):
            return self._to_json(self._dataclass_to_dict(obj), depth)
        else:
            return f'"{str(obj)}"'

    def _dataclass_to_dict(self, obj: Any) -> Dict[str, Any]:
        result = {}
        for field_name in obj.__dataclass_fields__:
            value = getattr(obj, field_name)
            if hasattr(value, "__dataclass_fields__"):
                result[field_name] = self._dataclass_to_dict(value)
            elif isinstance(value, dict):
                result[field_name] = {
                    k: self._dataclass_to_dict(v) if hasattr(v, "__dataclass_fields__") else v
                    for k, v in value.items()
                }
            elif isinstance(value, list):
                result[field_name] = [
                    self._dataclass_to_dict(item) if hasattr(item, "__dataclass_fields__") else item
                    for item in value
                ]
            else:
                result[field_name] = value
        return result

class JSONDeserializer:
    def __init__(self):
        self.pos = 0
        self.text = ""

    def deserialize(self, json_str: str) -> Any:
        self.pos = 0
        self.text = json_str
        self._skip_whitespace()
        return self._parse_value()

    def _skip_whitespace(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] in " \t\n\r":
            self.pos += 1

    def _parse_value(self) -> Any:
        self._skip_whitespace()
        if self.pos >= len(self.text):
            return None

        char = self.text[self.pos]

        if char == '"':
            return self._parse_string()
        elif char == '{':
            return self._parse_object()
        elif char == '[':
            return self._parse_array()
        elif char == 't':
            return self._parse_literal("true", True)
        elif char == 'f':
            return self._parse_literal("false", False)
        elif char == 'n':
            return self._parse_literal("null", None)
        elif char == '-' or char.isdigit():
            return self._parse_number()
        else:
            raise ValueError(f"Unexpected character at position {self.pos}: {char}")

    def _parse_string(self) -> str:
        self.pos += 1
        result = []
        while self.pos < len(self.text):
            char = self.text[self.pos]
            if char == '"':
                self.pos += 1
                return "".join(result)
            elif char == '\\':
                self.pos += 1
                if self.pos < len(self.text):
                    escape_char = self.text[self.pos]
                    if escape_char == 'n':
                        result.append('\n')
                    elif escape_char == 'r':
                        result.append('\r')
                    elif escape_char == 't':
                        result.append('\t')
                    elif escape_char == '"':
                        result.append('"')
                    elif escape_char == '\\':
                        result.append('\\')
                    else:
                        result.append(escape_char)
            else:
                result.append(char)
            self.pos += 1
        raise ValueError("Unterminated string")

    def _parse_object(self) -> Dict[str, Any]:
        self.pos += 1
        result = {}
        self._skip_whitespace()

        if self.pos < len(self.text) and self.text[self.pos] == '}':
            self.pos += 1
            return result

        while self.pos < len(self.text):
            self._skip_whitespace()
            key = self._parse_string()
            self._skip_whitespace()

            if self.pos < len(self.text) and self.text[self.pos] == ':':
                self.pos += 1

            self._skip_whitespace()
            value = self._parse_value()
            result[key] = value

            self._skip_whitespace()
            if self.pos < len(self.text):
                if self.text[self.pos] == '}':
                    self.pos += 1
                    return result
                elif self.text[self.pos] == ',':
                    self.pos += 1

        return result

    def _parse_array(self) -> List[Any]:
        self.pos += 1
        result = []
        self._skip_whitespace()

        if self.pos < len(self.text) and self.text[self.pos] == ']':
            self.pos += 1
            return result

        while self.pos < len(self.text):
            self._skip_whitespace()
            value = self._parse_value()
            result.append(value)

            self._skip_whitespace()
            if self.pos < len(self.text):
                if self.text[self.pos] == ']':
                    self.pos += 1
                    return result
                elif self.text[self.pos] == ',':
                    self.pos += 1

        return result

    def _parse_number(self) -> Union[int, float]:
        start = self.pos
        if self.text[self.pos] == '-':
            self.pos += 1

        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            self.pos += 1

        is_float = False
        if self.pos < len(self.text) and self.text[self.pos] == '.':
            is_float = True
            self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

        if self.pos < len(self.text) and self.text[self.pos] in 'eE':
            is_float = True
            self.pos += 1
            if self.pos < len(self.text) and self.text[self.pos] in '+-':
                self.pos += 1
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1

        num_str = self.text[start:self.pos]
        return float(num_str) if is_float else int(num_str)

    def _parse_literal(self, literal: str, value: Any) -> Any:
        if self.text[self.pos:self.pos + len(literal)] == literal:
            self.pos += len(literal)
            return value
        raise ValueError(f"Expected {literal} at position {self.pos}")

@dataclass
class TestCase:
    name: str
    test_func: Callable[[], bool]
    expected: Any = None

class TestHarness:
    def __init__(self):
        self.tests: List[TestCase] = []
        self.passed = 0
        self.failed = 0
        self.results: List[Tuple[str, bool, str]] = []

    def add_test(self, name: str, test_func: Callable[[], bool]) -> None:
        self.tests.append(TestCase(name=name, test_func=test_func))

    def assert_equal(self, actual: Any, expected: Any, message: str = "") -> bool:
        if actual == expected:
            return True
        raise AssertionError(f"{message}: Expected {expected}, got {actual}")

    def assert_true(self, condition: bool, message: str = "") -> bool:
        if condition:
            return True
        raise AssertionError(f"{message}: Expected True, got False")

    def assert_not_none(self, value: Any, message: str = "") -> bool:
        if value is not None:
            return True
        raise AssertionError(f"{message}: Expected non-None value")

    def run(self) -> bool:
        print("=" * 60)
        print("CTS BENCHMARK TEST HARNESS")
        print("=" * 60)

        for test in self.tests:
            try:
                result = test.test_func()
                if result:
                    self.passed += 1
                    self.results.append((test.name, True, "PASS"))
                    print(f"[PASS] {test.name}")
                else:
                    self.failed += 1
                    self.results.append((test.name, False, "FAIL: Returned False"))
                    print(f"[FAIL] {test.name}: Returned False")
            except AssertionError as e:
                self.failed += 1
                self.results.append((test.name, False, f"FAIL: {str(e)}"))
                print(f"[FAIL] {test.name}: {str(e)}")
            except Exception as e:
                self.failed += 1
                self.results.append((test.name, False, f"ERROR: {str(e)}"))
                print(f"[ERROR] {test.name}: {str(e)}")

        print("=" * 60)
        print(f"Results: {self.passed} passed, {self.failed} failed")
        print("=" * 60)

        return self.failed == 0

def run_cts_benchmark() -> bool:
    harness = TestHarness()

    def test_data_ingest():
        ingestor = DataIngestor()
        result = ingestor.ingest()
        harness.assert_true(result.is_ok, "Ingest should succeed")
        validation = result.unwrap()
        harness.assert_true(len(validation.valid_records) > 0, "Should have valid records")
        harness.assert_true(validation.invalid_count >= 0, "Invalid count should be non-negative")
        return True

    def test_validation_errors():
        ingestor = DataIngestor()
        result = ingestor.ingest()
        validation = result.unwrap()
        harness.assert_true(len(validation.errors) > 0, "Should have validation errors")
        return True

    def test_aggregation():
        ingestor = DataIngestor()
        result = ingestor.ingest()
        records = result.unwrap().valid_records

        aggregator = StatefulAggregator()
        report = aggregator.aggregate_by_category(records)

        harness.assert_true(report.total_records > 0, "Should have records")
        harness.assert_true(report.total_groups > 0, "Should have groups")
        harness.assert_true(report.global_stats.count == report.total_records, "Stats count should match")
        return True

    def test_running_totals():
        aggregator = StatefulAggregator()
        record1 = Record(1, "Test1", 100.0, 10, Status.ACTIVE, Category.ALPHA)
        record2 = Record(2, "Test2", 200.0, 20, Status.ACTIVE, Category.ALPHA)

        aggregator.add_record(record1, "ALPHA")
        aggregator.add_record(record2, "ALPHA")

        total_value, total_qty = aggregator.get_running_total("ALPHA")
        harness.assert_equal(total_value, 300.0, "Value total")
        harness.assert_equal(total_qty, 30, "Quantity total")
        return True

    def test_rule_engine():
        engine = DeclarativeRuleEngine()

        high_value_record = Record(1, "Expensive", 1000.0, 50, Status.ACTIVE, Category.BETA)
        labels, score = engine.evaluate_record(high_value_record)

        harness.assert_true("HIGH_VALUE" in labels, "Should have HIGH_VALUE label")
        harness.assert_true(score >= 10.0, "Should have positive score")
        return True

    def test_rule_engine_multiple_conditions():
        engine = DeclarativeRuleEngine()

        alpha_active = Record(1, "PriorityItem", 100.0, 50, Status.ACTIVE, Category.ALPHA, ["tag1"])
        labels, score = engine.evaluate_record(alpha_active)

        harness.assert_true("PRIORITY" in labels, "Should have PRIORITY label")
        harness.assert_true("TAGGED" in labels, "Should have TAGGED label")
        return True

    def test_error_propagation():
        propagator = ErrorPropagator()

        def failing_operation():
            raise ValueError("Simulated failure")

        result = propagator.wrap_operation(failing_operation, "test_context")
        harness.assert_true(result.is_err, "Should be error")

        propagated = propagator.propagate(result, "outer_context")
        harness.assert_true(propagated.is_err, "Should still be error")
        harness.assert_not_none(propagated.error.cause, "Should have cause")
        return True

    def test_error_recovery():
        propagator = ErrorPropagator()

        error = ProcessingError(
            code="TEST_ERROR",
            message="Test error",
            severity=ErrorSeverity.RECOVERABLE
        )
        error_result: Result[int, ProcessingError] = Result.err(error)

        recovered = propagator.recover_or_fail(error_result, lambda: 42)
        harness.assert_true(recovered.is_ok, "Should recover")
        harness.assert_equal(recovered.unwrap(), 42, "Recovered value")
        return True

    def test_serialization():
        serializer = JSONSerializer()

        test_data = {
            "name": "test",
            "value": 123.45,
            "items": [1, 2, 3],
            "nested": {"a": 1, "b": 2}
        }

        json_str = serializer.serialize(test_data)
        harness.assert_true('"name"' in json_str, "Should contain name key")
        harness.assert_true("123.45" in json_str, "Should contain value")
        return True

    def test_deserialization():
        deserializer = JSONDeserializer()

        json_str = '{"name": "test", "value": 42, "list": [1, 2, 3]}'
        result = deserializer.deserialize(json_str)

        harness.assert_equal(result["name"], "test", "Name field")
        harness.assert_equal(result["value"], 42, "Value field")
        harness.assert_equal(result["list"], [1, 2, 3], "List field")
        return True

    def test_roundtrip_serialization():
        serializer = JSONSerializer()
        deserializer = JSONDeserializer()

        original = {
            "id": 1,
            "name": "RoundTrip Test",
            "values": [10.5, 20.5, 30.5],
            "nested": {"x": 100, "y": 200}
        }

        json_str = serializer.serialize(original)
        restored = deserializer.deserialize(json_str)

        harness.assert_equal(restored["id"], original["id"], "ID match")
        harness.assert_equal(restored["name"], original["name"], "Name match")
        harness.assert_equal(restored["values"], original["values"], "Values match")
        return True

    def test_full_pipeline():
        ingestor = DataIngestor()
        aggregator = StatefulAggregator()
        rule_engine = DeclarativeRuleEngine()
        serializer = JSONSerializer()
        deserializer = JSONDeserializer()

        ingest_result = ingestor.ingest()
        harness.assert_true(ingest_result.is_ok, "Ingest OK")

        records = ingest_result.unwrap().valid_records
        report = aggregator.aggregate_by_category(records)
        report = rule_engine.apply_rules_to_report(report)

        summary = {
            "total_records": report.total_records,
            "total_groups": report.total_groups,
            "groups": list(report.groups.keys())
        }

        json_str = serializer.serialize(summary)
        restored = deserializer.deserialize(json_str)

        harness.assert_equal(restored["total_records"], report.total_records, "Records match")
        return True

    harness.add_test("Task1: Data Ingest", test_data_ingest)
    harness.add_test("Task1: Validation Errors", test_validation_errors)
    harness.add_test("Task2: Aggregation", test_aggregation)
    harness.add_test("Task2: Running Totals", test_running_totals)
    harness.add_test("Task3: Rule Engine Basic", test_rule_engine)
    harness.add_test("Task3: Rule Engine Multiple Conditions", test_rule_engine_multiple_conditions)
    harness.add_test("Task4: Error Propagation", test_error_propagation)
    harness.add_test("Task4: Error Recovery", test_error_recovery)
    harness.add_test("Task5: Serialization", test_serialization)
    harness.add_test("Task5: Deserialization", test_deserialization)
    harness.add_test("Task5: Roundtrip", test_roundtrip_serialization)
    harness.add_test("Task6: Full Pipeline", test_full_pipeline)

    return harness.run()

if __name__ == "__main__":
    success = run_cts_benchmark()
    exit(0 if success else 1)
