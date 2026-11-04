import os
from dotenv import load_dotenv
from google import genai

from custom_mcp import CustomMCP
from tools import WeatherTool, DateTool


# Load environment variables
load_dotenv()

# Get API keys
gemini_api_key = os.getenv("GEMINI_API_KEY")
weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")

# Check API keys
if not gemini_api_key or not weather_api_key:
    raise ValueError("API keys are missing. Check your .env file.")

# Initialize Gemini client
client = genai.Client(api_key=gemini_api_key)

# Select Gemini model
model_name = "gemini-3.5-flash-lite"

# Initialize tools
tools = [
    WeatherTool(api_key=weather_api_key),
    DateTool()
]

# Create AI assistant
assistant = CustomMCP(
    client=client,
    model_name=model_name,
    tools=tools
)


def main():

    print("\n🤖 Simple AI Assistant")
    print("------------------------------")
    print("Ask me about weather or date!")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        if not user_input.strip():
            continue

        response = assistant.chat(user_input)

        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()