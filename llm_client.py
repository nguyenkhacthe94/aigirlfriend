import json
import requests

LLM_URL = "http://localhost:11434/api/generate"  # adjust to your setup
LLM_MODEL_NAME = "llama3"                        # adjust to your installed model

def build_emotion_prompt(text: str) -> str:
    """Return a prompt asking the LLM to classify emotion for the given text."""
    return f"""
You are an emotion classifier for a VTuber avatar.

For the given text, output ONLY valid JSON with fields:

* "emotion": one of ["neutral","happy","sad","angry","surprised"]
* "intensity": a number from 0.0 to 1.0

Text: "{text}"
"""

def call_llm(prompt: str) -> str:
    """
    Send a prompt to the local LLaMA HTTP server and return its raw text response.

    Adjust the payload / keys to match the actual server.
    """
    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    resp = requests.post(LLM_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    # Adjust this if your API uses a different field name
    return data.get("response", "").strip()

def extract_json_from_text(raw: str) -> dict:
    """
    Extract the first JSON object from a text string and parse it.
    Assumes there is a '{ ... }' somewhere in the text.
    """
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in LLM response")
    json_str = raw[start:end+1]
    return json.loads(json_str)

def get_emotion_for_text(text: str) -> dict:
    """
    Return a dict like: {"emotion": "happy", "intensity": 0.8}
    """
    prompt = build_emotion_prompt(text)
    raw_response = call_llm(prompt)
    data = extract_json_from_text(raw_response)

    # Add simple defaults / normalization
    emotion = data.get("emotion", "neutral")
    intensity = float(data.get("intensity", 0.5))
    intensity = max(0.0, min(1.0, intensity))

    return {"emotion": emotion, "intensity": intensity}

if __name__ == "__main__":
    sample_text = "Wow, that's amazing news!"
    try:
        result = get_emotion_for_text(sample_text)
        print("Input text:", sample_text)
        print("LLM emotion result:", result)
    except Exception as e:
        print(f"Error connecting to LLM: {e}")
