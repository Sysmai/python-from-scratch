# This is a simple calculator that can add, subtract, multiply,
# and divide two numbers

# Basic calculator using loops, conditionals, and functions

def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    return x / y


while True:
    print("\nOptions: add, subtract, multiply, divide, quit")
    choice = input("Choose an operation: ").strip().lower()

    if choice == "quit":
        print("Exiting the calculator...")
        break

    if choice not in ["add", "subtract", "multiply", "divide"]:
        print("Invalid choice. Please try again.")
        continue

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Error: please enter numeric values.")
        continue

    if choice == "add":
        result = add(num1, num2)
    elif choice == "subtract":
        result = subtract(num1, num2)
    elif choice == "multiply":
        result = multiply(num1, num2)
    else:
        result = divide(num1, num2)

    print(f"Result: {result}")
