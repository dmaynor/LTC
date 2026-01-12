# LTC Tokenizer Taxonomy

This document defines the tokenizer classes used in the Language Token Count (LTC) benchmark and their characteristics.

## Tokenizer Classification

| Class | Description | Reproducible | Examples |
|-------|-------------|--------------|----------|
| `open` | Fully open tokenizers with published vocab/merges | Yes | OpenAI cl100k_base, o200k_base |
| `opaque-api` | Vendor tokenizers accessible only via API | No | Claude, Gemini, GPT-4 native |
| `open-proxy` | Open tokenizers trained on benchmark corpus | Yes | SentencePiece BPE/Unigram |

## Tokenizers in LTC

### 1. OpenAI cl100k_base (`open`)

- **Library**: tiktoken
- **Vocab Size**: ~100,000
- **Algorithm**: BPE (Byte-Pair Encoding)
- **Used By**: GPT-4, GPT-3.5-turbo, Claude (approximate)
- **Status**: Primary benchmark tokenizer

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode(text)
```

### 2. OpenAI o200k_base (`open`)

- **Library**: tiktoken
- **Vocab Size**: ~200,000
- **Algorithm**: BPE
- **Used By**: GPT-4o
- **Status**: Secondary comparison

```python
import tiktoken
enc = tiktoken.get_encoding("o200k_base")
tokens = enc.encode(text)
```

### 3. SentencePiece Unigram (`open-proxy`)

- **Library**: sentencepiece
- **Vocab Size**: 256,000 (configurable)
- **Algorithm**: Unigram Language Model
- **Trained On**: LTC benchmark corpus
- **Status**: Open proxy for research

**Characteristics**:
- Probabilistic tokenization
- Generally better compression
- More stable token boundaries
- Better handling of rare subwords

### 4. SentencePiece BPE (`open-proxy`)

- **Library**: sentencepiece
- **Vocab Size**: 256,000 (configurable)
- **Algorithm**: Byte-Pair Encoding
- **Trained On**: LTC benchmark corpus
- **Status**: Open proxy for research

**Characteristics**:
- Deterministic merge rules
- More predictable segmentation
- Similar to OpenAI tokenizers
- Good baseline for comparison

## Open Proxy Methodology

SentencePiece BPE and Unigram tokenizers are included as **open proxy models**. They are not intended to replicate any specific vendor tokenizer, but to study algorithmic differences under controlled conditions.

### Training Parameters

Both proxy tokenizers are trained with:
- **Corpus**: All LTC benchmark source files
- **Vocab Size**: 256,000 tokens
- **Character Coverage**: 1.0 (critical for code)
- **Normalization**: None (preserve exact input)

### What Open Proxies Provide

Running both BPE and Unigram over the same corpus enables measurement of:
- Token count differences between algorithms
- Boundary stability across languages
- Code vs natural-language tokenization bias
- Compression vs robustness tradeoffs

### What Open Proxies Do NOT Provide

Important guardrails:
- This does **not** recreate Gemini's tokenizer
- This does **not** recreate Claude's tokenizer
- This does **not** give native vendor counts

They give controlled, reproducible proxies for research purposes.

## Usage in LTC

### Primary Benchmark (cl100k_base)

```bash
python benchmark.py benchmark/
```

### Multi-Tokenizer Comparison

```bash
python benchmark_multi.py benchmark/ --tokenizers cl100k_base,sp_unigram,sp_bpe
```

### Training SentencePiece Models

```bash
# Generate corpus from benchmark files
find benchmark -type f -print0 | xargs -0 cat > corpus.txt

# Train Unigram model
spm_train \
  --input=corpus.txt \
  --model_prefix=tokenizers/sp_unigram_256k \
  --model_type=unigram \
  --vocab_size=256000 \
  --character_coverage=1.0

# Train BPE model
spm_train \
  --input=corpus.txt \
  --model_prefix=tokenizers/sp_bpe_256k \
  --model_type=bpe \
  --vocab_size=256000 \
  --character_coverage=1.0
```

## Result Schema

All tokenizer results should include provenance information:

```json
{
  "tokenizer": "sentencepiece-unigram",
  "tokenizer_class": "open-proxy",
  "vocab_size": 256000,
  "algorithm": "unigram",
  "results": [...]
}
```

## Comparative Analysis

When comparing tokenizers, consider:

| Metric | Description |
|--------|-------------|
| Token Count | Raw number of tokens |
| Chars/Token | Compression efficiency |
| Tokens/Line | Code density |
| Boundary Stability | Consistency across similar inputs |
| OOV Rate | Out-of-vocabulary token frequency |

## References

- [SentencePiece Paper](https://arxiv.org/abs/1808.06226)
- [BPE Algorithm](https://arxiv.org/abs/1508.07909)
- [tiktoken Documentation](https://github.com/openai/tiktoken)
- [Unigram Language Model](https://arxiv.org/abs/1804.10959)
