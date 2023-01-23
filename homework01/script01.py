def ex1():
    words = []
    longest_word = ""
    
    with open("/usr/share/dict/words", "r") as filein:
        content = filein.readlines()
        words = [line.strip() for line in content]        

    words.sort(key=len, reverse=True)
    print(words[:5])
def main():
    print("\n\nExercise 1:")
    ex1()

main()

