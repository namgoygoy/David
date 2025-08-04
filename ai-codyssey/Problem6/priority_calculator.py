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

def calculate(tokens):
    i = 0
    while i < len(tokens):
        if tokens[i] == '*':
            result = multiply(float(tokens[i-1]), float(tokens[i+1]))
            tokens[i-1:i+2] = [str(result)]
            i = 0  # 인덱스 초기화
        elif tokens[i] == '/':
            result = divide(float(tokens[i-1]), float(tokens[i+1]))
            if result is None:
                return None
            tokens[i-1:i+2] = [str(result)]
            i = 0
        else:
            i += 1

    i = 0
    while i < len(tokens):
        if tokens[i] == '+':
            result = add(float(tokens[i-1]), float(tokens[i+1]))
            tokens[i-1:i+2] = [str(result)]
            i = 0
        elif tokens[i] == '-':
            result = subtract(float(tokens[i-1]), float(tokens[i+1]))
            tokens[i-1:i+2] = [str(result)]
            i = 0
        else:
            i += 1

    return float(tokens[0])

def main():
    try:
        expression = input("Enter expression: ").strip()
        tokens = expression.split()

        if len(tokens) % 2 == 0:
            print("Invalid input.")
            return

        result = calculate(tokens)
        if result is not None:
            print(f"Result: {result}")

    except Exception:
        print("Invalid input.")

if __name__ == "__main__":
    main()
