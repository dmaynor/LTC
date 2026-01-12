# Token Efficiency Benchmark Results

*Comparing token counts across 29 programming languages using cl100k_base tokenization (GPT-4/Claude)*

## Methodology

### Overview
This benchmark compares the token efficiency of 29 programming languages from the TIOBE Index Top 30 (January 2026), measuring how many tokens are required to express equivalent functionality across standardized tasks.

### Languages Evaluated
All TIOBE Top 30 languages except Scratch (visual/block-based, not text-tokenizable):
- **Full 8 tasks**: Python, C, Java, C++, C#, JavaScript, Visual Basic, Delphi, R, Perl, Fortran, Rust, MATLAB, PHP, Go, Ada, Kotlin, COBOL, Swift, Classic VB, Dart, Ruby, Julia, Objective-C, Lua
- **Limited tasks**: SQL (2), SAS (3), Prolog (5), Assembly (3) - due to paradigm constraints

### Tasks Implemented
1. **Hello World** - Basic output
2. **Function Definition** - Simple arithmetic function
3. **FizzBuzz** - Control flow and conditionals
4. **List Manipulation** - Filter and transform collections
5. **Class/Struct** - Object-oriented data structure with methods
6. **File I/O** - Read, process, and write files
7. **Error Handling** - Parse with success/failure indication
8. **HTTP Request** - Network request with error handling

### Tokenization
Uses **cl100k_base** encoding via tiktoken - the same tokenizer used by GPT-4 and Claude models.

## Summary Table

| Rank | Language | Total Tokens | Chars/Token | Tokens/Line | Tasks |
|------|----------|--------------|-------------|-------------|-------|
| 1 | sql | 41 | 3.49 | 5.86 | 2 |
| 2 | sas | 83 | 3.3 | 4.88 | 3 |
| 3 | prolog | 219 | 2.74 | 9.12 | 5 |
| 4 | kotlin | 317 | 3.46 | 7.73 | 8 |
| 5 | python | 327 | 3.61 | 7.11 | 8 |
| 6 | julia | 353 | 3.19 | 6.3 | 8 |
| 7 | ruby | 363 | 2.95 | 6.48 | 8 |
| 8 | haskell | 364 | 3.19 | 10.11 | 8 |
| 9 | r | 391 | 3.31 | 7.52 | 8 |
| 10 | javascript | 412 | 3.69 | 6.87 | 8 |
| 11 | csharp | 433 | 3.83 | 6.1 | 8 |
| 12 | matlab | 437 | 3.49 | 6.33 | 8 |
| 13 | swift | 443 | 3.49 | 7.91 | 8 |
| 14 | dart | 450 | 3.28 | 7.03 | 8 |
| 15 | lua | 458 | 3.47 | 6.74 | 8 |
| 16 | rust | 471 | 3.23 | 7.48 | 8 |
| 17 | perl | 478 | 3.01 | 7.03 | 8 |
| 18 | php | 489 | 3.27 | 8.02 | 8 |
| 19 | ocaml | 493 | 3.1 | 9.67 | 8 |
| 20 | go | 514 | 3.34 | 4.32 | 8 |
| 21 | visualbasic | 569 | 4.31 | 6.77 | 8 |
| 22 | classicvb | 620 | 3.73 | 7.05 | 8 |
| 23 | assembly | 651 | 2.49 | 5.29 | 3 |
| 24 | java | 657 | 4.76 | 6.2 | 8 |
| 25 | cpp | 704 | 3.64 | 6.18 | 8 |
| 26 | objectivec | 714 | 4.18 | 6.74 | 8 |
| 27 | ada | 810 | 3.77 | 7.17 | 8 |
| 28 | delphi | 848 | 3.52 | 5.33 | 8 |
| 29 | fortran | 894 | 3.49 | 7.58 | 8 |
| 30 | c | 1020 | 3.49 | 6.54 | 8 |
| 31 | cobol | 1362 | 3.56 | 9.46 | 8 |

## Normalized Comparison (8-Task Languages Only)

For fair comparison, considering only languages with all 8 tasks:

| Rank | Language | Total Tokens | Efficiency vs Python |
|------|----------|--------------|---------------------|
| 1 | kotlin | 317 | 3.1% more efficient |
| 2 | python | 327 | baseline |
| 3 | julia | 353 | 8.0% less efficient |
| 4 | ruby | 363 | 11.0% less efficient |
| 5 | haskell | 364 | 11.3% less efficient |
| 6 | r | 391 | 19.6% less efficient |
| 7 | javascript | 412 | 26.0% less efficient |
| 8 | csharp | 433 | 32.4% less efficient |
| 9 | matlab | 437 | 33.6% less efficient |
| 10 | swift | 443 | 35.5% less efficient |
| 11 | dart | 450 | 37.6% less efficient |
| 12 | lua | 458 | 40.1% less efficient |
| 13 | rust | 471 | 44.0% less efficient |
| 14 | perl | 478 | 46.2% less efficient |
| 15 | php | 489 | 49.5% less efficient |
| 16 | ocaml | 493 | 50.8% less efficient |
| 17 | go | 514 | 57.2% less efficient |
| 18 | visualbasic | 569 | 74.0% less efficient |
| 19 | classicvb | 620 | 89.6% less efficient |
| 20 | java | 657 | 100.9% less efficient |
| 21 | cpp | 704 | 115.3% less efficient |
| 22 | objectivec | 714 | 118.3% less efficient |
| 23 | ada | 810 | 147.7% less efficient |
| 24 | delphi | 848 | 159.3% less efficient |
| 25 | fortran | 894 | 173.4% less efficient |
| 26 | c | 1020 | 211.9% less efficient |
| 27 | cobol | 1362 | 316.5% less efficient |

## Per-Task Breakdown


### task1_hello

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | julia | 6 |
| 2 | lua | 6 |
| 3 | matlab | 6 |
| 4 | python | 6 |
| 5 | r | 6 |
| 6 | ruby | 6 |
| 7 | swift | 6 |
| 8 | csharp | 7 |
| 9 | javascript | 7 |
| 10 | haskell | 8 |
| 11 | ocaml | 8 |
| 12 | php | 11 |
| 13 | dart | 12 |
| 14 | kotlin | 12 |
| 15 | rust | 12 |
| 16 | classicvb | 13 |
| 17 | perl | 13 |
| 18 | sas | 13 |
| 19 | delphi | 15 |
| 20 | fortran | 15 |
| 21 | prolog | 15 |
| 22 | go | 19 |
| 23 | visualbasic | 22 |
| 24 | c | 24 |
| 25 | java | 26 |
| 26 | ada | 27 |
| 27 | cpp | 29 |
| 28 | objectivec | 29 |
| 29 | cobol | 31 |
| 30 | assembly | 85 |

### task2_function

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | ocaml | 9 |
| 2 | julia | 10 |
| 3 | python | 12 |
| 4 | csharp | 13 |
| 5 | dart | 13 |
| 6 | ruby | 13 |
| 7 | javascript | 14 |
| 8 | lua | 14 |
| 9 | prolog | 14 |
| 10 | r | 14 |
| 11 | kotlin | 15 |
| 12 | c | 16 |
| 13 | cpp | 16 |
| 14 | objectivec | 16 |
| 15 | matlab | 17 |
| 16 | go | 18 |
| 17 | haskell | 19 |
| 18 | delphi | 21 |
| 19 | php | 21 |
| 20 | swift | 21 |
| 21 | perl | 22 |
| 22 | rust | 22 |
| 23 | ada | 23 |
| 24 | classicvb | 23 |
| 25 | java | 25 |
| 26 | assembly | 29 |
| 27 | visualbasic | 30 |
| 28 | fortran | 36 |
| 29 | cobol | 84 |

### task3_fizzbuzz

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | python | 63 |
| 2 | swift | 65 |
| 3 | julia | 66 |
| 4 | kotlin | 67 |
| 5 | ruby | 68 |
| 6 | lua | 71 |
| 7 | matlab | 72 |
| 8 | rust | 73 |
| 9 | prolog | 75 |
| 10 | r | 77 |
| 11 | csharp | 79 |
| 12 | javascript | 79 |
| 13 | ocaml | 82 |
| 14 | php | 82 |
| 15 | haskell | 83 |
| 16 | perl | 85 |
| 17 | go | 88 |
| 18 | dart | 90 |
| 19 | classicvb | 92 |
| 20 | delphi | 95 |
| 21 | visualbasic | 95 |
| 22 | c | 99 |
| 23 | objectivec | 103 |
| 24 | java | 104 |
| 25 | fortran | 106 |
| 26 | ada | 122 |
| 27 | cpp | 122 |
| 28 | cobol | 224 |
| 29 | assembly | 537 |

### task4_list

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | sql | 20 |
| 2 | haskell | 23 |
| 3 | julia | 24 |
| 4 | python | 26 |
| 5 | kotlin | 28 |
| 6 | sas | 29 |
| 7 | javascript | 30 |
| 8 | r | 30 |
| 9 | ruby | 30 |
| 10 | matlab | 34 |
| 11 | perl | 34 |
| 12 | ocaml | 35 |
| 13 | swift | 37 |
| 14 | csharp | 39 |
| 15 | dart | 39 |
| 16 | rust | 45 |
| 17 | php | 48 |
| 18 | lua | 54 |
| 19 | prolog | 54 |
| 20 | visualbasic | 57 |
| 21 | go | 58 |
| 22 | java | 68 |
| 23 | cpp | 69 |
| 24 | objectivec | 72 |
| 25 | classicvb | 83 |
| 26 | fortran | 107 |
| 27 | ada | 108 |
| 28 | c | 130 |
| 29 | delphi | 131 |
| 30 | cobol | 226 |

### task5_class

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | haskell | 52 |
| 2 | kotlin | 61 |
| 3 | prolog | 61 |
| 4 | swift | 62 |
| 5 | python | 63 |
| 6 | dart | 64 |
| 7 | julia | 64 |
| 8 | javascript | 65 |
| 9 | ocaml | 69 |
| 10 | classicvb | 70 |
| 11 | lua | 74 |
| 12 | ruby | 74 |
| 13 | cpp | 76 |
| 14 | go | 82 |
| 15 | java | 82 |
| 16 | php | 84 |
| 17 | c | 88 |
| 18 | csharp | 90 |
| 19 | matlab | 91 |
| 20 | r | 91 |
| 21 | rust | 95 |
| 22 | visualbasic | 99 |
| 23 | perl | 101 |
| 24 | fortran | 110 |
| 25 | ada | 120 |
| 26 | objectivec | 143 |
| 27 | delphi | 154 |
| 28 | cobol | 239 |

### task6_fileio

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | sql | 21 |
| 2 | sas | 41 |
| 3 | r | 61 |
| 4 | python | 70 |
| 5 | ruby | 76 |
| 6 | csharp | 84 |
| 7 | kotlin | 85 |
| 8 | haskell | 90 |
| 9 | matlab | 94 |
| 10 | julia | 99 |
| 11 | perl | 99 |
| 12 | php | 104 |
| 13 | visualbasic | 106 |
| 14 | javascript | 108 |
| 15 | cpp | 110 |
| 16 | dart | 117 |
| 17 | lua | 120 |
| 18 | swift | 120 |
| 19 | rust | 138 |
| 20 | go | 147 |
| 21 | java | 154 |
| 22 | objectivec | 155 |
| 23 | ocaml | 174 |
| 24 | classicvb | 206 |
| 25 | delphi | 211 |
| 26 | c | 257 |
| 27 | ada | 258 |
| 28 | fortran | 282 |
| 29 | cobol | 288 |

### task7_error

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | kotlin | 18 |
| 2 | go | 24 |
| 3 | python | 30 |
| 4 | rust | 33 |
| 5 | ocaml | 35 |
| 6 | ruby | 36 |
| 7 | julia | 40 |
| 8 | haskell | 45 |
| 9 | csharp | 50 |
| 10 | dart | 52 |
| 11 | javascript | 52 |
| 12 | classicvb | 53 |
| 13 | lua | 54 |
| 14 | perl | 57 |
| 15 | swift | 62 |
| 16 | r | 65 |
| 17 | php | 72 |
| 18 | ada | 74 |
| 19 | visualbasic | 74 |
| 20 | java | 76 |
| 21 | matlab | 77 |
| 22 | cpp | 84 |
| 23 | delphi | 84 |
| 24 | objectivec | 84 |
| 25 | c | 111 |
| 26 | fortran | 122 |
| 27 | cobol | 146 |

### task8_http

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | kotlin | 31 |
| 2 | haskell | 44 |
| 3 | julia | 44 |
| 4 | matlab | 46 |
| 5 | r | 47 |
| 6 | rust | 53 |
| 7 | javascript | 57 |
| 8 | python | 57 |
| 9 | ruby | 60 |
| 10 | dart | 63 |
| 11 | lua | 65 |
| 12 | perl | 67 |
| 13 | php | 67 |
| 14 | swift | 70 |
| 15 | csharp | 71 |
| 16 | ada | 78 |
| 17 | go | 78 |
| 18 | classicvb | 80 |
| 19 | ocaml | 81 |
| 20 | visualbasic | 86 |
| 21 | objectivec | 112 |
| 22 | fortran | 116 |
| 23 | java | 122 |
| 24 | cobol | 124 |
| 25 | delphi | 137 |
| 26 | cpp | 198 |
| 27 | c | 295 |

## Analysis

### Key Findings

#### Most Token-Efficient Languages (All 8 Tasks)

1. **Kotlin** (317 tokens) - Concise syntax, type inference, extension functions
2. **Python** (327 tokens) - Minimal syntax, whitespace-significant, excellent tokenizer training
3. **Julia** (353 tokens) - Mathematical notation, Unicode support, clean syntax
4. **Ruby** (363 tokens) - Minimal boilerplate, expressive blocks, clean syntax
5. **Haskell** (364 tokens) - Efficient syntax

#### Least Token-Efficient Languages

1. **Cobol** (1362 tokens) - Verbose English-like syntax, required divisions
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
| C-Family | ~813 | C, Cpp, Objectivec |
| Legacy Enterprise | ~1022 | Cobol, Fortran, Ada |
| Visual Basic | ~594 | Visualbasic, Classicvb |

### Task Complexity Impact

| Task | Avg Tokens | Variance | Most Efficient | Least Efficient |
|------|-----------|----------|----------------|-----------------|
| Task 1: Hello | 16 | Very High | Julia (6) | Assembly (85) |
| Task 2: Function | 21 | Very High | Ocaml (9) | Cobol (84) |
| Task 3: Fizzbuzz | 106 | Very High | Python (63) | Assembly (537) |
| Task 4: List | 59 | Very High | Sql (20) | Cobol (226) |
| Task 5: Class | 90 | Very High | Haskell (52) | Cobol (239) |
| Task 6: Fileio | 134 | Very High | Sql (21) | Cobol (288) |
| Task 7: Error | 63 | Very High | Kotlin (18) | Cobol (146) |
| Task 8: Http | 87 | Very High | Kotlin (31) | C (295) |

### Implications for LLM Applications

1. **Context Window Efficiency**: Using Python/Ruby over Java/C could reduce context usage by 60-200%
2. **Code Generation**: More token-efficient languages allow generating longer programs within output limits
3. **Code Understanding**: Concise languages require fewer tokens to represent equivalent semantics
4. **Multi-file Projects**: Token savings compound significantly across large codebases

### Recommendations by Use Case

| Use Case | Recommended Language | Rationale |
|----------|---------------------|-----------|
| General scripting | Python | Balance of efficiency and ecosystem |
| JVM projects | Kotlin | 2-3x more efficient than Java |
| Systems programming | Rust | 50%+ more efficient than C |
| Web development | JavaScript | Standard for web, reasonable efficiency |
| Data analysis | Julia or R | Domain-optimized, concise |
| Mobile apps | Swift/Kotlin | Modern, efficient alternatives |

## Conclusion

Among general-purpose languages with full task coverage, **Kotlin** emerges as the most token-efficient (317 tokens), followed closely by **Python** (327) and **Julia** (353).
 Python ranks #2 (327 tokens), making it a strong choice balancing efficiency with ecosystem support.

The least efficient languages are legacy systems (COBOL, Fortran) and C-family languages requiring explicit memory management or verbose type declarations.
 Java's verbosity results in 2.1x more tokens than Kotlin for equivalent functionality.


For LLM-based code generation and analysis, choosing token-efficient languages can significantly reduce costs and improve performance by maximizing the utility of context windows.
