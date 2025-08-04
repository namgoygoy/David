def main():
    try:
        inputs = input("").split().split()
        numbers = [float(x) for x in inputs]
    except ValueError:
        print("")
        return