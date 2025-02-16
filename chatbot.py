from utils import get_answer

if __name__ == "__main__":
    while True:
        user_input = input("Ask me a question: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        print(get_answer(user_input))
