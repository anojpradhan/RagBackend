from app.services.memory_service import MemoryService

memory_service = MemoryService()

if memory_service.ping():
    print("Redis connection successful.")
