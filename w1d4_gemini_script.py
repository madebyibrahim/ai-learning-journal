import os
import sys
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Load the environment variables from your secure .env file
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env file.")
        return
        
    # 2. Initialize the modern client
    client = genai.Client(api_key=api_key)

    history = []
    
    print("Chatbot Started! Type /exit or /quit to end the conversation.\n")

    while True: 
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.startswith("/"):
            command = user_input.lower()
            if command in ["/quit", "/exit"]:
                print("Goodbye!")
                break
            else:
                print(f"Unknown command: {user_input}. Type /exit to quit")
                continue
        
        history.append({
            "role":"user",
            "parts": [{"text": user_input}]
        })

        try:
            print("Gemini: ", end="", flush=True)
            response_stream = client.models.generate_content_stream(
                model="gemini-3.5-flash",
                contents=history,
            )

            full_response = ""

            for chunk in response_stream:
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
            print("\n")

            history.append({
                "role": "model",
                "parts": [{"text": full_response}]
            })
 
        except Exception as e:
            print(f"\n\nAn error occurred: {e}")

if __name__ == "__main__":
    main()