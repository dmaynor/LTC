# Token Efficiency Benchmark: Complete Report of All 30 TIOBE Languages

*Using cl100k_base tokenization (GPT-4/Claude) - January 2026*

## Executive Summary

This benchmark evaluates the token efficiency of the **TIOBE Top 30 programming languages** (January 2026) using the **cl100k_base tokenizer** (GPT-4/Claude). Token efficiency directly impacts LLM context window utilization, API costs, and code generation capabilities.

**Key Finding:** Kotlin is the most token-efficient general-purpose language (317 tokens), followed closely by Python (327) and Julia (353).

---

## Complete Language Rankings

### Overall Ranking (All 30 Languages)

| Rank | Language | TIOBE Rank | Total Tokens | Chars/Token | Tokens/Line | Tasks | Status |
|------|----------|------------|--------------|-------------|-------------|-------|--------|
| 1 | **SQL** | 8 | 41 | 3.49 | 5.86 | 2 | Limited (domain-specific) |
| 2 | **SAS** | 25 | 83 | 3.30 | 4.88 | 3 | Limited (domain-specific) |
| 3 | **Prolog** | 23 | 219 | 2.74 | 9.12 | 5 | Limited (declarative) |
| 4 | **Kotlin** | 20 | 317 | 3.46 | 7.73 | 8 | Full |
| 5 | **Python** | 1 | 327 | 3.61 | 7.11 | 8 | Full |
| 6 | **Julia** | 28 | 353 | 3.19 | 6.30 | 8 | Full |
| 7 | **Ruby** | 27 | 363 | 2.95 | 6.48 | 8 | Full |
| 8 | **R** | 10 | 391 | 3.31 | 7.52 | 8 | Full |
| 9 | **JavaScript** | 6 | 412 | 3.69 | 6.87 | 8 | Full |
| 10 | **C#** | 5 | 433 | 3.83 | 6.10 | 8 | Full |
| 11 | **MATLAB** | 14 | 437 | 3.49 | 6.33 | 8 | Full |
| 12 | **Swift** | 22 | 443 | 3.49 | 7.91 | 8 | Full |
| 13 | **Dart** | 26 | 450 | 3.28 | 7.03 | 8 | Full |
| 14 | **Lua** | 30 | 458 | 3.47 | 6.74 | 8 | Full |
| 15 | **Rust** | 13 | 471 | 3.23 | 7.48 | 8 | Full |
| 16 | **Perl** | 11 | 478 | 3.01 | 7.03 | 8 | Full |
| 17 | **PHP** | 15 | 489 | 3.27 | 8.02 | 8 | Full |
| 18 | **Go** | 16 | 514 | 3.34 | 4.32 | 8 | Full |
| 19 | **Visual Basic** | 7 | 569 | 4.31 | 6.77 | 8 | Full |
| 20 | **Classic VB** | 24 | 620 | 3.73 | 7.05 | 8 | Full |
| 21 | **Assembly** | 19 | 651 | 2.49 | 5.29 | 3 | Limited (low-level) |
| 22 | **Java** | 3 | 657 | 4.76 | 6.20 | 8 | Full |
| 23 | **C++** | 4 | 704 | 3.64 | 6.18 | 8 | Full |
| 24 | **Objective-C** | 29 | 714 | 4.18 | 6.74 | 8 | Full |
| 25 | **Ada** | 18 | 810 | 3.77 | 7.17 | 8 | Full |
| 26 | **Delphi** | 9 | 848 | 3.52 | 5.33 | 8 | Full |
| 27 | **Fortran** | 12 | 894 | 3.49 | 7.58 | 8 | Full |
| 28 | **C** | 2 | 1020 | 3.49 | 6.54 | 8 | Full |
| 29 | **COBOL** | 21 | 1362 | 3.56 | 9.46 | 8 | Full |
| 30 | **Scratch** | 17 | N/A | N/A | N/A | 0 | Excluded (visual) |

---

## Normalized Comparison (8-Task Languages Only)

For fair comparison, considering only languages with all 8 tasks:

| Rank | Language | Total Tokens | Efficiency vs Python |
|------|----------|--------------|---------------------|
| 1 | Kotlin | 317 | 3.1% more efficient |
| 2 | Python | 327 | baseline |
| 3 | Julia | 353 | 8.0% less efficient |
| 4 | Ruby | 363 | 11.0% less efficient |
| 5 | R | 391 | 19.6% less efficient |
| 6 | JavaScript | 412 | 26.0% less efficient |
| 7 | C# | 433 | 32.4% less efficient |
| 8 | MATLAB | 437 | 33.6% less efficient |
| 9 | Swift | 443 | 35.5% less efficient |
| 10 | Dart | 450 | 37.6% less efficient |
| 11 | Lua | 458 | 40.1% less efficient |
| 12 | Rust | 471 | 44.0% less efficient |
| 13 | Perl | 478 | 46.2% less efficient |
| 14 | PHP | 489 | 49.5% less efficient |
| 15 | Go | 514 | 57.2% less efficient |
| 16 | Visual Basic | 569 | 74.0% less efficient |
| 17 | Classic VB | 620 | 89.6% less efficient |
| 18 | Java | 657 | 100.9% less efficient |
| 19 | C++ | 704 | 115.3% less efficient |
| 20 | Objective-C | 714 | 118.3% less efficient |
| 21 | Ada | 810 | 147.7% less efficient |
| 22 | Delphi | 848 | 159.3% less efficient |
| 23 | Fortran | 894 | 173.4% less efficient |
| 24 | C | 1020 | 211.9% less efficient |
| 25 | COBOL | 1362 | 316.5% less efficient |

---

## Detailed Language Profiles

### Tier 1: Most Efficient (≤400 tokens)

#### 1. Kotlin (317 tokens) - TIOBE #20

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 12 | 11th |
| Function | 15 | 10th |
| FizzBuzz | 67 | 4th |
| List Ops | 28 | 4th |
| Class/Struct | 61 | **1st** |
| File I/O | 85 | 7th |
| Error Handling | 18 | **1st** |
| HTTP Request | 31 | **1st** |

**Strengths:** Type inference, null safety operators, extension functions, concise lambdas

**Sample:** `fun add(a: Int, b: Int) = a + b`

---

#### 2. Python (327 tokens) - TIOBE #1

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 12 | 2nd |
| FizzBuzz | 63 | **1st** |
| List Ops | 26 | 3rd |
| Class/Struct | 63 | 4th |
| File I/O | 70 | 4th |
| Error Handling | 30 | 3rd |
| HTTP Request | 57 | 6th (tie) |

**Strengths:** Whitespace-significant (no braces), excellent tokenizer training, minimal boilerplate

**Sample:** `print("Hello, World!")`

---

#### 3. Julia (353 tokens) - TIOBE #28

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 10 | **1st** |
| FizzBuzz | 66 | 3rd |
| List Ops | 24 | 2nd |
| Class/Struct | 64 | 5th (tie) |
| File I/O | 99 | 9th |
| Error Handling | 40 | 6th |
| HTTP Request | 44 | 2nd |

**Strengths:** Mathematical notation, Unicode identifiers, clean syntax

**Sample:** `add(a, b) = a + b`

---

#### 4. Ruby (363 tokens) - TIOBE #27

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 13 | 3rd (tie) |
| FizzBuzz | 68 | 5th |
| List Ops | 30 | 6th (tie) |
| Class/Struct | 74 | 9th (tie) |
| File I/O | 76 | 5th |
| Error Handling | 36 | 5th |
| HTTP Request | 60 | 8th |

**Strengths:** Blocks, implicit returns, expressive syntax

**Sample:** `puts "Hello, World!"`

---

#### 5. R (391 tokens) - TIOBE #10

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 14 | 6th (tie) |
| FizzBuzz | 77 | 10th |
| List Ops | 30 | 6th (tie) |
| Class/Struct | 91 | 17th (tie) |
| File I/O | 61 | 3rd |
| Error Handling | 65 | 14th |
| HTTP Request | 47 | 4th |

**Strengths:** Statistical computing primitives, vectorized operations

**Sample:** `print("Hello, World!")`

---

### Tier 2: Efficient (401-500 tokens)

#### 6. JavaScript (412 tokens) - TIOBE #6

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 7 | 8th (tie) |
| Function | 14 | 6th (tie) |
| FizzBuzz | 79 | 11th (tie) |
| List Ops | 30 | 6th (tie) |
| Class/Struct | 65 | 7th |
| File I/O | 108 | 13th |
| Error Handling | 52 | 8th (tie) |
| HTTP Request | 57 | 6th (tie) |

**Total:** 412 tokens | **Chars/Token:** 3.69 | **Efficiency vs Python:** 26.0% less efficient

---

#### 7. C# (433 tokens) - TIOBE #5

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 7 | 8th (tie) |
| Function | 13 | 3rd (tie) |
| FizzBuzz | 79 | 11th (tie) |
| List Ops | 39 | 12th (tie) |
| Class/Struct | 90 | 16th |
| File I/O | 84 | 6th |
| Error Handling | 50 | 7th |
| HTTP Request | 71 | 14th |

**Total:** 433 tokens | **Chars/Token:** 3.83 | **Efficiency vs Python:** 32.4% less efficient

---

#### 8. MATLAB (437 tokens) - TIOBE #14

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 17 | 14th |
| FizzBuzz | 72 | 7th |
| List Ops | 34 | 9th |
| Class/Struct | 91 | 17th (tie) |
| File I/O | 94 | 8th |
| Error Handling | 77 | 19th |
| HTTP Request | 46 | 3rd |

**Total:** 437 tokens | **Chars/Token:** 3.49 | **Efficiency vs Python:** 33.6% less efficient

---

#### 9. Swift (443 tokens) - TIOBE #22

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 21 | 16th (tie) |
| FizzBuzz | 65 | 2nd |
| List Ops | 37 | 11th |
| Class/Struct | 62 | 3rd |
| File I/O | 120 | 16th (tie) |
| Error Handling | 62 | 13th |
| HTTP Request | 70 | 13th |

**Total:** 443 tokens | **Chars/Token:** 3.49 | **Efficiency vs Python:** 35.5% less efficient

---

#### 10. Dart (450 tokens) - TIOBE #26

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 12 | 11th (tie) |
| Function | 13 | 3rd (tie) |
| FizzBuzz | 90 | 16th |
| List Ops | 39 | 12th (tie) |
| Class/Struct | 64 | 5th (tie) |
| File I/O | 117 | 15th |
| Error Handling | 52 | 8th (tie) |
| HTTP Request | 63 | 9th |

**Total:** 450 tokens | **Chars/Token:** 3.28 | **Efficiency vs Python:** 37.6% less efficient

---

#### 11. Lua (458 tokens) - TIOBE #30

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 6 | **1st (tie)** |
| Function | 14 | 6th (tie) |
| FizzBuzz | 71 | 6th |
| List Ops | 54 | 16th (tie) |
| Class/Struct | 74 | 9th (tie) |
| File I/O | 120 | 16th (tie) |
| Error Handling | 54 | 11th |
| HTTP Request | 65 | 10th |

**Total:** 458 tokens | **Chars/Token:** 3.47 | **Efficiency vs Python:** 40.1% less efficient

---

#### 12. Rust (471 tokens) - TIOBE #13

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 12 | 11th (tie) |
| Function | 22 | 19th (tie) |
| FizzBuzz | 73 | 8th |
| List Ops | 45 | 14th |
| Class/Struct | 95 | 19th |
| File I/O | 138 | 18th |
| Error Handling | 33 | 4th |
| HTTP Request | 53 | 5th |

**Total:** 471 tokens | **Chars/Token:** 3.23 | **Efficiency vs Python:** 44.0% less efficient

---

#### 13. Perl (478 tokens) - TIOBE #11

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 13 | 14th (tie) |
| Function | 22 | 19th (tie) |
| FizzBuzz | 85 | 14th |
| List Ops | 34 | 9th (tie) |
| Class/Struct | 101 | 21st |
| File I/O | 99 | 9th (tie) |
| Error Handling | 57 | 12th |
| HTTP Request | 67 | 11th (tie) |

**Total:** 478 tokens | **Chars/Token:** 3.01 | **Efficiency vs Python:** 46.2% less efficient

---

#### 14. PHP (489 tokens) - TIOBE #15

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 11 | 10th |
| Function | 21 | 16th (tie) |
| FizzBuzz | 82 | 13th |
| List Ops | 48 | 15th |
| Class/Struct | 84 | 14th |
| File I/O | 104 | 11th |
| Error Handling | 72 | 15th |
| HTTP Request | 67 | 11th (tie) |

**Total:** 489 tokens | **Chars/Token:** 3.27 | **Efficiency vs Python:** 49.5% less efficient

---

### Tier 3: Moderate (501-700 tokens)

#### 15. Go (514 tokens) - TIOBE #16

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 19 | 20th |
| Function | 18 | 15th |
| FizzBuzz | 88 | 15th |
| List Ops | 58 | 19th |
| Class/Struct | 82 | 12th (tie) |
| File I/O | 147 | 19th |
| Error Handling | 24 | 2nd |
| HTTP Request | 78 | 15th (tie) |

**Total:** 514 tokens | **Chars/Token:** 3.34 | **Efficiency vs Python:** 57.2% less efficient

**Note:** Go's explicit error handling (`if err != nil`) adds tokens but excels in Task 7.

---

#### 16. Visual Basic (569 tokens) - TIOBE #7

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 22 | 21st |
| Function | 30 | 25th |
| FizzBuzz | 95 | 18th (tie) |
| List Ops | 57 | 18th |
| Class/Struct | 99 | 20th |
| File I/O | 106 | 12th |
| Error Handling | 74 | 16th (tie) |
| HTTP Request | 86 | 18th |

**Total:** 569 tokens | **Chars/Token:** 4.31 | **Efficiency vs Python:** 74.0% less efficient

---

#### 17. Classic VB (620 tokens) - TIOBE #24

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 13 | 14th (tie) |
| Function | 23 | 21st (tie) |
| FizzBuzz | 92 | 17th |
| List Ops | 83 | 23rd |
| Class/Struct | 70 | 8th |
| File I/O | 206 | 22nd |
| Error Handling | 53 | 10th |
| HTTP Request | 80 | 17th |

**Total:** 620 tokens | **Chars/Token:** 3.73 | **Efficiency vs Python:** 89.6% less efficient

---

#### 18. Java (657 tokens) - TIOBE #3

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 26 | 23rd |
| Function | 25 | 23rd |
| FizzBuzz | 104 | 22nd |
| List Ops | 68 | 20th |
| Class/Struct | 82 | 12th (tie) |
| File I/O | 154 | 20th |
| Error Handling | 76 | 18th |
| HTTP Request | 122 | 21st |

**Total:** 657 tokens | **Chars/Token:** 4.76 | **Efficiency vs Python:** 100.9% less efficient

**Note:** Java requires 2.1x more tokens than Kotlin for equivalent functionality.

---

### Tier 4: Verbose (701-900 tokens)

#### 19. C++ (704 tokens) - TIOBE #4

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 29 | 25th (tie) |
| Function | 16 | 11th (tie) |
| FizzBuzz | 122 | 24th (tie) |
| List Ops | 69 | 21st |
| Class/Struct | 76 | 11th |
| File I/O | 110 | 14th |
| Error Handling | 84 | 20th (tie) |
| HTTP Request | 198 | 24th |

**Total:** 704 tokens | **Chars/Token:** 3.64 | **Efficiency vs Python:** 115.3% less efficient

---

#### 20. Objective-C (714 tokens) - TIOBE #29

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 29 | 25th (tie) |
| Function | 16 | 11th (tie) |
| FizzBuzz | 103 | 21st |
| List Ops | 72 | 22nd |
| Class/Struct | 143 | 24th |
| File I/O | 155 | 21st |
| Error Handling | 84 | 20th (tie) |
| HTTP Request | 112 | 19th |

**Total:** 714 tokens | **Chars/Token:** 4.18 | **Efficiency vs Python:** 118.3% less efficient

---

#### 21. Ada (810 tokens) - TIOBE #18

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 27 | 24th |
| Function | 23 | 21st (tie) |
| FizzBuzz | 122 | 24th (tie) |
| List Ops | 108 | 25th |
| Class/Struct | 120 | 23rd |
| File I/O | 258 | 25th |
| Error Handling | 74 | 16th (tie) |
| HTTP Request | 78 | 15th (tie) |

**Total:** 810 tokens | **Chars/Token:** 3.77 | **Efficiency vs Python:** 147.7% less efficient

---

#### 22. Delphi/Object Pascal (848 tokens) - TIOBE #9

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 15 | 17th (tie) |
| Function | 21 | 16th (tie) |
| FizzBuzz | 95 | 18th (tie) |
| List Ops | 131 | 27th |
| Class/Struct | 154 | 25th |
| File I/O | 211 | 23rd |
| Error Handling | 84 | 20th (tie) |
| HTTP Request | 137 | 23rd |

**Total:** 848 tokens | **Chars/Token:** 3.52 | **Efficiency vs Python:** 159.3% less efficient

---

#### 23. Fortran (894 tokens) - TIOBE #12

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 15 | 17th (tie) |
| Function | 36 | 26th |
| FizzBuzz | 106 | 23rd |
| List Ops | 107 | 24th |
| Class/Struct | 110 | 22nd |
| File I/O | 282 | 26th |
| Error Handling | 122 | 24th |
| HTTP Request | 116 | 20th |

**Total:** 894 tokens | **Chars/Token:** 3.49 | **Efficiency vs Python:** 173.4% less efficient

---

### Tier 5: Very Verbose (>900 tokens)

#### 24. C (1020 tokens) - TIOBE #2

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 24 | 22nd |
| Function | 16 | 11th (tie) |
| FizzBuzz | 99 | 20th |
| List Ops | 130 | 26th |
| Class/Struct | 88 | 15th |
| File I/O | 257 | 24th |
| Error Handling | 111 | 23rd |
| HTTP Request | 295 | **25th** |

**Total:** 1020 tokens | **Chars/Token:** 3.49 | **Efficiency vs Python:** 211.9% less efficient

**Note:** Manual memory management and verbose HTTP libraries significantly increase token count.

---

#### 25. COBOL (1362 tokens) - TIOBE #21

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 31 | 27th |
| Function | 84 | **27th** |
| FizzBuzz | 224 | 26th |
| List Ops | 226 | **28th** |
| Class/Struct | 239 | **26th** |
| File I/O | 288 | **27th** |
| Error Handling | 146 | **25th** |
| HTTP Request | 124 | 22nd |

**Total:** 1362 tokens | **Chars/Token:** 3.56 | **Efficiency vs Python:** 316.5% less efficient

**Note:** COBOL's English-like verbose syntax requires 4.2x more tokens than Python.

---

### Limited Evaluation Languages

#### Assembly x86-64 (651 tokens for 3 tasks) - TIOBE #19

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 85 | **28th** |
| Function | 29 | 24th |
| FizzBuzz | 537 | **27th** |

**Note:** Low-level operations require many instructions. Excluded from Tasks 4-8.

---

#### SQL (41 tokens for 2 tasks) - TIOBE #8

| Task | Tokens | Rank |
|------|--------|------|
| List Ops | 20 | **1st** |
| File I/O | 21 | **1st** |

**Note:** SQL excels at set operations but is domain-specific.

---

#### SAS (83 tokens for 3 tasks) - TIOBE #25

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 13 | 14th (tie) |
| List Ops | 29 | 5th |
| File I/O | 41 | 2nd |

**Note:** Statistical computing domain. Excluded from Tasks 2, 3, 5, 7, 8.

---

#### Prolog (219 tokens for 5 tasks) - TIOBE #23

| Task | Tokens | Rank |
|------|--------|------|
| Hello World | 15 | 17th (tie) |
| Function | 14 | 6th (tie) |
| FizzBuzz | 75 | 9th |
| List Ops | 54 | 16th (tie) |
| Class/Struct | 61 | **1st (tie)** |

**Note:** Declarative paradigm. Excluded from Tasks 6-8.

---

#### Scratch - TIOBE #17

**Status:** Excluded from benchmark

**Reason:** Visual block-based programming language that cannot be represented as text tokens. Not applicable for LLM tokenization analysis.

---

## Per-Task Breakdown

### Task 1: Hello World

Print "Hello, World!" to stdout.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | Julia | 6 |
| 1 | Lua | 6 |
| 1 | MATLAB | 6 |
| 1 | Python | 6 |
| 1 | R | 6 |
| 1 | Ruby | 6 |
| 1 | Swift | 6 |
| 8 | C# | 7 |
| 8 | JavaScript | 7 |
| 10 | PHP | 11 |
| 11 | Dart | 12 |
| 11 | Kotlin | 12 |
| 11 | Rust | 12 |
| 14 | Classic VB | 13 |
| 14 | Perl | 13 |
| 14 | SAS | 13 |
| 17 | Delphi | 15 |
| 17 | Fortran | 15 |
| 17 | Prolog | 15 |
| 20 | Go | 19 |
| 21 | Visual Basic | 22 |
| 22 | C | 24 |
| 23 | Java | 26 |
| 24 | Ada | 27 |
| 25 | C++ | 29 |
| 25 | Objective-C | 29 |
| 27 | COBOL | 31 |
| 28 | Assembly | 85 |

---

### Task 2: Function Definition

Define a function `add(a, b)` that returns the sum of two numbers.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | Julia | 10 |
| 2 | Python | 12 |
| 3 | C# | 13 |
| 3 | Dart | 13 |
| 3 | Ruby | 13 |
| 6 | JavaScript | 14 |
| 6 | Lua | 14 |
| 6 | Prolog | 14 |
| 6 | R | 14 |
| 10 | Kotlin | 15 |
| 11 | C | 16 |
| 11 | C++ | 16 |
| 11 | Objective-C | 16 |
| 14 | MATLAB | 17 |
| 15 | Go | 18 |
| 16 | Delphi | 21 |
| 16 | PHP | 21 |
| 16 | Swift | 21 |
| 19 | Perl | 22 |
| 19 | Rust | 22 |
| 21 | Ada | 23 |
| 21 | Classic VB | 23 |
| 23 | Java | 25 |
| 24 | Assembly | 29 |
| 25 | Visual Basic | 30 |
| 26 | Fortran | 36 |
| 27 | COBOL | 84 |

---

### Task 3: FizzBuzz

Print numbers 1-100 with FizzBuzz logic.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | Python | 63 |
| 2 | Swift | 65 |
| 3 | Julia | 66 |
| 4 | Kotlin | 67 |
| 5 | Ruby | 68 |
| 6 | Lua | 71 |
| 7 | MATLAB | 72 |
| 8 | Rust | 73 |
| 9 | Prolog | 75 |
| 10 | R | 77 |
| 11 | C# | 79 |
| 11 | JavaScript | 79 |
| 13 | PHP | 82 |
| 14 | Perl | 85 |
| 15 | Go | 88 |
| 16 | Dart | 90 |
| 17 | Classic VB | 92 |
| 18 | Delphi | 95 |
| 18 | Visual Basic | 95 |
| 20 | C | 99 |
| 21 | Objective-C | 103 |
| 22 | Java | 104 |
| 23 | Fortran | 106 |
| 24 | Ada | 122 |
| 24 | C++ | 122 |
| 26 | COBOL | 224 |
| 27 | Assembly | 537 |

---

### Task 4: List Manipulation

Filter even numbers and double them.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | SQL | 20 |
| 2 | Julia | 24 |
| 3 | Python | 26 |
| 4 | Kotlin | 28 |
| 5 | SAS | 29 |
| 6 | JavaScript | 30 |
| 6 | R | 30 |
| 6 | Ruby | 30 |
| 9 | MATLAB | 34 |
| 9 | Perl | 34 |
| 11 | Swift | 37 |
| 12 | C# | 39 |
| 12 | Dart | 39 |
| 14 | Rust | 45 |
| 15 | PHP | 48 |
| 16 | Lua | 54 |
| 16 | Prolog | 54 |
| 18 | Visual Basic | 57 |
| 19 | Go | 58 |
| 20 | Java | 68 |
| 21 | C++ | 69 |
| 22 | Objective-C | 72 |
| 23 | Classic VB | 83 |
| 24 | Fortran | 107 |
| 25 | Ada | 108 |
| 26 | C | 130 |
| 27 | Delphi | 131 |
| 28 | COBOL | 226 |

---

### Task 5: Class/Struct

Define a Point type with distance calculation.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | Kotlin | 61 |
| 1 | Prolog | 61 |
| 3 | Swift | 62 |
| 4 | Python | 63 |
| 5 | Dart | 64 |
| 5 | Julia | 64 |
| 7 | JavaScript | 65 |
| 8 | Classic VB | 70 |
| 9 | Lua | 74 |
| 9 | Ruby | 74 |
| 11 | C++ | 76 |
| 12 | Go | 82 |
| 12 | Java | 82 |
| 14 | PHP | 84 |
| 15 | C | 88 |
| 16 | C# | 90 |
| 17 | MATLAB | 91 |
| 17 | R | 91 |
| 19 | Rust | 95 |
| 20 | Visual Basic | 99 |
| 21 | Perl | 101 |
| 22 | Fortran | 110 |
| 23 | Ada | 120 |
| 24 | Objective-C | 143 |
| 25 | Delphi | 154 |
| 26 | COBOL | 239 |

---

### Task 6: File I/O

Read file, count words, write results.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | SQL | 21 |
| 2 | SAS | 41 |
| 3 | R | 61 |
| 4 | Python | 70 |
| 5 | Ruby | 76 |
| 6 | C# | 84 |
| 7 | Kotlin | 85 |
| 8 | MATLAB | 94 |
| 9 | Julia | 99 |
| 9 | Perl | 99 |
| 11 | PHP | 104 |
| 12 | Visual Basic | 106 |
| 13 | JavaScript | 108 |
| 14 | C++ | 110 |
| 15 | Dart | 117 |
| 16 | Lua | 120 |
| 16 | Swift | 120 |
| 18 | Rust | 138 |
| 19 | Go | 147 |
| 20 | Java | 154 |
| 21 | Objective-C | 155 |
| 22 | Classic VB | 206 |
| 23 | Delphi | 211 |
| 24 | C | 257 |
| 25 | Ada | 258 |
| 26 | Fortran | 282 |
| 27 | COBOL | 288 |

---

### Task 7: Error Handling

Parse integer with success/failure indication.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | Kotlin | 18 |
| 2 | Go | 24 |
| 3 | Python | 30 |
| 4 | Rust | 33 |
| 5 | Ruby | 36 |
| 6 | Julia | 40 |
| 7 | C# | 50 |
| 8 | Dart | 52 |
| 8 | JavaScript | 52 |
| 10 | Classic VB | 53 |
| 11 | Lua | 54 |
| 12 | Perl | 57 |
| 13 | Swift | 62 |
| 14 | R | 65 |
| 15 | PHP | 72 |
| 16 | Ada | 74 |
| 16 | Visual Basic | 74 |
| 18 | Java | 76 |
| 19 | MATLAB | 77 |
| 20 | C++ | 84 |
| 20 | Delphi | 84 |
| 20 | Objective-C | 84 |
| 23 | C | 111 |
| 24 | Fortran | 122 |
| 25 | COBOL | 146 |

---

### Task 8: HTTP Request

Fetch URL content with error handling.

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | Kotlin | 31 |
| 2 | Julia | 44 |
| 3 | MATLAB | 46 |
| 4 | R | 47 |
| 5 | Rust | 53 |
| 6 | JavaScript | 57 |
| 6 | Python | 57 |
| 8 | Ruby | 60 |
| 9 | Dart | 63 |
| 10 | Lua | 65 |
| 11 | Perl | 67 |
| 11 | PHP | 67 |
| 13 | Swift | 70 |
| 14 | C# | 71 |
| 15 | Ada | 78 |
| 15 | Go | 78 |
| 17 | Classic VB | 80 |
| 18 | Visual Basic | 86 |
| 19 | Objective-C | 112 |
| 20 | Fortran | 116 |
| 21 | Java | 122 |
| 22 | COBOL | 124 |
| 23 | Delphi | 137 |
| 24 | C++ | 198 |
| 25 | C | 295 |

---

## Statistical Analysis

### Token Efficiency by Language Family

| Family | Languages | Avg Tokens | Best | Worst |
|--------|-----------|------------|------|-------|
| Dynamic Scripting | Python, Ruby, Julia, Lua, Perl | 396 | Python (327) | Perl (478) |
| Modern JVM | Kotlin, Java | 487 | Kotlin (317) | Java (657) |
| Modern Systems | Rust, Go, Swift | 476 | Swift (443) | Go (514) |
| C-Family | C, C++, Objective-C | 813 | C++ (704) | C (1020) |
| Legacy Enterprise | COBOL, Fortran, Ada | 1022 | Ada (810) | COBOL (1362) |
| Visual Basic | VB.NET, Classic VB | 594 | VB.NET (569) | Classic VB (620) |
| Domain-Specific | SQL, SAS, MATLAB | - | SQL (41/2) | MATLAB (437) |

---

### Task-by-Task Champions

| Task | Most Efficient | Tokens | Least Efficient | Tokens | Ratio |
|------|----------------|--------|-----------------|--------|-------|
| Hello World | Julia/Lua/MATLAB/Python/R/Ruby/Swift | 6 | Assembly | 85 | 14.2x |
| Function | Julia | 10 | COBOL | 84 | 8.4x |
| FizzBuzz | Python | 63 | Assembly | 537 | 8.5x |
| List Ops | SQL | 20 | COBOL | 226 | 11.3x |
| Class/Struct | Kotlin/Prolog | 61 | COBOL | 239 | 3.9x |
| File I/O | SQL | 21 | COBOL | 288 | 13.7x |
| Error Handling | Kotlin | 18 | COBOL | 146 | 8.1x |
| HTTP Request | Kotlin | 31 | C | 295 | 9.5x |

---

### Tokenizer Affinity (Chars/Token)

Higher values indicate the language compresses well with cl100k_base:

| Rank | Language | Chars/Token | Interpretation |
|------|----------|-------------|----------------|
| 1 | Java | 4.76 | Very well compressed |
| 2 | Visual Basic | 4.31 | Well compressed |
| 3 | Objective-C | 4.18 | Well compressed |
| 4 | C# | 3.83 | Above average |
| 5 | Ada | 3.77 | Above average |
| 6 | Classic VB | 3.73 | Above average |
| 7 | JavaScript | 3.69 | Above average |
| 8 | C++ | 3.64 | Average |
| 9 | Python | 3.61 | Average |
| 10 | COBOL | 3.56 | Average |
| 11 | Delphi | 3.52 | Average |
| 12 | C | 3.49 | Average |
| 12 | Fortran | 3.49 | Average |
| 12 | MATLAB | 3.49 | Average |
| 12 | SQL | 3.49 | Average |
| 12 | Swift | 3.49 | Average |
| 17 | Lua | 3.47 | Average |
| 18 | Kotlin | 3.46 | Average |
| 19 | Go | 3.34 | Below average |
| 20 | R | 3.31 | Below average |
| 21 | SAS | 3.30 | Below average |
| 22 | Dart | 3.28 | Below average |
| 23 | PHP | 3.27 | Below average |
| 24 | Rust | 3.23 | Below average |
| 25 | Julia | 3.19 | Below average |
| 26 | Perl | 3.01 | Below average |
| 27 | Ruby | 2.95 | Below average |
| 28 | Prolog | 2.74 | Poor compression |
| 29 | Assembly | 2.49 | Poor compression |

---

## Recommendations

### By Use Case

| Use Case | Recommended | Alternative | Avoid |
|----------|-------------|-------------|-------|
| General scripting | Python | Ruby, Julia | COBOL, C |
| JVM projects | Kotlin | - | Java (2.1x more tokens) |
| Systems programming | Rust | Go | C (2.2x more tokens) |
| Web backend | JavaScript | PHP | Java |
| Web frontend | JavaScript | Dart | - |
| Mobile (iOS) | Swift | - | Objective-C |
| Mobile (Android) | Kotlin | - | Java |
| Data science | Julia, R | Python | - |
| Scientific computing | Julia | MATLAB | Fortran |
| Enterprise legacy | - | - | COBOL (use Kotlin/Python if possible) |

---

### Token Budget Planning

For a 128K context window, approximate code capacity:

| Language | Est. Lines | Est. Files (500 LOC each) |
|----------|-----------|---------------------------|
| Python | ~18,000 | ~36 |
| Kotlin | ~16,500 | ~33 |
| JavaScript | ~18,600 | ~37 |
| Java | ~10,600 | ~21 |
| C | ~9,800 | ~20 |
| COBOL | ~6,800 | ~14 |

---

## Key Findings Summary

### Most Token-Efficient Languages (All 8 Tasks)

1. **Kotlin** (317 tokens) - Concise syntax, type inference, extension functions
2. **Python** (327 tokens) - Minimal syntax, whitespace-significant, excellent tokenizer training
3. **Julia** (353 tokens) - Mathematical notation, Unicode support, clean syntax
4. **Ruby** (363 tokens) - Minimal boilerplate, expressive blocks, clean syntax
5. **R** (391 tokens) - Statistical computing optimized

### Least Token-Efficient Languages

1. **COBOL** (1362 tokens) - Verbose English-like syntax, required divisions
2. **C** (1020 tokens) - Manual memory management, explicit typing, header includes
3. **Fortran** (894 tokens) - Legacy syntax, explicit declarations
4. **Delphi** (848 tokens) - Pascal heritage, verbose declarations
5. **Ada** (810 tokens) - Verbose by design for safety, explicit everything

### Language Family Patterns

| Family | Avg Tokens | Representative Languages |
|--------|------------|-------------------------|
| Dynamic Scripting | ~396 | Python, Ruby, Julia, Lua, Perl |
| Modern JVM | ~487 | Kotlin, Java |
| Modern Systems | ~476 | Rust, Go, Swift |
| C-Family | ~813 | C, C++, Objective-C |
| Legacy Enterprise | ~1022 | COBOL, Fortran, Ada |
| Visual Basic | ~594 | VB.NET, Classic VB |

### Implications for LLM Applications

1. **Context Window Efficiency**: Using Python/Ruby over Java/C could reduce context usage by 60-200%
2. **Code Generation**: More token-efficient languages allow generating longer programs within output limits
3. **Code Understanding**: Concise languages require fewer tokens to represent equivalent semantics
4. **Multi-file Projects**: Token savings compound significantly across large codebases

---

## Conclusion

**Kotlin** (317 tokens) is the most token-efficient general-purpose language for LLM applications, offering a 3.1% advantage over Python and a remarkable 2.1x efficiency gain over Java for JVM projects.

**Python** (327 tokens) remains an excellent choice, ranking #2 overall with the strongest ecosystem and highest tokenizer training representation.

**Key insights:**

1. Modern languages (Kotlin, Swift, Rust) significantly outperform their predecessors (Java, Objective-C, C)
2. Legacy enterprise languages (COBOL, Fortran) consume 3-4x more tokens than modern alternatives
3. Language family matters more than age - dynamic scripting languages average 396 tokens vs. 1022 for legacy enterprise
4. SQL dominates domain-specific tasks but lacks general applicability

For LLM-based code generation and analysis, choosing token-efficient languages can reduce API costs by 50-75% while fitting more code context into limited windows.

---

*Report generated using cl100k_base tokenization via tiktoken*
*Benchmark data: January 2026*
