from google import genai
from google.genai import types

GEMINI_API_KEY = ""


def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"


def call_function(name, args):
    print(f"Invoked tool: {name}")
    result = globals()[name](**args)
    return { "result": result }


def handle_tool_call(response, contents):
    func_call_part = response.function_calls[0]
    func_call_content = response.candidates[0].content
    func_name = func_call_part.name
    func_args = func_call_part.args

    func_result = call_function(func_name, func_args)
    func_response_part = types.Part.from_function_response(
        name=func_name,
        response=func_result
    )
    func_response_content = types.Content(
        role="tool",
        parts=[func_response_part]
    )

    contents.extend([func_call_content, func_response_content])


def main():
    query = input("User: ")
    user_content = types.UserContent(
        parts=[types.Part.from_text(text=query)]
    )
    contents = [user_content]


    with genai.Client(api_key=GEMINI_API_KEY) as client:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                tools=[get_current_weather],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            ),
        )

        if response.function_calls:
            handle_tool_call(response, contents)

            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=[get_current_weather],
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    )
                )
            )

        print(response.text)


if __name__ == "__main__":
    main()
