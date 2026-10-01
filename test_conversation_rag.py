from app.services.container import rag_service

session_id = "test-session-001"

answer1 = rag_service.answer(
    session_id=session_id,
    question="What does PostgreSQL store?",
)

print("\n--- ANSWER 1 ---")
print(answer1)


answer2 = rag_service.answer(
    session_id=session_id,
    question="And what does Qdrant store?",
)

print("\n--- ANSWER 2 ---")
print(answer2)


print("\n--- MEMORY ---")

messages = rag_service.memory_service.get_messages(session_id)

for message in messages:
    print(f"{message['role']}: {message['content']}")
