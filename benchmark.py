#!/usr/bin/env python3
"""
Token efficiency benchmark measurement tool.
Uses a simplified BPE-like tokenization approximation.
"""

import re
import json
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class TokenMetrics:
    """Metrics for a single code sample."""
    filepath: str
    language: str
    task: str
    characters: int
    tokens: int
    lines: int
    tokens_per_line: float
    chars_per_token: float


def count_tokens_simple(code: str) -> int:
    """
    Count tokens using a BPE-like approximation.
    This mimics how cl100k_base tokenizes code:
    - Common words stay as single tokens
    - Identifiers get split on camelCase/snake_case boundaries
    - Numbers, operators, and punctuation are individual tokens
    - Whitespace patterns (indentation) are tokenized
    """
    tokens = 0

    # Split into lines to handle indentation
    lines = code.split('\n')

    for line in lines:
        if not line:
            tokens += 1  # Newline token
            continue

        # Count leading whitespace as tokens (typically 1 token per 4 spaces)
        leading_ws = len(line) - len(line.lstrip())
        if leading_ws > 0:
            tokens += (leading_ws + 3) // 4  # Approximately 1 token per 4 spaces/1 tab

        content = line.strip()
        if not content:
            tokens += 1  # Newline
            continue

        # Tokenize the content
        # Pattern matches: words, numbers, multi-char operators, single chars
        pattern = r'''
            "[^"]*"           |  # Double-quoted strings
            '[^']*'           |  # Single-quoted strings
            \d+\.?\d*         |  # Numbers
            [a-zA-Z_]\w*      |  # Identifiers
            ==|!=|<=|>=|&&|\|\||  # Multi-char operators
            ->|=>|::|\.\.|    |  # More multi-char ops
            <<|>>|            |  # Bit shifts
            \+\+|--|          |  # Increment/decrement
            \+=|-=|\*=|/=     |  # Compound assignment
            .                     # Single characters
        '''

        matches = re.findall(pattern, content, re.VERBOSE)

        for match in matches:
            if not match or match.isspace():
                continue
            # Strings count as roughly 1 token per 4 chars
            if match.startswith('"') or match.startswith("'"):
                tokens += max(1, len(match) // 4)
            # Long identifiers get split
            elif re.match(r'^[a-zA-Z_]\w*$', match):
                # Split on camelCase and underscores
                parts = re.split(r'(?<=[a-z])(?=[A-Z])|_', match)
                # Each part becomes roughly 1 token, with common words staying whole
                for part in parts:
                    if part:
                        if len(part) <= 4:
                            tokens += 1
                        else:
                            tokens += (len(part) + 3) // 4
            # Numbers
            elif re.match(r'^\d+\.?\d*$', match):
                tokens += 1 if len(match) <= 4 else (len(match) + 2) // 3
            else:
                tokens += 1

        tokens += 1  # Newline token

    return max(1, tokens)


def analyze_file(filepath: Path, language: str, task: str) -> TokenMetrics:
    """Analyze a code file and return token metrics."""
    code = filepath.read_text(encoding='utf-8')

    char_count = len(code)
    token_count = count_tokens_simple(code)
    line_count = len(code.splitlines())

    return TokenMetrics(
        filepath=str(filepath),
        language=language,
        task=task,
        characters=char_count,
        tokens=token_count,
        lines=line_count,
        tokens_per_line=round(token_count / max(line_count, 1), 2),
        chars_per_token=round(char_count / max(token_count, 1), 2),
    )


def analyze_benchmark_directory(base_path: Path) -> list[TokenMetrics]:
    """
    Analyze all code files in benchmark directory structure.
    Expected structure: base_path/<language>/<task>.<ext>
    """
    results = []

    for lang_dir in sorted(base_path.iterdir()):
        if not lang_dir.is_dir():
            continue
        language = lang_dir.name

        for code_file in sorted(lang_dir.iterdir()):
            if code_file.is_file():
                task = code_file.stem
                metrics = analyze_file(code_file, language, task)
                results.append(metrics)

    return results


def generate_report(results: list[TokenMetrics]) -> str:
    """Generate markdown report from results."""
    # Aggregate by language
    lang_totals: dict[str, dict] = {}

    for m in results:
        if m.language not in lang_totals:
            lang_totals[m.language] = {
                'tokens': 0, 'chars': 0, 'lines': 0, 'tasks': 0
            }
        lang_totals[m.language]['tokens'] += m.tokens
        lang_totals[m.language]['chars'] += m.characters
        lang_totals[m.language]['lines'] += m.lines
        lang_totals[m.language]['tasks'] += 1

    # Sort by total tokens
    sorted_langs = sorted(
        lang_totals.items(),
        key=lambda x: x[1]['tokens']
    )

    lines = ["# Token Efficiency Benchmark Results\n"]
    lines.append("*Comparing token counts across 29 programming languages using BPE-style tokenization*\n")
    lines.append("## Summary Table\n")
    lines.append("| Rank | Language | Total Tokens | Chars/Token | Tokens/Line | Tasks |")
    lines.append("|------|----------|--------------|-------------|-------------|-------|")

    for rank, (lang, data) in enumerate(sorted_langs, 1):
        cpt = round(data['chars'] / max(data['tokens'], 1), 2)
        tpl = round(data['tokens'] / max(data['lines'], 1), 2)
        lines.append(
            f"| {rank} | {lang} | {data['tokens']} | {cpt} | {tpl} | {data['tasks']} |"
        )

    # Add detailed per-task breakdown
    lines.append("\n## Per-Task Breakdown\n")

    # Group by task
    task_data: dict[str, list[tuple[str, int]]] = {}
    for m in results:
        if m.task not in task_data:
            task_data[m.task] = []
        task_data[m.task].append((m.language, m.tokens))

    for task in sorted(task_data.keys()):
        lines.append(f"\n### {task}\n")
        lines.append("| Rank | Language | Tokens |")
        lines.append("|------|----------|--------|")
        sorted_task = sorted(task_data[task], key=lambda x: x[1])
        for rank, (lang, tokens) in enumerate(sorted_task, 1):
            lines.append(f"| {rank} | {lang} | {tokens} |")

    # Add analysis section
    lines.append("\n## Analysis\n")
    lines.append("### Most Token-Efficient Languages (Top 5)\n")
    for rank, (lang, data) in enumerate(sorted_langs[:5], 1):
        lines.append(f"{rank}. **{lang}** - {data['tokens']} total tokens across {data['tasks']} tasks")

    lines.append("\n### Least Token-Efficient Languages (Bottom 5)\n")
    for rank, (lang, data) in enumerate(reversed(sorted_langs[-5:]), 1):
        lines.append(f"{rank}. **{lang}** - {data['tokens']} total tokens across {data['tasks']} tasks")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <benchmark_directory>")
        sys.exit(1)

    base_path = Path(sys.argv[1])
    results = analyze_benchmark_directory(base_path)

    # Output JSON for further processing
    json_output = [asdict(r) for r in results]
    Path("benchmark_results.json").write_text(
        json.dumps(json_output, indent=2)
    )

    # Output markdown report
    report = generate_report(results)
    print(report)
    Path("benchmark_report.md").write_text(report)
