# LLM-RAG-App 🚀

LLM-RAG-App is a multi-tenant, microservices-based platform designed to deliver a robust Retrieval-Augmented Generation (RAG) platform. Each user can operate their own personalized RAG service, leveraging specialized models tailored to their unique contexts. The platform seamlessly integrates user authentication, document ingestion, embedding generation, and retrieval capabilities. Built with cutting-edge technologies like FastAPI, Celery, Qdrant, and OpenAI's GPT-4 model, it ensures scalability, performance, and adaptability for diverse use cases.

## Features ✨

### User Service 👤
- **Authentication**: User registration and login with JWT-based authentication.
- **Role Management**: Role-based access control (e.g., admin-only endpoints).
- **Protected Endpoints**: Access user-specific or role-specific resources.

### RAG Service 📄🔍
- **Document Ingestion**: Upload and process documents (PDF and text files).
- **Embedding Generation**: Generate embeddings for text using Sentence Transformers.
- **Vector Search**: Store and retrieve embeddings using Qdrant.
- **Question Answering**: Use OpenAI's GPT-4 model to answer questions based on retrieved context.

## Core Technology Stack 🛠️

| Layer            | Tech                                         | Notes                                                                 |
|-------------------|----------------------------------------------|-----------------------------------------------------------------------|
| **API Server**    | FastAPI, Uvicorn                            | ⚡ Async, fast, dependency-injection friendly                         |
| **Auth**          | JWT auth (roadmap: Azure AD OAuth2)         | 🔒 Enterprise SSO-friendly                                            |
| **Data Layer**    | PostgreSQL + SQLAlchemy                     | 🗄️ Multi-tenant, RLS support                                          |
| **Vector Store**  | Qdrant (roadmap: Azure Cognitive Search / Azure Vector DB) | 📊 Pluggable, scalable                                                |
| **LLM Integration** | Azure OpenAI                              | 🤖 On-prem or hybrid depending on infra                               |
| **Caching / Queues** | Redis                                    | 🚀 For RAG performance, background jobs                               |
| **Async Tasks**   | Celery                                      | 🛠️ For ingestion / re-indexing                                        |
| **Secrets/Config** | .env managed securely (roadmap: Azure Key Vault) | 🔑 Centralized secret management                                      |
| **Monitoring**    | Prometheus, Grafana / Azure Monitor         | 📈 Optional for ops                                                   |
| **Deployment**    | Docker + Kubernetes (AKS or on-prem K8s)    | 🐳 Scalable, enterprise-ready                                         |

---

## Architecture 🏗️

The application is divided into two main services:

1. **User Service**:
    - Handles user authentication and role-based access control.
    - Built with FastAPI and SQLAlchemy for database interactions.

2. **RAG Service**:
    - Manages document ingestion, embedding generation, and retrieval.
    - Uses Celery for asynchronous task processing and Qdrant for vector search.

---

## Installation ⚙️

### Prerequisites ✅
- Docker and Docker Compose 🐳
- Python 3.11 🐍
- PostgreSQL 🗄️
- Redis 🔄

### Steps 🛠️
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/llm-rag-app.git
    cd llm-rag-app
    ```
2. Set up environment variables:
    - Copy `.env.example` to `.env` and configure the variables.

3. Start the services:
    ```bash
    docker-compose up --build
    ```

4. Verify the services:
    - User Service: [http://localhost:8000](http://localhost:8000) 🌐
    - RAG Service: [http://localhost:8001](http://localhost:8001) 🌐

---

## Usage 🖥️

### User Service 👤
- **Register**: `POST /api/v1/auth/register`
- **Login**: `POST /api/v1/auth/login`
- **Protected Endpoints**:
  - `GET /api/v1/protected/me`
  - `GET /api/v1/protected/admin-only`

### RAG Service 📄🔍
- **Health Check**: `GET /api/v1/health`
- **Upload Document**: `POST /api/v1/upload/upload`
- **Ingest Texts**: `POST /api/v1/upload/ingest`
- **Search**: `GET /api/v1/search?query=<query>`
- **Ask a Question**: `POST /api/v1/rag/ask`

---

## Development 🛠️

### Running Locally 🖥️
1. Install dependencies:
    ```bash
    pip install -r services/user-service/requirements.txt
    pip install -r services/rag-service/requirements.txt
    ```
2. Start the services:
    ```bash
    uvicorn services/user-service/app/main:app --reload --port 8000
    uvicorn services/rag-service/app/main:app --reload --port 8001
    ```
3. Run Celery workers:
    ```bash
    celery -A services/rag-service/app/worker.celery_app worker --loglevel=info
    ```

### Running with Docker Compose 🐳
1. Build and start the services:
    ```bash
    docker-compose up --build
    ```
2. Run Celery workers in a separate terminal:
    ```bash
    docker-compose run rag-service celery -A app.worker.celery_app worker --loglevel=info
    ```
3. Access the services:
    - User Service: [http://localhost:8000](http://localhost:8000) 🌐
    - RAG Service: [http://localhost:8001](http://localhost:8001) 🌐

### Running Tests 🧪
- **User Service**:
  ```bash
  pytest services/user-service/tests
  ```
- **RAG Service**:
  ```bash
  pytest services/rag-service/tests
  ```

---

## Environment Variables 🌍

| Variable                          | Description                              |
|-----------------------------------|------------------------------------------|
| `DATABASE_URL`                    | PostgreSQL connection string             |
| `JWT_SECRET_KEY`                  | Secret key for JWT                       |
| `JWT_ALGORITHM`                   | Algorithm for JWT                        |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes         |
| `REDIS_PORT`                      | Redis port                               |
| `QDRANT_PORT`                     | Qdrant port                              |
| `SERVER_PORT`                     | Service port                             |
| `LOGGER_LEVEL`                    | Logging level (e.g., DEBUG, INFO)        |

---

## File Structure 📂

```
llm-rag-app/
├── services/
│   ├── user-service/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── core/
│   │   │   ├── db/
│   │   │   ├── schemas/
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   ├── rag-service/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── db/
│   │   │   ├── llm/
│   │   │   ├── services/
│   │   │   ├── tasks/
│   │   │   └── main.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
├── tools/
├── .env.example
└── README.md
```

---

## Roadmap 🛤️

### Upcoming Features 🌟
1. **Kubernetes Integration**:
    - Full support for Kubernetes to enable scaling and orchestration of microservices.
    - Helm charts for simplified deployment.

2. **WebSocket for Task Status Updates**:
    - Real-time updates for long-running tasks such as document ingestion and embedding generation.
    - Improved user experience with live progress tracking.

3. **Frontend with React.js**:
    - A modern, user-friendly interface for interacting with the application.
    - Integration with backend APIs for seamless functionality.

4. **Responsive Layout**:
    - Ensure the frontend is fully responsive and optimized for various devices, including desktops, tablets, and mobile phones.

---

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments 🙌

- [FastAPI](https://fastapi.tiangolo.com/) ⚡
- [Celery](https://docs.celeryproject.org/) 🛠️
- [Qdrant](https://qdrant.tech/) 📊
- [OpenAI GPT-4](https://openai.com/) 🤖