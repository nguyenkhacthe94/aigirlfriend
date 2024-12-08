from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

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
        model="gemma2:9b",
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