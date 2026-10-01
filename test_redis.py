from app.services.memory_service import MemoryService

memory_service = MemoryService()

session_id = "test-session-001"

memory_service.clear_session(session_id)

memory_service.add_message(
    session_id=session_id,
    role="user",
    content="My name is Anoj.",
)

memory_service.add_message(
    session_id=session_id,
    role="assistant",
    content="Nice to meet you, Anoj.",
)

memory_service.add_message(
    session_id=session_id,
    role="user",
    content="What is my name?",
)


messages = memory_service.get_messages(
    session_id=session_id,
)


print("\n--- CHAT MEMORY ---")

for message in messages:
    print(message)
