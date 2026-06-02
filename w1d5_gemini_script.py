import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Constants
AVAILABLE_MODELS = [
    "gemini-3.1-flash-lite",        # 500/day
    "gemini-3.5-flash",             # 20/day
    "gemini-2.5-flash",             # 20/day
    "gemini-2.5-flash-lite",        # 20/day
]

def print_model_menu():
    print("\n----- Available Models -----")
    for idx, model_name in enumerate(AVAILABLE_MODELS, 1):
        print(f"[{idx}] {model_name}")
    print("----------------------------\n")

def print_help_menu():
    print("\n----- CLI Control Panel Commands -----")
    print("    /help : Show this help menu")
    print("    /status : Show the current active configuration")
    print("    /temp <0.0 - 2.0> : Adjust creativity (low = factual, high = creative)")
    print("    /max <integer> : Limit maximum output tokens")
    print("    /model <model_name> : Configure active model")
    print("    /exit or /quit : End the session")
    print("--------------------------------------\n")

def main():
    current_model="gemini-3.1-flash-lite" # define model
    temperature=0.7 #define creativity (0-2.0)
    max_output_tokens=2048 # limit output tokens

    # 1. Load the environment variables from your secure .env file
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env file.")
        return 
    
    # 2. Initialize the modern client
    client = genai.Client(api_key=api_key)

    history = []
    
    print("Chatbot Started! Type /help to get the help message.")
    print_help_menu()

    while True: 
        user_input = input("You: ").strip()

        if not user_input:
            continue

        elif user_input.startswith("/"):
            parts = user_input.split()
            command = parts[0].lower()

            if command in ["/quit", "/exit"]:
                print("\nGemini: Goodbye!")
                break

            elif command == "/status":
                print("\n---------- System Information ----------")
                print(f"    Model               : {current_model}")
                print(f"    Temperature         : {temperature}")
                print(f"    Max Output Tokens   : {max_output_tokens}")
                print(f"    History Length      : {len(history)} entries")
                print("----------------------------------------\n")
                continue

            elif command == "/temp":
                if len(parts) < 2:
                    print("\nSystem: Please provide a value for temperature between 0.0 and 2.0\n")
                    continue
                try:
                    val = float(parts[1])
                    if 0 <= val <= 2:
                        temperature = val
                        print(f"\nSystem Success: Temperature is set to {temperature}.\n")
                    else:
                        print("\nSystem Error: Temperature value must be between 0 and 2.0 (inclusive).\n")
                except ValueError:
                    print("\nSystem Error: Temperature must be a number.\n")
                continue
            
            elif command == "/max":
                if len(parts) < 2:
                    print("\nPlease provide a maximum output token value.\n")
                    continue
                try:
                    val = int(parts[1])
                    if val > 0:
                        max_output_tokens = val
                        print(f"\nSystem Success: Maximum Output Tokens value set to {max_output_tokens}.\n")
                    else:
                        print("\nSystem Error: Please provide a positive integer value for Maximum Output Tokens.\n")
                except ValueError:
                    print("\nSystem Error: Maximum Output Tokens must be a positive integer.\n")
                continue
            
            elif command == "/model":
                if len(parts)<2:
                    print("\nPlease provide a positive integer for the model to use. (e.g. /model 4)")
                    print_model_menu()
                    continue
                try:
                    selection = int(parts[1])
                    if selection < 1 or selection > len(AVAILABLE_MODELS):
                        print(f"\nPlease select a positive integer between 1 and {len(AVAILABLE_MODELS)}\n")
                        continue
                    current_model = AVAILABLE_MODELS[selection-1]
                    print(f"\nSystem Success: Model set to {current_model}\n")
                
                except ValueError as e:
                    print(f"\nSystem Error: Please input a positive integer between 1 and {len(AVAILABLE_MODELS)}. {e}\n")
                    print_model_menu()

                continue

            elif command == "/help":
                print_help_menu()
                continue

        
        history.append({
            "role":"user",
            "parts": [{"text": user_input}]
        })

        config = types.GenerateContentConfig(
            temperature = temperature, # Variable from 0.0 to 2.0
            max_output_tokens = max_output_tokens # Limit output tokens (token is about 4 characters ~~ 0.75 words)
        )   

        try:
            print("\nGemini: ", end="", flush=True)
            response_stream = client.models.generate_content_stream(
                model=current_model,
                contents=history,
                config=config
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