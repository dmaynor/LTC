#!/usr/bin/env python3
"""
Multi-tokenizer benchmark runner for LTC.

Supports:
- tiktoken encodings (cl100k_base, o200k_base, p50k_base)
- SentencePiece models (BPE, Unigram)

Usage:
    python benchmark_multi.py benchmark/ --tokenizers cl100k_base,sp_unigram
    python benchmark_multi.py benchmark/ --all

Requirements:
    pip install tiktoken sentencepiece --break-system-packages
"""

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Protocol, Optional


class Tokenizer(Protocol):
    """Protocol for tokenizer implementations."""
    name: str
    tokenizer_class: str

    def count_tokens(self, text: str) -> int:
        ...


@dataclass
class TiktokenTokenizer:
    """Wrapper for tiktoken encodings."""
    name: str
    tokenizer_class: str = "open"
    _encoding: Optional[object] = None

    def __post_init__(self):
        import tiktoken
        self._encoding = tiktoken.get_encoding(self.name)

    def count_tokens(self, text: str) -> int:
        return len(self._encoding.encode(text))


@dataclass
class SentencePieceTokenizer:
    """Wrapper for SentencePiece models."""
    name: str
    model_path: str
    tokenizer_class: str = "open-proxy"
    _sp: Optional[object] = None

    def __post_init__(self):
        import sentencepiece as spm
        self._sp = spm.SentencePieceProcessor(model_file=self.model_path)

    def count_tokens(self, text: str) -> int:
        return len(self._sp.encode(text))


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


def analyze_file(filepath: Path, language: str, task: str, tokenizer: Tokenizer) -> TokenMetrics:
    """Analyze a code file with a specific tokenizer."""
    code = filepath.read_text(encoding='utf-8', errors='replace')

    char_count = len(code)
    token_count = tokenizer.count_tokens(code)
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


def analyze_benchmark(base_path: Path, tokenizer: Tokenizer) -> list[TokenMetrics]:
    """Analyze all code files with a specific tokenizer."""
    results = []

    for lang_dir in sorted(base_path.iterdir()):
        if not lang_dir.is_dir():
            continue
        language = lang_dir.name

        for code_file in sorted(lang_dir.iterdir()):
            if code_file.is_file():
                task = code_file.stem
                metrics = analyze_file(code_file, language, task, tokenizer)
                results.append(metrics)

    return results


def generate_summary(results: list[TokenMetrics]) -> dict:
    """Generate summary statistics by language."""
    lang_totals = {}

    for m in results:
        if m.language not in lang_totals:
            lang_totals[m.language] = {
                'tokens': 0, 'chars': 0, 'lines': 0, 'tasks': 0
            }
        lang_totals[m.language]['tokens'] += m.tokens
        lang_totals[m.language]['chars'] += m.characters
        lang_totals[m.language]['lines'] += m.lines
        lang_totals[m.language]['tasks'] += 1

    return lang_totals


def get_tokenizer(name: str, tokenizers_dir: Path) -> Tokenizer:
    """Get a tokenizer by name."""
    # tiktoken encodings
    tiktoken_encodings = ['cl100k_base', 'o200k_base', 'p50k_base', 'r50k_base']

    if name in tiktoken_encodings:
        return TiktokenTokenizer(name=name)

    # SentencePiece models
    sp_models = {
        'sp_unigram': 'sp_unigram_256k.model',
        'sp_bpe': 'sp_bpe_256k.model',
        'sp_unigram_256k': 'sp_unigram_256k.model',
        'sp_bpe_256k': 'sp_bpe_256k.model',
    }

    if name in sp_models:
        model_path = tokenizers_dir / sp_models[name]
        if not model_path.exists():
            raise FileNotFoundError(
                f"SentencePiece model not found: {model_path}\n"
                f"Train it first with: python train_sentencepiece.py"
            )
        algorithm = "unigram" if "unigram" in name else "bpe"
        return SentencePieceTokenizer(
            name=f"sentencepiece-{algorithm}",
            model_path=str(model_path)
        )

    # Custom model path
    if name.endswith('.model'):
        model_path = Path(name)
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        return SentencePieceTokenizer(name=model_path.stem, model_path=str(model_path))

    raise ValueError(f"Unknown tokenizer: {name}")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-tokenizer benchmark runner for LTC"
    )
    parser.add_argument(
        "benchmark_dir",
        help="Path to benchmark directory"
    )
    parser.add_argument(
        "--tokenizers", "-t",
        default="cl100k_base",
        help="Comma-separated list of tokenizers (default: cl100k_base)"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Run all available tokenizers"
    )
    parser.add_argument(
        "--tokenizers-dir",
        default="tokenizers",
        help="Directory containing SentencePiece models (default: tokenizers)"
    )
    parser.add_argument(
        "--output", "-o",
        default="benchmark_multi_results.json",
        help="Output JSON file (default: benchmark_multi_results.json)"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Generate comparison table"
    )
    args = parser.parse_args()

    base_path = Path(args.benchmark_dir)
    tokenizers_dir = Path(args.tokenizers_dir)

    if not base_path.exists():
        print(f"Error: Benchmark directory '{base_path}' not found")
        return 1

    # Determine tokenizers to run
    if args.all:
        tokenizer_names = ['cl100k_base', 'o200k_base']
        # Add SentencePiece if models exist
        if (tokenizers_dir / 'sp_unigram_256k.model').exists():
            tokenizer_names.append('sp_unigram')
        if (tokenizers_dir / 'sp_bpe_256k.model').exists():
            tokenizer_names.append('sp_bpe')
    else:
        tokenizer_names = [t.strip() for t in args.tokenizers.split(',')]

    all_results = {}

    for tokenizer_name in tokenizer_names:
        print(f"\n{'=' * 60}")
        print(f"Running tokenizer: {tokenizer_name}")
        print('=' * 60)

        try:
            tokenizer = get_tokenizer(tokenizer_name, tokenizers_dir)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            continue

        results = analyze_benchmark(base_path, tokenizer)
        summary = generate_summary(results)

        all_results[tokenizer_name] = {
            'tokenizer': tokenizer.name,
            'tokenizer_class': tokenizer.tokenizer_class,
            'results': [asdict(r) for r in results],
            'summary': summary
        }

        # Print summary table
        sorted_langs = sorted(summary.items(), key=lambda x: x[1]['tokens'])
        print(f"\n{'Language':<15} {'Tokens':>10} {'Tasks':>6}")
        print("-" * 35)
        for lang, data in sorted_langs[:10]:
            print(f"{lang:<15} {data['tokens']:>10} {data['tasks']:>6}")
        if len(sorted_langs) > 10:
            print(f"... and {len(sorted_langs) - 10} more languages")

    # Save results
    output_path = Path(args.output)
    output_path.write_text(json.dumps(all_results, indent=2))
    print(f"\nResults saved to: {output_path}")

    # Generate comparison table if requested
    if args.compare and len(all_results) > 1:
        print("\n" + "=" * 80)
        print("TOKENIZER COMPARISON")
        print("=" * 80)

        # Get all languages
        all_langs = set()
        for data in all_results.values():
            all_langs.update(data['summary'].keys())

        # Header
        header = f"{'Language':<15}"
        for tok_name in all_results.keys():
            header += f" {tok_name:>12}"
        print(header)
        print("-" * len(header))

        # Rows
        for lang in sorted(all_langs):
            row = f"{lang:<15}"
            for tok_name, data in all_results.items():
                tokens = data['summary'].get(lang, {}).get('tokens', '-')
                if isinstance(tokens, int):
                    row += f" {tokens:>12}"
                else:
                    row += f" {tokens:>12}"
            print(row)

    return 0


if __name__ == "__main__":
    exit(main())
