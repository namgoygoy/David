def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers

def main():
    try:
        inputs = input("Enter numbers separated by space: ").strip().split()
        numbers = [float(x) for x in inputs]
    except ValueError:
        print("Invalid input.")
        return

    sorted_numbers = bubble_sort(numbers)
    print("Sorted:", ' '.join(map(str, sorted_numbers)))
    # map str은 각 숫자를 문자열로 변환 ' '.join 리스트안의 문자열을 하나의 문자열로 만듬

if __name__ == "__main__":
    main()
