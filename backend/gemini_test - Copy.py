import os
from google import genai


# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")


# Create Gemini client
client = genai.Client(
    api_key=api_key
)


# Send test question
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What is university attendance?"
)

# Print Gemini answer
print("\nGemini Response:")
print(response.text)