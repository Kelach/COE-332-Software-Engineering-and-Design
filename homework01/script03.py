from names import get_full_name
def ex3():
    for _ in range(5):
        name = get_full_name()
        print(f"Name: {name} Length: {len(name)-1}")



def main():
    print("\n\nExercise 3:")
    ex3()
    
main()
