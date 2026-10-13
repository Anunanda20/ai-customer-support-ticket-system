import os

from dotenv import load_dotenv
from google import genai
import ollama

load_dotenv()


def generate_support_response(customer_message):
    """Generate a professional customer-support response using Gemini or Ollama."""

    if not isinstance(customer_message, str) or not customer_message.strip():
        raise ValueError("Customer message cannot be empty.")

    provider = os.getenv("AI_PROVIDER", "gemini").strip().lower()

    system_instruction = (
        "You are a professional customer support assistant. "
        "Write helpful, polite, empathetic, and professional responses. "
        "Use clear sentences, correct spelling, proper spacing, and natural language. "
        "Address the customer's actual issue directly. "
        "Never use placeholders such as [Customer], [Customer Name], "
        "[Your Name], [Company Name], or similar bracketed names. "
        "Never invent the customer's name or personal details. "
        "Do not ask customers to share passwords, OTPs, or sensitive credentials. "
        "Ask only relevant questions needed to troubleshoot the issue. "
        "Provide practical troubleshooting steps when appropriate. "
        "Do not claim that an issue has been resolved unless confirmed. "
        "Keep responses concise, friendly, and easy to understand. "
        "Do not include a signature or sign-off unless appropriate. "
    )

    # Option 1: Use Ollama
    if provider == "ollama":
        response = ollama.chat(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            messages=[
                {
                    "role": "system",
                    "content": system_instruction,
                },
                {
                    "role": "user",
                    "content": customer_message.strip(),
                },
            ],
        )

        answer = response["message"]["content"].strip()

        if not answer:
            raise RuntimeError("Ollama returned an empty response.")

        return answer

    # Option 2: Use Google Gemini
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is missing from .env.")

        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents=customer_message.strip(),
            config={
                "system_instruction": system_instruction,
            },
        )

        if not response.text or not response.text.strip():
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()

    raise ValueError(
        "Invalid AI_PROVIDER. Choose 'gemini' or 'ollama'."
    )
