from names import get_full_name, get_first_name

def ex1():
    words = []
    longest_word = ""
    
    with open("words.txt", "r") as filein:
        words = filein.read().splitlines()

    words.sort(key=len, reverse=True)
    print(words[:5])
def main():
    print("\n\nExercise 1:")
    ex1()

main()

