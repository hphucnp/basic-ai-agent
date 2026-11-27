from agent import run_agent


def main():
    while True:
        question = input("Customer: ")

        if question.lower() == "exit":
            break

        answer = run_agent(question)

        print(f"Agent: {answer}")


if __name__ == "__main__":
    main()