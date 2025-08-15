from calculator import add, subtract, multiply, divide

def precedence(op):
    if op in ('+', '-'):
        return 1
    elif op in ('*', '/'):
        return 2
    return 0

def apply_operator(operators, values):
    right = values.pop()
    left = values.pop()
    op = operators.pop()
    
    if op == '+':
        values.append(add(left, right))
    elif op == '-':
        values.append(subtract(left, right))
    elif op == '*':
        values.append(multiply(left, right))
    elif op == '/':
        result = divide(left, right)
        if result is None:
            raise ValueError("Division by zero")
        values.append(result)

def evaluate_expression(tokens):
    values = []
    operators = []
    i = 0

    while i < len(tokens):
        token = tokens[i]
        if token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop() 
        elif token in '+-*/':
            while (operators and operators[-1] != '(' and
                   precedence(operators[-1]) >= precedence(token)):
                apply_operator(operators, values)
            operators.append(token)
        else:
            try:
                values.append(float(token))
            except:
                raise ValueError("Invalid number")
        i += 1

    while operators:
        apply_operator(operators, values)

    return values[0]

def main():
    try:
        expression = input("Enter expression: ").strip()
        tokens = expression.split()

        result = evaluate_expression(tokens)
        print(f"Result: {result}")
    except Exception as e:
        print("Invalid input.")

if __name__ == "__main__":
    main()


# 스택을 사용하는 이유 단순히 왼쪽부터 계산하면 3 + 5 = 8 후 8 * 2 = 16 ❌ 틀림
# 스택을 이용하면, 연산자 우선순위를 보고 *가 +보다 높으므로 5 * 2를 먼저 계산  