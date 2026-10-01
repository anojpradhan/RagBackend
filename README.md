# Palm Mind AI- Conversational RAG Backend

A production-oriented backend for **document ingestion, semantic retrieval, conversational RAG, and interview booking**, built as part of the Palm Mind AI technical assignment.

The system provides a REST API for uploading PDF/TXT documents, processing and chunking their contents, generating embeddings, storing vectors in Qdrant, maintaining document metadata in PostgreSQL, and answering user queries through a custom Retrieval-Augmented Generation (RAG) pipeline.

The application is fully containerized using Docker Compose.

---

## Features

- FastAPI REST API
- PDF and TXT document ingestion
- Two selectable chunking strategies:
  - Recursive character chunking
  - Sentence-based chunking

- Sentence-transformer embeddings
- Qdrant vector database for semantic search
- PostgreSQL for document metadata
- Custom RAG pipeline
- Redis-based conversational memory
- Multi-turn conversations
- LLM-powered interview booking
- Structured booking information storage
- Async PostgreSQL access using SQLAlchemy
- Environment-based configuration
- Dockerized development and deployment environment
- API documentation through Swagger/OpenAPI
- Modular service-oriented architecture
- Type annotations throughout the application

---

## Architecture

```text
                         Client
                           │
                           ▼
                    ┌─────────────┐
                    │   FastAPI   │
                    │     API     │
                    └──────┬──────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
    Document Ingestion              Conversational RAG
             │                           │
             ▼                           ▼
        Text Extraction              Query Embedding
             │                           │
             ▼                           ▼
          Chunking                    Qdrant
             │                           │
             ▼                           ▼
        Embeddings                  Relevant Chunks
             │                           │
       ┌─────┴─────┐                     ▼
       │           │                  Context
       ▼           ▼                     │
    Qdrant    PostgreSQL                ▼
       │       Metadata                LLM
       │                                │
       │                                ▼
       │                              Answer
       │
       └──────────────┐
                      ▼
                    Redis
              Conversation Memory
```

---

## Technology Stack

| Component             | Technology                                         |
| --------------------- | -------------------------------------------------- |
| Backend               | FastAPI                                            |
| Language              | Python 3.13                                        |
| Validation & Settings | Pydantic / Pydantic Settings                       |
| Database              | PostgreSQL 17                                      |
| ORM                   | SQLAlchemy                                         |
| PostgreSQL Driver     | asyncpg                                            |
| Vector Database       | Qdrant                                             |
| Embedding Model       | `sentence-transformers/all-MiniLM-L6-v2`           |
| LLM                   | Google Gemini                                      |
| LLM Integration       | LangChain Google GenAI                             |
| Text Chunking         | LangChain Text Splitters + custom sentence chunker |
| Conversation Memory   | Redis                                              |
| PDF Processing        | PyMuPDF                                            |
| Containerization      | Docker / Docker Compose                            |
| API Documentation     | Swagger / OpenAPI                                  |

---

## Project Structure

```text
palm-mind-rag-backend/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── health.py
│   │       └── documents.py
│   │
│   ├── chunker/
│   │   ├── base.py
│   │   ├── recursive.py
│   │   ├── sentence.py
│   │   └── factory.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── database.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   └── document.py
│   │
│   ├── repositories/
│   │   └── document_repository.py
│   │
│   ├── schemas/
│   │   ├── document.py
│   │   └── chunking.py
│   │
│   ├── services/
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_service.py
│   │   └── rag_service.py
│   │
│   └── main.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Document Ingestion Flow

The document ingestion pipeline follows this workflow:

```text
PDF / TXT
   │
   ▼
Upload API
   │
   ▼
Text Extraction
   │
   ▼
Chunking Strategy
   │
   ├── Recursive Chunking
   │
   └── Sentence Chunking
   │
   ▼
Generate Embeddings
   │
   ▼
Store Vectors in Qdrant
   │
   ▼
Store Document Metadata in PostgreSQL
```

Each stored vector contains metadata such as:

- Document ID
- Filename
- Chunk index
- Chunk text

The PostgreSQL database stores document-level information such as:

- Document ID
- Filename
- File type
- Chunking strategy
- Chunk count
- Creation timestamp

---

## Chunking Strategies

The ingestion API supports two chunking strategies.

### Recursive Chunking

Uses `RecursiveCharacterTextSplitter` to recursively divide documents while attempting to preserve meaningful text boundaries.

Default configuration:

```text
Chunk size: 500
Chunk overlap: 50
```

### Sentence Chunking

A custom sentence-based chunker separates text using sentence boundaries and combines sentences until the configured chunk size is reached.

The strategy can be selected through the API request.

---

## Embedding and Vector Search

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The generated embeddings have a dimension of:

```text
384
```

Qdrant stores the vectors using cosine similarity.

The retrieval process is:

```text
User Question
     │
     ▼
Question Embedding
     │
     ▼
Qdrant Similarity Search
     │
     ▼
Top-K Relevant Chunks
     │
     ▼
RAG Context
```

---

## Custom RAG Pipeline

The RAG implementation is intentionally built without using `RetrievalQAChain`.

The pipeline follows:

```text
Question
   │
   ▼
Generate Query Embedding
   │
   ▼
Search Qdrant
   │
   ▼
Retrieve Relevant Chunks
   │
   ▼
Build Context
   │
   ▼
Construct Prompt
   │
   ▼
LLM
   │
   ▼
Generated Answer
```

This keeps retrieval and generation as separate components and provides greater control over the RAG workflow.

---

## Conversational Memory

Redis is used to maintain conversation state for multi-turn interactions.

Conceptually:

```text
User Message
     │
     ▼
Redis Conversation History
     │
     ▼
Current Question + Conversation Context
     │
     ▼
RAG Retrieval
     │
     ▼
LLM
     │
     ▼
Response
     │
     ▼
Redis
```

This allows the system to maintain context across multiple messages in a conversation.

---

## Interview Booking

The conversational system also supports interview-booking interactions.

The LLM can extract structured information such as:

```text
Name
Email
Date
Time
```

The extracted information is validated before being stored.

This allows a conversation such as:

```text
User → I would like to schedule an interview.

AI → Sure. May I have your name?

User → Anoj Pradhan

AI → What email address should I use?

...
```

to be converted into structured booking data.

---

## API

### Health Check

```http
GET /api/v1/health
```

Example response:

```json
{
  "status": "ok"
}
```

### Document Upload

```http
POST /api/v1/documents/upload
```

The endpoint accepts:

- `.pdf`
- `.txt`

and supports selecting the chunking strategy.

Available strategies:

```text
recursive
sentence
```

Example:

```text
POST /api/v1/documents/upload?chunking_strategy=recursive
```

The API processes the document, generates chunks and embeddings, stores the vectors in Qdrant, and stores document metadata in PostgreSQL.

### Interactive API Documentation

Once the application is running:

```text
http://localhost:8000/docs
```

Swagger UI provides an interactive interface for testing the available endpoints.

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
```

Never commit the real `.env` file or API keys to GitHub.

A `.env.example` file is included as a template.

---

# Running with Docker

Docker Compose runs the complete application stack:

```text
FastAPI
PostgreSQL
Redis
Qdrant
```

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd palm-mind-rag-backend
```

### 2. Configure environment variables

Create `.env` from `.env.example` and provide the required credentials.

### 3. Build and start the services

```bash
docker compose up -d --build
```

### 4. Check the services

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

### 5. Check API logs

```bash
docker compose logs api
```

### 6. Open Swagger

```text
http://localhost:8000/docs
```

### 7. Stop the services

```bash
docker compose down
```

Persistent data is stored in Docker volumes for:

- PostgreSQL
- Redis
- Qdrant

---

# Running Locally Without Docker

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

Configure `.env` for locally running services.

Then start FastAPI:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Docker Services

The Docker Compose environment contains the following services:

| Service    | Purpose                              | Port |
| ---------- | ------------------------------------ | ---: |
| `api`      | FastAPI application                  | 8000 |
| `postgres` | Document metadata                    | 5432 |
| `redis`    | Conversation memory                  | 6379 |
| `qdrant`   | Vector storage and similarity search | 6333 |

Within the Docker network, services communicate using their Compose service names:

```text
postgres:5432
redis:6379
qdrant:6333
```

---

## Design Decisions

### Modular Architecture

Responsibilities are separated into services, repositories, schemas, models, and API layers rather than placing the complete RAG workflow inside the route handlers.

### Strategy-Based Chunking

Chunking is implemented using a common abstraction:

```text
BaseChunker
    │
    ├── RecursiveChunker
    │
    └── SentenceChunker
```

A factory selects the appropriate implementation based on the requested strategy.

### Separate Vector and Metadata Storage

Qdrant is responsible for semantic vector retrieval, while PostgreSQL stores relational document metadata.

This allows each database to handle the type of data it is designed for.

### Custom RAG

Retrieval and generation are implemented as separate steps rather than relying on a high-level `RetrievalQAChain`.

This provides explicit control over:

- Query embedding
- Retrieval
- Context construction
- Prompt construction
- LLM generation

### Containerized Infrastructure

Docker Compose provides a reproducible environment containing the API and its supporting services.

---

## Requirements

- Python 3.13+
- Docker Desktop
- Docker Compose
- Google Gemini API key

When running the complete system through Docker, local installations of PostgreSQL, Redis, and Qdrant are not required.

---

## Security Notes

The following files and credentials should not be committed:

```text
.env
API keys
Passwords
Local virtual environments
```

The repository includes `.gitignore` and `.dockerignore` configurations to prevent unnecessary or sensitive files from being included.

---

## Future Improvements

Potential production improvements include:

- Alembic database migrations
- Automated test suite
- Authentication and authorization
- File size and MIME-type validation
- OCR support for scanned PDFs
- More robust document lifecycle management
- Retry and rollback handling across PostgreSQL and Qdrant
- Structured logging
- Rate limiting
- Production deployment configuration
- Improved observability and monitoring

---

## Assignment Constraints Addressed

The implementation follows the main technical constraints:

- FastAPI REST backend
- PDF/TXT ingestion
- Two selectable chunking strategies
- Vector database integration using Qdrant
- SQL metadata storage using PostgreSQL
- Custom RAG implementation
- Redis conversation memory
- Multi-turn conversation support
- LLM-based interview booking
- Modular architecture
- Type annotations
- Dockerized application
- No FAISS
- No Chroma
- No `RetrievalQAChain`
- No frontend/UI

---

## Author

**Anoj Pradhan**

BSc CSIT — Tribhuvan University

AI/ML & Data Science Enthusiast | Full Stack Developer

---
