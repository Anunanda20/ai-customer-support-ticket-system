from ai_service import generate_support_response

message = "I cannot log in to my account. Please help me."

response = generate_support_response(message)

print("\nAI Support Response:")
print(response)
