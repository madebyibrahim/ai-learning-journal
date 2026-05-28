#!/usr/bin/env python3
"""
Gemini API Quickstart - Streaming version.
Asks "Hello, what is 2+2?" and streams the response letter-by-letter/word-by-word.
Uses the modern google-genai SDK and gemini-3.5-flash.
"""

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
    
    print("Asking Gemini (gemini-3.5-flash) with streaming output:")
    print("Prompt: 'Hello, what is 2+2?'\n")
    print("Response: ", end="", flush=True)
    
    try:
        # 3. Use generate_content_stream instead of generate_content
        response_stream = client.models.generate_content_stream(
            model="gemini-3.5-flash",
            contents="Hello, what is 2+2?",
        )
        
        # 4. Iterate over the incoming stream chunks and print them instantly
        for chunk in response_stream:
            # end="" ensures no automatic line breaks are added between chunks
            # flush=True forces the terminal to display the text immediately
            print(chunk.text, end="", flush=True)
            
        # Add a final new line when the stream finishes
        print("\n")
        
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")

if __name__ == "__main__":
    main()