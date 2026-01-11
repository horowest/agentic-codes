from google import genai
from google.genai import types

GEMINI_API_KEY = ""
GEMINI_MODEL = "gemini-2.5-flash"

with genai.Client(api_key=GEMINI_API_KEY) as client:
    # response = client.models.generate_content(
    #     model=GEMINI_MODEL,
    #     contents="Tell a joke",
    # )
    # print(response.text)

    # response_2 = client.models.generate_content(
    #     model=GEMINI_MODEL,
    #     config=types.GenerateContentConfig(
    #         system_instruction="You're an assistant who tells software related jokes",
    #         # max_output_tokens=3,
    #         # temperature=0.3,
    #     ),
    #     contents=types.UserContent(
    #         parts=[types.Part.from_text(text="tell a joke")]
    #     ),
    # )

   for response in client.models.generate_content_stream(
        model=GEMINI_MODEL,
        config=types.GenerateContentConfig(
            system_instruction="You're an assistant who tells software related jokes",
            # max_output_tokens=3,
            # temperature=0.3,
        ),
        contents=types.UserContent(
            parts=[types.Part.from_text(text="tell a joke in 100 words")]
        ),
    ):
        print(response.text)