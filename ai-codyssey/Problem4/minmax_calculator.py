def main():
    try:
        numbers = input("Enter numbers separated by space: ").split()
        floats = [float(n) for n in numbers]

        min_value = floats[0]
        max_value = floats[0]

        for num in floats[1:]:
            # 인덱스 1 부터 끝까지 처리 예를 들어 [10, 20] 이면 인덱스 1은 10 인덱스 2는 20
            if num < min_value:
                min_value = num
            if num > max_value:
                max_value = num

        print(f"Min: {min_value}, Max: {max_value}")

    except ValueError:
        print("Invalid input.")

if __name__ == "__main__":
    main()
