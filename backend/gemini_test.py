import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from root .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv()

# Get API key from environment (.env)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file or chatbot_service.py.")


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Send test question
response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents="What is university attendance?"
)

# Print Gemini answer
print("\nGemini Response:")
print(response.text)