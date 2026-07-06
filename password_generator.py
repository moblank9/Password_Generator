import random
import string
import math


def get_yes_no(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ('y', 'yes'):
            return True
        elif choice in ('n', 'no'):
            return False
        print("Please enter Y or N.")


def get_password_length():
    while True:
        try:
            length = int(input("Length: "))
            if length < 4:
                print("Password must be at least 4 characters long.")
            else:
                return length
        except ValueError:
            print("Please enter a valid number.")


def build_character_pool(use_upper, use_lower, use_numbers, use_symbols):
    pool = ''
    rules = []

    if use_upper:
        pool += string.ascii_uppercase
        rules.append('Uppercase')
    if use_lower:
        pool += string.ascii_lowercase
        rules.append('Lowercase')
    if use_numbers:
        pool += string.digits
        rules.append('Numbers')
    if use_symbols:
        pool += string.punctuation
        rules.append('Symbols')

    if not pool:
        print("You must include at least one character type. Defaulting to all.")
        return string.ascii_letters + string.digits + string.punctuation, [
            'Uppercase', 'Lowercase', 'Numbers', 'Symbols'
        ]

    return pool, rules


def generate_password(length, pool, use_upper, use_lower, use_numbers, use_symbols):
    password = []

    if use_upper:
        password.append(random.choice(string.ascii_uppercase))
    if use_lower:
        password.append(random.choice(string.ascii_lowercase))
    if use_numbers:
        password.append(random.choice(string.digits))
    if use_symbols:
        password.append(random.choice(string.punctuation))

    for _ in range(length - len(password)):
        password.append(random.choice(pool))

    random.shuffle(password)
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

    use_upper = get_yes_no("Include Uppercase? Y/N: ")
    use_lower = get_yes_no("Include Lowercase? Y/N: ")
    use_numbers = get_yes_no("Include Numbers? Y/N: ")
    use_symbols = get_yes_no("Include Symbols? Y/N: ")

    pool, rules = build_character_pool(use_upper, use_lower, use_numbers, use_symbols)

    password = generate_password(length, pool, use_upper, use_lower,
                                  use_numbers, use_symbols)

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
