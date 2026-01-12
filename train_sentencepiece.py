#!/usr/bin/env python3
"""
Train SentencePiece tokenizers on the LTC benchmark corpus.

This script trains both BPE and Unigram models for comparative analysis.
These are open proxy models, not vendor tokenizer replicas.

Usage:
    python train_sentencepiece.py [--vocab-size 256000] [--benchmark-dir benchmark]

Requirements:
    pip install sentencepiece --break-system-packages
"""

import argparse
import subprocess
import tempfile
from pathlib import Path


def collect_corpus(benchmark_dir: Path) -> str:
    """Collect all benchmark source files into a single corpus."""
    corpus_parts = []

    for lang_dir in sorted(benchmark_dir.iterdir()):
        if not lang_dir.is_dir():
            continue

        for code_file in sorted(lang_dir.iterdir()):
            if code_file.is_file():
                try:
                    content = code_file.read_text(encoding='utf-8', errors='replace')
                    corpus_parts.append(content)
                except Exception as e:
                    print(f"Warning: Could not read {code_file}: {e}")

    return "\n".join(corpus_parts)


def train_model(corpus_file: str, model_prefix: str, model_type: str, vocab_size: int):
    """Train a SentencePiece model."""
    cmd = [
        "spm_train",
        f"--input={corpus_file}",
        f"--model_prefix={model_prefix}",
        f"--model_type={model_type}",
        f"--vocab_size={vocab_size}",
        "--character_coverage=1.0",
        "--normalization_rule_name=identity",  # No normalization for code
        "--add_dummy_prefix=false",  # Don't add space prefix
        "--remove_extra_whitespaces=false",  # Preserve whitespace
        "--split_by_unicode_script=false",  # Don't split on script boundaries
        "--split_by_whitespace=false",  # Allow cross-whitespace tokens
        "--byte_fallback=true",  # Handle any byte sequence
    ]

    print(f"Training {model_type} model: {model_prefix}")
    print(f"  Vocab size: {vocab_size}")
    print(f"  Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error training model:")
        print(result.stderr)
        return False

    print(f"  Success: {model_prefix}.model created")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Train SentencePiece tokenizers on LTC benchmark corpus"
    )
    parser.add_argument(
        "--vocab-size", type=int, default=256000,
        help="Vocabulary size (default: 256000)"
    )
    parser.add_argument(
        "--benchmark-dir", type=str, default="benchmark",
        help="Path to benchmark directory (default: benchmark)"
    )
    parser.add_argument(
        "--output-dir", type=str, default="tokenizers",
        help="Output directory for models (default: tokenizers)"
    )
    args = parser.parse_args()

    benchmark_dir = Path(args.benchmark_dir)
    output_dir = Path(args.output_dir)

    if not benchmark_dir.exists():
        print(f"Error: Benchmark directory '{benchmark_dir}' not found")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect corpus
    print("Collecting corpus from benchmark files...")
    corpus = collect_corpus(benchmark_dir)
    print(f"  Corpus size: {len(corpus)} characters")

    # Write corpus to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(corpus)
        corpus_file = f.name

    print(f"  Written to: {corpus_file}")

    # Train Unigram model
    unigram_prefix = output_dir / f"sp_unigram_{args.vocab_size // 1000}k"
    success_unigram = train_model(
        corpus_file, str(unigram_prefix), "unigram", args.vocab_size
    )

    # Train BPE model
    bpe_prefix = output_dir / f"sp_bpe_{args.vocab_size // 1000}k"
    success_bpe = train_model(
        corpus_file, str(bpe_prefix), "bpe", args.vocab_size
    )

    # Cleanup
    Path(corpus_file).unlink()

    # Summary
    print("\n" + "=" * 60)
    print("Training Summary")
    print("=" * 60)
    print(f"Unigram: {'SUCCESS' if success_unigram else 'FAILED'}")
    print(f"BPE:     {'SUCCESS' if success_bpe else 'FAILED'}")

    if success_unigram and success_bpe:
        print(f"\nModels saved to: {output_dir}/")
        print(f"  - sp_unigram_{args.vocab_size // 1000}k.model")
        print(f"  - sp_bpe_{args.vocab_size // 1000}k.model")
        return 0

    return 1


if __name__ == "__main__":
    exit(main())
