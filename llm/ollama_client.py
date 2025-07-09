"""
Sends prompt + data to the Ollama LLM running locally (e.g., LLaMA 3.1)

Used by: batch_manager.py
"""

import requests

def call_llm_with_prompt(prompt: str, model: str = "llama3.1:8b") -> str:
    """
    Sends a prompt to the Ollama server and returns the generated text.

    Args:
        prompt (str): The full prompt to send (including data)
        model (str): The model to use (default is 'llama3')

    Returns:
        str: The raw text output from the model
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False   # Set True for real-time generation, False for full result
    }

    try:
        # 🔍 Debug: show what we’re sending to the model (just a snippet)
        print("\n🔺 Prompt being sent to LLM (first 300 chars):")
        print(prompt[:300])
        print("🔁 Sending request to Ollama...\n")

        # Call Ollama server
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            result = response.json()
            raw_output = result.get("response", "").strip()

            # 🧠 Debug: preview the model response
            print("✅ LLM Response received (first 300 chars):")
            print(raw_output[:300])
            return raw_output

        else:
            # ❌ Log error details
            print(f"❌ LLM API Error: {response.status_code}")
            print("Response:", response.text)
            return ""

    except Exception as e:
        # ❌ Handle connection issues
        print(f"❌ Failed to connect to Ollama: {e}")
        return ""
