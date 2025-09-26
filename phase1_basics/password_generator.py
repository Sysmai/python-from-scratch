"""
This is a simple password generator
"""

import math  # for math.functions
import string  # for the character pool
import secrets  # for the random choice


# Constant for ambiguous characters
CONFUSING = set("O0ol1|`'\\\"")


def secure_shuffle(chars: list[str]) -> None:
    """Shuffle a list in a secure way"""
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]


def estimate_entropy(length: int, pool_size: int) -> float:
    """Estimate the entropy of a password"""
    if length <= 0 or pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)


def strength_label(bits: float) -> str:
    """Return a label for the strength of a password"""
    if bits < 28:
        return "weak"
    if bits < 56:
        return "moderate"
    if bits < 80:
        return "strong"
    return "very strong"


def generate_password(
    length=12,
    use_digits=True,
    use_symbols=True,
    avoid_confusing=False,
    enforce_requirements=False,
):
    """
    Generate a random password
    """
    pool = string.ascii_letters
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation
    if avoid_confusing:
        pool = "".join(ch for ch in pool if ch not in CONFUSING)

    if not pool:
        raise ValueError("Character pool is empty")

    if enforce_requirements:
        # ensure at least one of each selected type
        required = []
        if use_digits:
            digits_pool = (
                "".join(ch for ch in string.digits if ch not in CONFUSING)
                if avoid_confusing
                else string.digits
            )
            if digits_pool:
                required.append(secrets.choice(digits_pool))
        if use_symbols:
            symbols_pool = (
                "".join(ch for ch in string.punctuation if ch not in CONFUSING)
                if avoid_confusing
                else string.punctuation
            )
            if symbols_pool:
                required.append(secrets.choice(symbols_pool))
        if len(required) > length:
            raise ValueError(
                "Password length is too short to meet requirements"
                )
        password_chars = required + [
            secrets.choice(pool) for _ in range(length - len(required))
        ]
        secure_shuffle(password_chars)
        return "".join(password_chars)
    else:
        return "".join(secrets.choice(pool) for _ in range(length))


def ask_int(prompt: str, minimum: int = 4, maximum: int = 128) -> int:
    """Ask the user for an integer in a range. Reprompt until valid."""
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Please enter a whole number.")
            continue
        value = int(raw)
        if value < minimum:
            print(f"Please enter a number at least {minimum}.")
            continue
        if value > maximum:
            print(f"Please enter a number no greater than {maximum}.")
            continue
        return value


def ask_bool(prompt: str) -> bool:
    """Ask a yes/no question. Accepts y/n or yes/no. Re-prompt until valid."""
    while True:
        raw = input(prompt + " [y/n]").strip().lower()
        if raw == "y" or raw == "yes":
            return True
        if raw == "n" or raw == "no":
            return False
        print("Please enter y/n or yes/no.")


def main():
    print("=== Password Generator ===")
    length = ask_int("Length (4-128): ", minimum=4, maximum=128)
    use_digits = ask_bool("Include digits 0-9?")
    use_symbols = ask_bool("Include symbols?")
    enforce = ask_bool("Enforce at least one of each selected type?")
    avoid_confusing = ask_bool("Avoid confusing characters like O0Ol1|`'\\\"?")

    password = generate_password(
        length=length,
        use_digits=use_digits,
        use_symbols=use_symbols,
        enforce_requirements=enforce,
        avoid_confusing=avoid_confusing,
    )

    # strength estimate
    pool = "".join(
        ch
        for ch in (
            string.ascii_letters
            + (string.digits if use_digits else "")
            + (string.punctuation if use_symbols else "")
        )
        if not (avoid_confusing and ch in CONFUSING)
    )
    pool_size = len(pool)
    bits = estimate_entropy(length, pool_size)

    print("\nYour password:")
    print(password)
    print(
        f"\nEstimated strength: {strength_label(bits)} ({bits:.1f} bits) "
        f"from pool {pool_size} x length {length}"
    )


if __name__ == "__main__":
    main()
