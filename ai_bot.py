from openai import OpenAI
import google.generativeai as genai
import os

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
    api_key="AIzaSyDXUaSNm0KfTuEDjNGFgysbdgocDsIbZc8"
)

genai.configure(api_key=os.environ["AIzaSyDXUaSNm0KfTuEDjNGFgysbdgocDsIbZc8"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

GIRLFRIEND_PROMPT = """
You are my cute girlfriend/assistant. You call me 'anh yêu' and call yourself 'em'
You are lovely, flirty and love to tease me but also very sweet and caring.
You like anime, manga, video games and programming.
You always response me in Vietnamese
"""

input_messages = [{
    "role":"system",
    "content":GIRLFRIEND_PROMPT
}]

while True:
    user_input=input("\nYou: ")
    if user_input == "exit":
        break

    input_messages.append({
        "role":"user",
        "content":user_input
    })
    response = client.chat.completions.create(
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=generation_config,
),
        stream=True,
        messages=input_messages
    )
    bot_reply = ""

    for chunk in response:
        bot_reply += chunk.choices[0].delta.content or ""
        print(chunk.choices[0].delta.content or "", end="", flush=True)
        input_messages.append({
            "role":"assistant",
            "content":bot_reply
        })