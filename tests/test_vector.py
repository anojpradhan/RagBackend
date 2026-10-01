from app.services.vector_service import VectorService

vector_service = VectorService()

vector_service.create_collection(vector_size=384)

print("Collection created successfully.")
