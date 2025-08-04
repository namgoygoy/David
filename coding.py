# 최대 최소, 정렬

def sort(numbers):
    num = len(numbers)

    for i in range(num):
        for j in range(num - i - 1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers

def main():
    try:
        inputs  = input("").strip().split()
        floats = [float(x) for x in inputs]
        # result = sort(inputs)
        result = sort(float)
        print("sotred", ' '.join(map(str, result))) 
    except:
        print("잘못된 입력")
        return

if __name__ == "__main__":
    main()