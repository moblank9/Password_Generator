# Password_Generator # 
Password Generator & Strength Analyzer

A Python CLI tool that generates secure, customizable passwords and evaluates their strength using entropy estimation.

# Features

- Generate cryptographically random passwords of arbitrary length
- Choose which character types to include:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Symbols (!@#$%^&* etc.)
- Guarantees at least one character from each selected type
- Strength rating with visual star display (★☆☆☆☆ – ★★★★★)
- Entropy estimation in bits

# Requirements

- Python 3.6+

# Usage

```bash
python3 password_generator.py
```

Follow the interactive prompts:

```
==============================
   Password Generator
==============================

Length: 16
Include Uppercase? Y/N: y
Include Lowercase? Y/N: y
Include Numbers? Y/N: y
Include Symbols? Y/N: y

------------------------------
Generated Password:

  /bA8h4fusM({l3j[

Strength:  ★★★★★ Very Strong
Entropy:   104.9 bits
Length:    16 chars
Pool:      94 characters
Includes:  Uppercase, Lowercase, Numbers, Symbols
------------------------------
```

# Strength Tiers

| Entropy (bits) | Rating        | Stars |
|----------------|---------------|-------|
| < 28           | Weak          | ★☆☆☆☆ |
| 28 – 35        | Fair          | ★★☆☆☆ |
| 36 – 59        | Strong        | ★★★☆☆ |
| 60 – 79        | Very Strong   | ★★★★☆ |
| ≥ 80           | Very Strong   | ★★★★★ |

A password with ≥ 60 bits of entropy is considered resistant to brute-force attacks.

# How It Works

1. **Character pool** — builds a pool from the selected character types using Python's `string` module.
2. **Guaranteed placement** — one random character from each selected type is placed first, then the remaining slots are filled randomly from the full pool.
3. **Shuffle** — the final list is shuffled so the guaranteed characters aren't always at the start.
4. **Entropy** — calculated as `length × log₂(pool_size)`. Higher entropy = stronger password.
