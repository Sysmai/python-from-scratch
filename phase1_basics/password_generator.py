"""
This is a simple password generator
"""

import string  # for the character pool
import secrets  # for the random choice


def generate_password(length=12, use_digits=True, use_symbols=True):
    """
    Generate a random password
    """
    pool = string.ascii_letters
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    if not pool:
        raise ValueError("Character pool is empty")

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

    #  Ensure at least one category beyond letters is user chose none
    if not use_digits and not use_symbols:
        print("Generating with letters only.")
    password = generate_password(length=length, use_digits=use_digits,
                                 use_symbols=use_symbols)
    print("\nYour password:")
    print(password)


if __name__ == "__main__":
    main()
