import secrets
import string
import math

# Single source of truth for character categories.
# Add/remove entries here and both pool-building and generation stay in sync.
CATEGORIES = {
    'Uppercase': string.ascii_uppercase,
    'Lowercase': string.ascii_lowercase,
    'Numbers':   string.digits,
    'Symbols':   string.punctuation,
}


def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        print("Please enter Y or N.")


def get_password_length(min_length=4):
    while True:
        try:
            length = int(input("Length: "))
            if length < min_length:
                print(f"Password must be at least {min_length} characters long.")
            else:
                return length
        except ValueError:
            print("Please enter a valid number.")


def secure_shuffle(seq):
    """Fisher-Yates shuffle using the `secrets` module (random.shuffle is not
    cryptographically secure, so we can't use it here)."""
    seq = list(seq)
    for i in reversed(range(1, len(seq))):
        j = secrets.randbelow(i + 1)
        seq[i], seq[j] = seq[j], seq[i]
    return seq


def build_character_pool(selected):
    """selected: dict like {'Uppercase': True, 'Lowercase': False, ...}"""
    rules = [name for name, enabled in selected.items() if enabled]
    pool = ''.join(CATEGORIES[name] for name in rules)

    if not pool:
        print("You must include at least one character type. Defaulting to all.")
        rules = list(CATEGORIES.keys())
        pool = ''.join(CATEGORIES.values())

    return pool, rules


def generate_password(length, pool, rules):
    # Guarantee at least one character from each selected category.
    password = [secrets.choice(CATEGORIES[name]) for name in rules]

    if length < len(password):
        raise ValueError(
            f"Length ({length}) is too short for the selected character "
            f"types ({len(password)} categories require at least {len(password)} characters)."
        )

    # Fill the remaining slots from the full pool.
    remaining = length - len(password)
    password.extend(secrets.choice(pool) for _ in range(remaining))

    password = secure_shuffle(password)
    return ''.join(password)


def estimate_entropy(length, pool_size):
    return length * math.log2(pool_size)


def assess_strength(length, pool_size):
    entropy = estimate_entropy(length, pool_size)
    if entropy < 28:
        return 'Weak', 1
    elif entropy < 36:
        return 'Fair', 2
    elif entropy < 60:
        return 'Strong', 3
    elif entropy < 80:
        return 'Very Strong', 4
    else:
        return 'Very Strong', 5


def print_banner():
    print("=" * 30)
    print("   Password Generator")
    print("=" * 30)
    print()


def main():
    print_banner()
    length = get_password_length()

    selected = {
        'Uppercase': get_yes_no("Include Uppercase? Y/N: "),
        'Lowercase': get_yes_no("Include Lowercase? Y/N: "),
        'Numbers':   get_yes_no("Include Numbers? Y/N: "),
        'Symbols':   get_yes_no("Include Symbols? Y/N: "),
    }

    pool, rules = build_character_pool(selected)
    password = generate_password(length, pool, rules)

    pool_size = len(set(pool))
    entropy = estimate_entropy(length, pool_size)
    label, stars = assess_strength(length, pool_size)

    print()
    print("-" * 30)
    print("Generated Password:")
    print()
    print(f"  {password}")
    print()
    print(f"Strength:  {'★' * stars}{'☆' * (5 - stars)} {label}")
    print(f"Entropy:   {entropy:.1f} bits")
    print(f"Length:    {len(password)} chars")
    print(f"Pool:      {pool_size} characters")
    print(f"Includes:  {', '.join(rules)}")
    print("-" * 30)
    print()


if __name__ == '__main__':
    main()