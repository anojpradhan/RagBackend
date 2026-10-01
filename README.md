# Palm Mind AI- Conversational RAG Backend

A backend system built with **FastAPI** that provides document ingestion, semantic search, conversational RAG, Redis-based conversation memory, and AI-powered interview booking.

The project was developed as a technical assignment for the **AI/ML Internship at Palm Mind AI**.

---

## Features

* PDF and TXT document upload
* Text extraction from uploaded documents
* Two selectable chunking strategies:

  * Recursive Character Chunking
  * Sentence-based Chunking
* Sentence-transformer embeddings
* Qdrant vector database for semantic search
* PostgreSQL for document and interview booking metadata
* Custom Retrieval-Augmented Generation (RAG) pipeline
* Gemini LLM integration
* Primary and fallback Gemini models
* Redis-based conversation memory
* Multi-turn conversations using session IDs
* AI-powered interview booking
* Structured extraction of:

  * Name
  * Email
  * Interview date
  * Interview time
* Dockerized application and supporting services
* REST APIs documented through FastAPI Swagger

---

## Architecture

### Document Ingestion

```text
PDF / TXT
   ↓
Text Extraction
   ↓
Chunking
   ↓
Embeddings
   ↓
Qdrant
   ↓
PostgreSQL Metadata
```

### Conversational RAG

```text
User Question
     ↓
Redis Conversation History
     ↓
Question Embedding
     ↓
Qdrant Similarity Search
     ↓
Relevant Document Context
     ↓
Gemini LLM
     ↓
Answer
     ↓
Redis Conversation Memory
```

### Interview Booking

```text
User Request
     ↓
Conversation History
     ↓
Gemini Structured Extraction
     ↓
Collect Missing Information
     ↓
PostgreSQL
     ↓
Booking Confirmation
```

---

## Technology Stack

| Technology            | Purpose                                  |
| --------------------- | ---------------------------------------- |
| FastAPI               | REST API framework                       |
| Python                | Backend development                      |
| PostgreSQL            | Document and booking metadata            |
| SQLAlchemy            | Database ORM                             |
| Qdrant                | Vector database                          |
| Sentence Transformers | Text embeddings                          |
| Redis                 | Conversation and booking memory          |
| Gemini                | LLM and booking information extraction   |
| LangChain             | Gemini integration and structured output |
| PyMuPDF               | PDF text extraction                      |
| Docker                | Containerization                         |
| Docker Compose        | Multi-service orchestration              |
| Pydantic              | Data validation                          |

---

## Project Structure

```text
palm-mind-rag-backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       ├── documents.py
│   │       ├── chat.py
│   │       └── bookings.py
│   │
│   ├── chunker/
│   │   ├── base.py
│   │   ├── factory.py
│   │   ├── recursive.py
│   │   └── sentence.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── database.py
│   │   └── init_db.py
│   │
│   ├── llm/
│   │   ├── base.py
│   │   └── gemini.py
│   │
│   ├── models/
│   │   ├── document.py
│   │   └── booking.py
│   │
│   ├── repositories/
│   │   ├── document_repository.py
│   │   └── booking_repository.py
│   │
│   ├── schemas/
│   │   ├── document.py
│   │   ├── chunking.py
│   │   ├── chat.py
│   │   └── booking.py
│   │
│   └── services/
│       ├── container.py
│       ├── document_service.py
│       ├── embedding_service.py
│       ├── vector_service.py
│       ├── rag_service.py
│       ├── memory_service.py
│       └── booking_service.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

### Folder Responsibilities

* **`api/`** — FastAPI routes and API endpoints
* **`chunker/`** — Document chunking strategies
* **`core/`** — Configuration and application-level exceptions
* **`db/`** — Database connection and initialization
* **`llm/`** — LLM abstraction and Gemini implementation
* **`models/`** — SQLAlchemy database models
* **`repositories/`** — Database operations
* **`schemas/`** — Pydantic request and response schemas
* **`services/`** — Application and business logic
* **`main.py`** — FastAPI application entry point

---

## API Endpoints

### Health Check

```http
GET /api/v1/health
```

Returns the application health status.

Example response:

```json
{
  "status": "ok"
}
```

---

### Document Upload

```http
POST /api/v1/documents/upload
```

Uploads a PDF or TXT document and processes it into chunks.

The chunking strategy can be selected using:

```text
recursive
```

or

```text
sentence
```

The endpoint returns the filename, file type, selected chunking strategy, and generated chunks.

---

### Conversational Chat

```http
POST /api/v1/chat
```

Request:

```json
{
  "session_id": "example-session",
  "question": "What information is available in the document?"
}
```

The system:

1. Retrieves previous conversation history from Redis.
2. Generates an embedding for the question.
3. Searches Qdrant for relevant document chunks.
4. Builds context from the retrieved chunks.
5. Sends the context and conversation history to Gemini.
6. Returns the generated answer.
7. Stores the conversation in Redis.

---

### Interview Booking

```http
POST /api/v1/bookings
```

Request:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "interview_date": "2026-10-15",
  "interview_time": "10:00:00"
}
```

The booking is stored in PostgreSQL.

The conversational RAG endpoint also supports interview booking through natural language. Gemini extracts booking information from the conversation and asks for any missing information before creating the booking.

---

## Data Storage

### PostgreSQL

PostgreSQL stores structured application data.

Current models include:

* `Document`
* `Booking`

### Qdrant

Qdrant stores document embeddings and associated chunk information for semantic retrieval.

### Redis

Redis stores:

* Conversation history
* Temporary interview booking information

Conversation and booking memory currently expire after **24 hours**.

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/palm_mind

QDRANT_URL=http://qdrant:6333
QDRANT_COLLECTION=documents

REDIS_URL=redis://redis:6379

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

GOOGLE_API_KEY=your_google_api_key

GEMINI_PRIMARY_MODEL=your_primary_model
GEMINI_FALLBACK_MODEL=your_fallback_model
```

> Do not commit the `.env` file or API keys to GitHub.

---

## Running with Docker

Make sure Docker Desktop is installed and running.

Build and start all services:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

Expected services:

```text
palm-mind-api
palm-mind-postgres
palm-mind-redis
palm-mind-qdrant
```

To view API logs:

```bash
docker compose logs api
```

To stop the services:

```bash
docker compose down
```

---

## Services

Docker Compose runs the following services:

| Service    |   Port | Purpose             |
| ---------- | -----: | ------------------- |
| API        | `8000` | FastAPI application |
| PostgreSQL | `5432` | Relational database |
| Redis      | `6379` | Conversation memory |
| Qdrant     | `6333` | Vector database     |

---

## API Documentation

Once the application is running, FastAPI automatically provides interactive API documentation.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

## Local Development Without Docker

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## RAG Approach

This project implements the RAG pipeline manually rather than using a high-level retrieval chain.

The main flow is:

```text
Question
   ↓
Embedding Generation
   ↓
Qdrant Similarity Search
   ↓
Relevant Chunks
   ↓
Context Construction
   ↓
Conversation History
   ↓
Gemini Prompt
   ↓
Generated Answer
```

The system instructs the LLM to use the retrieved document context as the primary source and avoid generating unsupported information.

---

## Interview Booking Flow

Interview booking is integrated into the conversational endpoint.

The system:

1. Detects booking-related requests.
2. Retrieves the existing conversation from Redis.
3. Uses Gemini to extract booking information.
4. Stores partially collected information in Redis.
5. Identifies missing fields.
6. Asks the user for the missing information.
7. Validates the completed booking using Pydantic schemas.
8. Stores the booking in PostgreSQL.
9. Returns a booking confirmation.
10. Clears the temporary booking data from Redis.

Required booking information:

```text
Name
Email
Interview Date
Interview Time
```

---

## Notes

* The project is designed as a backend-only application.
* No frontend/UI is included.
* Qdrant is used instead of FAISS or Chroma.
* The RAG pipeline is implemented directly without `RetrievalQAChain`.
* Redis provides temporary conversational memory.
* Gemini has a configurable primary and fallback model.
* Docker Compose is used to run the complete backend stack.

---

## Author

**Anoj Pradhan**
