from chatbot.ollama_client import FloatChatbot

def test_chatbot():
    # Initialize the chatbot
    print("Initializing chatbot...")
    chatbot = FloatChatbot()
    
    # Test queries
    test_questions = [
        "What was the maximum temperature recorded in any profile?",
        "Tell me about the profiles from January 2000",
        "What's the typical depth range of these profiles?",
    ]
    
    print("\nTesting queries...\n")
    for question in test_questions:
        print(f"Question: {question}")
        print("-" * 80)
        response = chatbot.query(question)
        print(f"Response: {response}")
        print("-" * 80)
        print()

if __name__ == "__main__":
    test_chatbot()