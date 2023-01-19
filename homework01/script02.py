from names import get_full_name

def ex2():
    count = 0
    while count < 5:
        name = get_full_name()
        if len(name.strip()) == 8:
            print(name)
            count += 1

def main():
    print("\n\nExercise 2:")
    ex2()
main()
