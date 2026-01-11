from google import genai
from google.genai import types


GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini-2.5-flash-lite"

SYSTEM_INSTRUCTIONS = """
You're an assistant. Answer questions in a funny way. Keep your responses short and simple."
"""

def main():
    contents = []
    client = genai.Client(api_key=GEMINI_API_KEY)

    while True:
        query = input("User: ")

        if not query or query == "exit":
            break
        
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=query)]
        )
        contents.append(user_content)

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTIONS
            )
        )

        print(f"Model: {response.text}")
    
    print("Exited")


if __name__ == "__main__":
    main()
