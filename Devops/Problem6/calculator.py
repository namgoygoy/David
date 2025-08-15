def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        print("Error: Division by zero.")
        return None
    return a / b

def evaluate_expression(expression):
    try:
        tokens = expression.strip().split()
        if len(tokens) != 3:
            print("Invalid input format. Use: number operator number (e.g., 2 + 3)")
            return

        a = int(tokens[0])
        op = tokens[1]
        b = int(tokens[2])

        if op == '+':
            return add(a, b)
        elif op == '-':
            return subtract(a, b)
        elif op == '*':
            return multiply(a, b)
        elif op == '/':
            return divide(a, b)
        else:
            print("Invalid operator.")
            return
    except ValueError:
        print("Invalid number input.")
        return

     
if __name__ == "__main__":
    expression = input("Enter expression (e.g., 2 + 3): ")
    result = evaluate_expression(expression)
    if result is not None:
        print(f"Result: {result}")
