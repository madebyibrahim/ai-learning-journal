#!/usr/bin/env python3
"""
Gemini API Quickstart - asks "Hello, what is 2+2?" and prints the response.
Uses API key from .env file (multiple keys allowed, only one active).
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

def main():
    load_dotenv
    api_key=os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env file.")
        return
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.5-flash")
    print("Asking Gemini: 'Hello, what is 2+2?'")
    response = model.generate_content("Hello, what is 2+2?")
    print("\n Response:")
    print(response.text)

if __name__== "__main__":
    main()


