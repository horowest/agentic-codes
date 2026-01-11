"""
Simple chat app with memory
"""

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools import handle_tool_call, get_current_weather


load_dotenv()

GEMINI_MODEL = "gemini-2.5-flash-lite"
SYSTEM_INSTRUCTIONS = """
You're an assistant. Answer questions in a funny way. Keep your responses short and simple."
"""


def model_call(client, contents):
    return client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTIONS,
            tools=[get_current_weather],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )


def main():
    memory = []
    client = genai.Client()

    while True:
        query = input("User: ")

        if not query or query == "exit":
            break
        
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)]
        )
        memory.append(user_content)
        response = model_call(client, memory)

        if response.function_calls:
            handle_tool_call(response, memory)
            response = model_call(client, memory)

        print(f"Model: {response.text}")
    
    print("Exited")


if __name__ == "__main__":
    main()
