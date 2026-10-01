from app.services.memory_service import MemoryService

memory_service = MemoryService()

session_id = "test-session-001"


# Clear old data
memory_service.clear_session(session_id)


# Add conversation messages
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


# Retrieve messages
messages = memory_service.get_messages(
    session_id=session_id,
)


print("\n--- CHAT MEMORY ---")

for message in messages:
    print(message)


# Check Redis connection
print("\n--- REDIS PING ---")
print(memory_service.ping())


# Clear session
memory_service.clear_session(session_id)


# Verify session was cleared
messages_after_clear = memory_service.get_messages(
    session_id=session_id,
)

print("\n--- AFTER CLEAR ---")
print(messages_after_clear)
