def chatbot():
    print("Hi! I'm LongChatBot.")
    print("Type something to chat with me. Type 'bye' anytime to leave.\n")

    while True:
        user_input = input("You: ").lower()

        if user_input == "bye" or user_input == "exit" or user_input == "quit":
            print("Bot: Goodbye! It was fun chatting. 😊")
            break

        elif user_input == "hi" or user_input == "hello" or user_input == "hey":
            print("Bot: Hello! How are you doing today?")

        elif user_input == "how are you":
            print("Bot: I'm doing great, thanks for asking. What about you?")

        elif user_input == "i am fine":
            print("Bot: That's good to hear! What would you like to talk about?")

        elif user_input == "your name":
            print("Bot: My name is LongChatBot. I'm here to chat with you!")

        elif user_input == "help":
            print("Bot: You can ask me about my name, how I am, or just say hello!")

        elif user_input == "weather":
            print("Bot: I don't have access to weather data, but I hope it's nice where you are!")

        elif user_input == "what can you do":
            print("Bot: I can talk with you, answer simple questions, or just keep you company!")

        elif user_input == "tell me a joke":
            print("Bot: Why did the computer get cold? Because it left its Windows open! 😄")

        elif user_input == "what is going on" or user_input == "what's up":
            print("Bot: Just having a nice chat with you! How's your day going?")

        elif user_input == "how can i help you" or user_input == "how can i help":
            print("Bot: That's very kind of you! You can help me by having a nice conversation. What would you like to talk about?")

        elif user_input == "how you are doing" or user_input == "how are you doing":
            print("Bot: I'm doing well, thank you for asking! I'm always happy to chat with you. How about yourself?")

        else:
            print("Bot: Hmm, I didn't get that. Maybe try asking something else or type 'help'.")

# Run the chatbot
chatbot()
