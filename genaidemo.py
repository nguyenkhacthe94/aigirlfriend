import os
from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyDXUaSNm0KfTuEDjNGFgysbdgocDsIbZc8')

# Create the model
response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents='What is your name?'
)
print(response.text)

response = client.models.generate_content(
    model='gemini-2.0-flash-exp',
    contents='high',
    config=types.GenerateContentConfig(
        system_instruction='I say high, you say low',
        temperature= 0.3,
    ),
)
print(response.text)