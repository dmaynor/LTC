# Token Efficiency Benchmark Results

*Comparing token counts across 29 programming languages using BPE-style tokenization*

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

### Tokenization Approach
Uses BPE-style tokenization approximating cl100k_base encoding behavior:
- Identifiers split on camelCase/snake_case boundaries
- Common short words (≤4 chars) as single tokens
- Strings tokenized at ~4 chars/token
- Whitespace/indentation patterns tokenized

## Summary Table

| Rank | Language | Total Tokens | Chars/Token | Tokens/Line | Tasks |
|------|----------|--------------|-------------|-------------|-------|
| 1 | sql | 56 | 2.55 | 8.0 | 2 |
| 2 | sas | 105 | 2.61 | 6.18 | 3 |
| 3 | prolog | 283 | 2.12 | 11.79 | 5 |
| 4 | kotlin | 456 | 2.41 | 11.12 | 8 |
| 5 | ruby | 460 | 2.33 | 8.21 | 8 |
| 6 | julia | 461 | 2.44 | 8.23 | 8 |
| 7 | python | 491 | 2.41 | 10.67 | 8 |
| 8 | r | 580 | 2.23 | 11.15 | 8 |
| 9 | assembly | 606 | 2.67 | 4.93 | 3 |
| 10 | lua | 621 | 2.56 | 9.13 | 8 |
| 11 | swift | 621 | 2.49 | 11.09 | 8 |
| 12 | matlab | 623 | 2.45 | 9.03 | 8 |
| 13 | perl | 638 | 2.25 | 9.38 | 8 |
| 14 | javascript | 658 | 2.31 | 10.97 | 8 |
| 15 | dart | 663 | 2.22 | 10.36 | 8 |
| 16 | php | 668 | 2.39 | 10.95 | 8 |
| 17 | rust | 678 | 2.24 | 10.76 | 8 |
| 18 | csharp | 706 | 2.35 | 9.94 | 8 |
| 19 | go | 790 | 2.18 | 6.64 | 8 |
| 20 | classicvb | 831 | 2.78 | 9.44 | 8 |
| 21 | visualbasic | 892 | 2.75 | 10.62 | 8 |
| 22 | cpp | 1039 | 2.47 | 9.11 | 8 |
| 23 | ada | 1172 | 2.61 | 10.37 | 8 |
| 24 | fortran | 1188 | 2.63 | 10.07 | 8 |
| 25 | objectivec | 1214 | 2.46 | 11.45 | 8 |
| 26 | java | 1224 | 2.55 | 11.55 | 8 |
| 27 | delphi | 1269 | 2.35 | 7.98 | 8 |
| 28 | c | 1479 | 2.4 | 9.48 | 8 |
| 29 | cobol | 1784 | 2.72 | 12.39 | 8 |

## Normalized Comparison (8-Task Languages Only)

For fair comparison, considering only languages with all 8 tasks:

| Rank | Language | Total Tokens | Efficiency vs Python |
|------|----------|--------------|---------------------|
| 1 | kotlin | 456 | 7.1% more efficient |
| 2 | ruby | 460 | 6.3% more efficient |
| 3 | julia | 461 | 6.1% more efficient |
| 4 | python | 491 | baseline |
| 5 | lua | 621 | 26.5% less efficient |
| 6 | swift | 621 | 26.5% less efficient |
| 7 | matlab | 623 | 26.9% less efficient |
| 8 | perl | 638 | 29.9% less efficient |
| 9 | javascript | 658 | 34.0% less efficient |
| 10 | dart | 663 | 35.0% less efficient |
| 11 | php | 668 | 36.0% less efficient |
| 12 | rust | 678 | 38.1% less efficient |
| 13 | csharp | 706 | 43.8% less efficient |
| 14 | go | 790 | 60.9% less efficient |
| 15 | classicvb | 831 | 69.2% less efficient |
| 16 | visualbasic | 892 | 81.7% less efficient |
| 17 | cpp | 1039 | 111.6% less efficient |
| 18 | ada | 1172 | 138.7% less efficient |
| 19 | fortran | 1188 | 141.9% less efficient |
| 20 | objectivec | 1214 | 147.3% less efficient |
| 21 | java | 1224 | 149.3% less efficient |
| 22 | delphi | 1269 | 158.5% less efficient |
| 23 | c | 1479 | 201.2% less efficient |
| 24 | cobol | 1784 | 263.3% less efficient |

## Per-Task Breakdown

### task1_hello

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | ruby | 6 |
| 2 | matlab | 8 |
| 3 | julia | 9 |
| 4 | lua | 9 |
| 5 | python | 9 |
| 6 | r | 9 |
| 7 | swift | 9 |
| 8 | javascript | 12 |
| 9 | php | 12 |
| 10 | csharp | 14 |
| 11 | sas | 15 |
| 12 | classicvb | 16 |
| 13 | kotlin | 18 |
| 14 | perl | 18 |
| 15 | dart | 19 |
| 16 | rust | 20 |
| 17 | fortran | 21 |
| 18 | delphi | 24 |
| 19 | prolog | 27 |
| 20 | go | 30 |
| 21 | visualbasic | 34 |
| 22 | c | 37 |
| 23 | cpp | 38 |
| 24 | ada | 39 |
| 25 | java | 46 |
| 26 | cobol | 48 |
| 27 | objectivec | 54 |
| 28 | assembly | 84 |

### task2_function

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | julia | 12 |
| 2 | csharp | 16 |
| 3 | dart | 16 |
| 4 | ruby | 16 |
| 5 | kotlin | 17 |
| 6 | python | 17 |
| 7 | prolog | 18 |
| 8 | lua | 19 |
| 9 | r | 20 |
| 10 | javascript | 21 |
| 11 | c | 22 |
| 12 | cpp | 22 |
| 13 | matlab | 22 |
| 14 | objectivec | 22 |
| 15 | rust | 23 |
| 16 | swift | 23 |
| 17 | go | 26 |
| 18 | php | 29 |
| 19 | assembly | 30 |
| 20 | classicvb | 30 |
| 21 | perl | 30 |
| 22 | ada | 33 |
| 23 | delphi | 33 |
| 24 | java | 38 |
| 25 | visualbasic | 41 |
| 26 | fortran | 47 |
| 27 | cobol | 117 |

### task3_fizzbuzz

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | ruby | 64 |
| 2 | julia | 75 |
| 3 | kotlin | 77 |
| 4 | python | 77 |
| 5 | lua | 79 |
| 6 | swift | 79 |
| 7 | matlab | 80 |
| 8 | r | 90 |
| 9 | php | 91 |
| 10 | prolog | 91 |
| 11 | javascript | 102 |
| 12 | perl | 103 |
| 13 | rust | 105 |
| 14 | csharp | 108 |
| 15 | delphi | 110 |
| 16 | classicvb | 111 |
| 17 | dart | 111 |
| 18 | go | 114 |
| 19 | fortran | 123 |
| 20 | c | 131 |
| 21 | visualbasic | 139 |
| 22 | cpp | 140 |
| 23 | ada | 154 |
| 24 | objectivec | 158 |
| 25 | java | 160 |
| 26 | cobol | 283 |
| 27 | assembly | 492 |

### task4_list

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | sql | 23 |
| 2 | julia | 27 |
| 3 | python | 32 |
| 4 | kotlin | 36 |
| 5 | sas | 36 |
| 6 | ruby | 39 |
| 7 | r | 40 |
| 8 | perl | 41 |
| 9 | javascript | 44 |
| 10 | swift | 45 |
| 11 | matlab | 46 |
| 12 | dart | 54 |
| 13 | csharp | 60 |
| 14 | rust | 61 |
| 15 | php | 68 |
| 16 | prolog | 72 |
| 17 | lua | 76 |
| 18 | go | 85 |
| 19 | visualbasic | 89 |
| 20 | cpp | 105 |
| 21 | classicvb | 108 |
| 22 | java | 122 |
| 23 | objectivec | 124 |
| 24 | fortran | 134 |
| 25 | ada | 154 |
| 26 | c | 170 |
| 27 | delphi | 183 |
| 28 | cobol | 274 |

### task5_class

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | julia | 74 |
| 2 | prolog | 75 |
| 3 | swift | 90 |
| 4 | python | 91 |
| 5 | classicvb | 92 |
| 6 | kotlin | 92 |
| 7 | ruby | 95 |
| 8 | dart | 98 |
| 9 | javascript | 105 |
| 10 | lua | 112 |
| 11 | go | 124 |
| 12 | php | 125 |
| 13 | cpp | 126 |
| 14 | r | 128 |
| 15 | rust | 128 |
| 16 | java | 135 |
| 17 | c | 136 |
| 18 | matlab | 136 |
| 19 | perl | 141 |
| 20 | visualbasic | 142 |
| 21 | csharp | 145 |
| 22 | fortran | 153 |
| 23 | ada | 172 |
| 24 | delphi | 232 |
| 25 | objectivec | 241 |
| 26 | cobol | 287 |

### task6_fileio

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | sql | 33 |
| 2 | sas | 54 |
| 3 | r | 101 |
| 4 | ruby | 102 |
| 5 | python | 112 |
| 6 | perl | 130 |
| 7 | julia | 133 |
| 8 | kotlin | 135 |
| 9 | matlab | 143 |
| 10 | php | 151 |
| 11 | csharp | 156 |
| 12 | lua | 159 |
| 13 | cpp | 166 |
| 14 | swift | 177 |
| 15 | dart | 178 |
| 16 | visualbasic | 186 |
| 17 | javascript | 188 |
| 18 | rust | 209 |
| 19 | go | 242 |
| 20 | objectivec | 265 |
| 21 | classicvb | 275 |
| 22 | java | 317 |
| 23 | delphi | 332 |
| 24 | fortran | 364 |
| 25 | ada | 373 |
| 26 | c | 392 |
| 27 | cobol | 405 |

### task7_error

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | kotlin | 30 |
| 2 | go | 42 |
| 3 | rust | 51 |
| 4 | python | 52 |
| 5 | ruby | 54 |
| 6 | julia | 59 |
| 7 | lua | 78 |
| 8 | csharp | 79 |
| 9 | classicvb | 81 |
| 10 | dart | 82 |
| 11 | perl | 83 |
| 12 | javascript | 86 |
| 13 | swift | 94 |
| 14 | php | 99 |
| 15 | visualbasic | 112 |
| 16 | r | 114 |
| 17 | ada | 118 |
| 18 | matlab | 120 |
| 19 | delphi | 130 |
| 20 | objectivec | 138 |
| 21 | cpp | 141 |
| 22 | java | 151 |
| 23 | c | 165 |
| 24 | fortran | 174 |
| 25 | cobol | 198 |

### task8_http

| Rank | Language | Tokens |
|------|----------|--------|
| 1 | kotlin | 51 |
| 2 | matlab | 68 |
| 3 | julia | 72 |
| 4 | r | 78 |
| 5 | rust | 81 |
| 6 | ruby | 84 |
| 7 | lua | 89 |
| 8 | perl | 92 |
| 9 | php | 93 |
| 10 | javascript | 100 |
| 11 | python | 101 |
| 12 | swift | 104 |
| 13 | dart | 105 |
| 14 | classicvb | 118 |
| 15 | go | 127 |
| 16 | csharp | 128 |
| 17 | ada | 129 |
| 18 | visualbasic | 149 |
| 19 | cobol | 172 |
| 20 | fortran | 172 |
| 21 | objectivec | 212 |
| 22 | delphi | 225 |
| 23 | java | 255 |
| 24 | cpp | 301 |
| 25 | c | 426 |

## Analysis

### Key Findings

#### Most Token-Efficient Languages (All 8 Tasks)

1. **Kotlin** (456 tokens) - Concise syntax, type inference, extension functions
2. **Ruby** (460 tokens) - Minimal boilerplate, expressive blocks
3. **Julia** (461 tokens) - Mathematical notation, clean syntax
4. **Python** (491 tokens) - Readable, minimal punctuation
5. **Lua** (621 tokens) - Simple semantics, lightweight syntax

#### Least Token-Efficient Languages

1. **COBOL** (1784 tokens) - Verbose English-like syntax, required divisions
2. **C** (1479 tokens) - Manual memory management, explicit typing
3. **Delphi** (1269 tokens) - Pascal heritage, verbose declarations
4. **Java** (1224 tokens) - Verbose class structure, explicit types
5. **Objective-C** (1214 tokens) - Message-passing syntax overhead

### Language Family Patterns

| Family | Avg Tokens | Representative Languages |
|--------|------------|-------------------------|
| Dynamic Scripting | ~520 | Python, Ruby, Julia, Lua |
| Modern JVM | ~840 | Kotlin, Java |
| Modern Systems | ~734 | Rust, Go, Swift |
| C-Family | ~1243 | C, C++, Objective-C |
| Legacy Enterprise | ~1486 | COBOL, Fortran, Ada |
| Visual Basic | ~862 | VB.NET, Classic VB |

### Task Complexity Impact

| Task | Avg Tokens | Variance | Most Efficient | Least Efficient |
|------|-----------|----------|----------------|-----------------|
| Hello World | 27 | High | Ruby (6) | Assembly (84) |
| Function | 30 | Medium | Julia (12) | COBOL (117) |
| FizzBuzz | 121 | High | Ruby (64) | Assembly (492) |
| List Ops | 86 | High | SQL (23) | COBOL (274) |
| Class | 134 | High | Julia (74) | COBOL (287) |
| File I/O | 209 | Very High | SQL (33) | COBOL (405) |
| Error Handling | 102 | High | Kotlin (30) | COBOL (198) |
| HTTP | 137 | Very High | Kotlin (51) | C (426) |

### Implications for LLM Applications

1. **Context Window Efficiency**: Using Kotlin/Ruby/Python over Java/C could reduce context usage by 60-200%
2. **Code Generation**: More token-efficient languages allow generating longer programs within output limits
3. **Code Understanding**: Concise languages require fewer tokens to represent equivalent semantics
4. **Multi-file Projects**: Token savings compound significantly across large codebases

### Recommendations by Use Case

| Use Case | Recommended Language | Rationale |
|----------|---------------------|-----------|
| General scripting | Python | Balance of efficiency and ecosystem |
| JVM projects | Kotlin | 2.7x more efficient than Java |
| Systems programming | Rust | 54% more efficient than C |
| Web development | JavaScript | Standard for web, reasonable efficiency |
| Data analysis | Julia or R | Domain-optimized, concise |
| Mobile apps | Swift/Kotlin | Modern, efficient alternatives |

## Conclusion

Among general-purpose languages with full task coverage, **Kotlin** emerges as the most token-efficient (456 tokens), followed closely by **Ruby** (460) and **Julia** (461). Python ranks 4th (491 tokens), making it a strong choice balancing efficiency with ecosystem support.

The least efficient languages are legacy systems (COBOL, Fortran) and C-family languages requiring explicit memory management or verbose type declarations. Java's verbosity results in 2.7x more tokens than Kotlin for equivalent functionality.

For LLM-based code generation and analysis, choosing token-efficient languages can significantly reduce costs and improve performance by maximizing the utility of context windows.
