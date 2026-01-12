# Tokenizers Directory

This directory contains trained SentencePiece models for the LTC benchmark.

## Models (generated locally)

The following models should be trained locally:

- `sp_unigram_256k.model` - Unigram Language Model tokenizer
- `sp_bpe_256k.model` - BPE tokenizer

## Training

Generate models with:

```bash
python train_sentencepiece.py --vocab-size 256000
```

This will:
1. Collect all benchmark source files into a corpus
2. Train both Unigram and BPE models
3. Save models to this directory

## Requirements

```bash
pip install sentencepiece --break-system-packages
```

## Note

Model files (`.model`, `.vocab`) are gitignored because:
- They are large binary files
- They should be generated from the benchmark corpus
- Different vocab sizes may be needed for experiments

Always regenerate models after adding new languages to the benchmark.
