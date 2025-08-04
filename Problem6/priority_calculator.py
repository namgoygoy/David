# 사칙연산 함수
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b

def divide(a, b):
    if b == 0:
        print("Error: Division by zero.")
        return None
    return a / b

# 계산 함수: 우선 *, / 먼저 계산, 그다음 +, -
def calculate(tokens):
    def compute(op_set):
        nonlocal tokens
        i = 0
        while i < len(tokens):
            if tokens[i] in op_set:
                a = float(tokens[i - 1])
                b = float(tokens[i + 1])
                if tokens[i] == '*': result = multiply(a, b)
                elif tokens[i] == '/': 
                    result = divide(a, b)
                    if result is None: return False
                elif tokens[i] == '+': result = add(a, b)
                elif tokens[i] == '-': result = subtract(a, b)
                # 계산한 결과로 대체
                tokens[i - 1:i + 2] = [str(result)]
                i = 0  # 다시 처음부터 탐색
            else:
                i += 1
        return True

    # 1순위: *, /
    if not compute({'*', '/'}): return None
    # 2순위: +, -
    if not compute({'+', '-'}): return None
    return float(tokens[0])

# 입력 받고 실행하는 메인 함수
def main():
    try:
        expr = input("Enter expression: ").strip().split()
        if len(expr) % 2 == 0:
            print("Invalid input.")
            return
        result = calculate(expr)
        if result is not None:
            print(f"Result: {result}")
    except:
        print("Invalid input.")

if __name__ == "__main__":
    main()
