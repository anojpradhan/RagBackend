from app.llm.gemini import GeminiLLM

llm = GeminiLLM()

response = llm.generate(
    "Explain what Retrieval-Augmented Generation is in two sentences."
)

print("\n--- GEMINI RESPONSE ---")
print(response)
