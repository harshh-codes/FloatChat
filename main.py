# main.py
from chatbot.rag_pipeline import search_and_ask

if __name__ == "__main__":
    print("🌊 Argo Float Chatbot Ready!")
    while True:
        q = input("\nAsk a question (or type 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break
        answer = search_and_ask(q)
        print(f"\n🤖 {answer}")
