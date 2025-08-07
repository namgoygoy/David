def main():
    total = int(input())
    thing_type = int(input())
    result = 0

    for i in range(thing_type):
        price, count = map(int, input().split())
        result += price * count
    
    if total == result:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()