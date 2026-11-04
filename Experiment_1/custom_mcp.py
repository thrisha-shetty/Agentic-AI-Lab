from google.genai import types


class CustomMCP:

    def __init__(self, client, model_name, tools):

        self.client = client
        self.model_name = model_name

        self.tools = {
            tool.name: tool for tool in tools
        }

        def get_weather(city: str) -> dict:
            """Get current weather information for a city."""
            return self.tools["weather"].execute({
                "city": city
            })

        def get_date() -> dict:
            """Get the current date and time."""
            return self.tools["date"].execute({})

        self.functions = [
            get_weather,
            get_date
        ]

        # Create Gemini chat session
        self.chat_session = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                temperature=0.7,
                tools=self.functions
            )
        )

    def chat(self, user_input: str) -> str:

        try:

            response = self.chat_session.send_message(user_input)

            return response.text or "I couldn't process your request."

        except Exception as e:

            return f"Sorry, an error occurred: {e}"