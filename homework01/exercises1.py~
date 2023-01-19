from names import get_full_name, get_first_name

def ex1():
    words = []
    longest_word = ""
    
    with open("words.txt", "r") as filein:
        words = filein.read().splitlines()

    words.sort(key=len, reverse=True)
    print(words[:5])
    
def ex2():
    count = 0
    while count < 5:
        name = get_full_name()
        if len(name.strip()) == 8:
            print(name)
            count += 1

def ex3():
    for _ in range(5):
        name = get_full_name()
        print(f"Name: {name} Length: {name_length(name)}")

def name_length(name):
    return len(name.strip())


def main():
    print("\n\nExercise 1:")
    ex1()
    print("\n\nExercise 2:")
    ex2()
    print("\n\nExercise 3:")
    ex3()
    
main()
