from app.core.assistant import assistant_response


def main():
    print("AI Mental Health Assistant")
    print("Type 'exit' to stop.\n")

    while True:
        message = input("You: ")

        if message.lower() == "exit":
            print("Goodbye!")
            break

        response = assistant_response(message)

        print("\nAssistant:")
        print(response)
        print()


if __name__ == "__main__":
    main()