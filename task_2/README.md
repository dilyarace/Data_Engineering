# Task 2 — SHA3-256 File Hashing

An internship assignment focused on cryptographic hashing, binary file processing, custom sorting, and Python automation.

## Problem Statement

Given 256 binary files, the goal was to:

1. Compute the SHA3-256 hash of each file
2. Represent each hash as 64 lowercase hex characters
3. Sort the hashes in ascending order by a custom key: the product of `(hex_digit + 1)` across all 64 characters of the hash
4. Concatenate the sorted hashes into a single string with no separator
5. Append an email address to the end of the string
6. Compute the SHA3-256 of the final string — this is the answer


## What I Learned

### Hash Functions

A hash function takes any input (a file, a string, any data) and produces a fixed-length output. Think of it as a unique fingerprint for a file:

- The same file always produces the same hash
- Changing even a single byte produces a completely different hash
- The original file cannot be reconstructed from its hash

**SHA3-256** is a specific hashing algorithm that always outputs 64 hex characters.

> Note: SHA3-256 and SHA-256 are **different algorithms** and produce different results for the same input.

A reliable way to verify you are using the right algorithm is the **empty string test vector** — SHA3-256 of an empty string must always return:
```
a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
```

### Binary File Reading

Files can be opened as text or as raw binary. For hashing, raw bytes are required — reading as text would let the encoding layer transform the bytes, producing a different byte sequence and therefore a wrong hash. In Python, binary mode is specified with `"rb"`:

```python
with open(path, "rb") as f:
    data = f.read()
```

### Hexadecimal (Hex)

Hash output is written in hexadecimal — a base-16 number system using digits `0–9` and letters `a–f`:

```
"a" = 10,  "b" = 11,  "c" = 12,  "d" = 13,  "e" = 14,  "f" = 15
```

In Python, converting a hex character to an integer: `int("a", 16)` → `10`

### Custom Sort Key

A sort key is a value computed from each item that determines the sort order. The key itself is never part of the final output — it only controls the ordering.

In this task, the sort key for each hash is defined as the product of `(digit + 1)` for all 64 characters:

```
Hash: "3a2..."
"3" → 3 + 1 = 4
"a" → 10 + 1 = 11
"2" → 2 + 1 = 3
Key = 4 × 11 × 3 × ... (repeated for all 64 characters)
```

Adding 1 prevents the product from becoming zero when a character is `"0"`.


## Pipeline Overview

```
256 binary files
       │
       ▼  SHA3-256 per file
256 hashes (64 hex chars each)
       │
       ▼  compute sort key for each hash
sort hashes by key (ascending)
       │
       ▼  concatenate without separator
single string (16,384 characters)
       │
       ▼  append email
single string (16,384 + len(email) characters)
       │
       ▼  SHA3-256
64 hex characters — final answer
```


## Common Pitfalls

| Mistake | Why it matters |
|---|---|
| Using SHA-256 instead of SHA3-256 | Different algorithms produce different results |
| Reading files as text instead of binary | Encoding transforms the bytes — wrong hash |
| Adding a separator between hashes | Changes the string — changes the final hash |
| Email with uppercase letters | `Dilya@...` ≠ `dilya@...` |
| Processing more than 256 files | Hidden files like `.DS_Store` on macOS can sneak in |


## Stack

- **Language:** Python 3
- **Libraries:** `hashlib` (built-in), `os` (built-in) — no external dependencies
