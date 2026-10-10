
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
        "Use clear sentences, correct spelling, and proper spacing. "
        "Organize troubleshooting steps into numbered lists when appropriate. "
        "Address the customer's actual issue directly. "
        "Do not use placeholders such as [Customer Name], [Your Name], "
        "[Company Name], or [Customer's Name]. "
        "Do not invent the customer's name or personal details. "
        "Do not ask for passwords, one-time passwords, or other sensitive credentials. "
        "Ask only for information that is genuinely necessary to troubleshoot the issue. "
        "Do not claim that a ticket has been resolved or an action has been completed "
        "unless that is confirmed. "
        "Keep the response concise, natural, and easy to understand. "
        "End with 'Best regards, Customer Support Team' when an email-style "
        "closing is appropriate."
    )

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