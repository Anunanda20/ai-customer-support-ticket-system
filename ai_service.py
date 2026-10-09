import ollama


def generate_support_response(customer_message):
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful customer support assistant. Give clear, polite and concise responses to customer problems."
            },
            {
                "role": "user",
                "content": customer_message
            }
        ]
    )

    return response["message"]["content"]
