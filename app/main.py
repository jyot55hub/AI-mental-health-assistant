from app.core.assistant import assistant_response


def main():
    print("=" * 60)
    print("AI MENTAL HEALTH ASSISTANT")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        user_message = input("\nYou: ").strip()

        if user_message.lower() in ["exit", "quit"]:
            print("\nAssistant: Take care of yourself. Goodbye!")
            break

        if not user_message:
            print("Assistant: Please enter a message.")
            continue

        try:
            response = assistant_response(user_message)
            print(f"\nAssistant: {response}")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()