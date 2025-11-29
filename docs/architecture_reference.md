# Architecture Reference

This document provides a detailed technical overview of the codebase, including all implemented features, Azure services used, and code locations for learning and reference purposes.

## Table of Contents

- [Core Features Implemented](#core-features-implemented)
- [Azure Services Used](#azure-services-used)
- [Code Organization](#code-organization)
- [Key Entry Points](#key-entry-points)
- [Feature Code Locations](#feature-code-locations)
- [Data Flow Diagrams](#data-flow-diagrams)
- [Configuration & Environment Variables](#configuration--environment-variables)
- [Tech Stack & Dependencies](#tech-stack--dependencies)
- [Features Not Implemented (Expansion Opportunities)](#features-not-implemented-expansion-opportunities)

---

## Core Features Implemented

| Feature | Location | Description |
|---------|----------|-------------|
| **Streaming Chat API** | `src/api/routes.py:87-171` | SSE-based real-time chat with Azure OpenAI |
| **RAG (Retrieval-Augmented Generation)** | `src/api/routes.py:109-118` | Context-aware responses using vector search with citations |
| **Vector Search** | `src/api/search_index_manager.py:67-86` | Azure AI Search integration with HNSW algorithm |
| **Embedding Generation** | `src/api/search_index_manager.py:294-351` | Build embeddings from markdown documents |
| **Index Management** | `src/api/search_index_manager.py:159-180` | Create, delete, and manage search indexes |
| **Basic Authentication** | `src/api/routes.py:26-49` | Optional HTTP Basic authentication |
| **OpenTelemetry Tracing** | `src/api/main.py:45-58` | Application Insights monitoring integration |
| **Content Safety Filtering** | `src/api/routes.py:140-166` | Azure AI content filter handling with user-friendly errors |
| **Multi-model Support** | `src/api/main.py:66-75` | Configurable chat and embedding model deployments |

---

## Azure Services Used

| Service | Purpose | Code Reference |
|---------|---------|----------------|
| **Azure AI Foundry Projects** | Central AI project management | `src/api/main.py:40-43` |
| **Azure OpenAI Service** | Chat completions (gpt-4o-mini) & embeddings (text-embedding-3-small) | `src/api/main.py:66-75` |
| **Azure AI Search** | Vector store for RAG context retrieval | `src/api/search_index_manager.py` |
| **Azure Container Apps** | Serverless container hosting | `infra/api.bicep` |
| **Azure Container Registry** | Docker image storage | `infra/main.bicep` |
| **Azure Storage Account** | Blob storage for application data | `infra/main.bicep` |
| **Application Insights** | Performance monitoring & logging | `src/api/main.py:48` |
| **Azure Monitor** | OpenTelemetry tracing integration | `src/api/main.py:57-58` |
| **Azure Key Vault** | Secrets management | `infra/main.bicep` |
| **Log Analytics Workspace** | Centralized log collection | `infra/main.bicep` |
| **Managed Identity** | Passwordless Azure authentication | `src/api/main.py:25-37`, `infra/api.bicep:18-21` |

---

## Code Organization

```
get-started-with-ai-chat/
├── src/
│   ├── api/                              # Backend Python application
│   │   ├── main.py                       # FastAPI app creation & lifecycle
│   │   ├── routes.py                     # REST endpoints (chat, index)
│   │   ├── search_index_manager.py       # RAG search functionality
│   │   ├── util.py                       # Logger & Pydantic models
│   │   ├── upload_embeddings.py          # Embeddings upload utility
│   │   ├── templates/
│   │   │   └── index.html                # Jinja2 template (React mount)
│   │   ├── static/
│   │   │   ├── styles.css                # Global styles
│   │   │   └── react/assets/             # Built React app
│   │   └── data/
│   │       └── embeddings.csv            # Sample hiking product embeddings
│   │
│   ├── frontend/                         # React TypeScript application
│   │   ├── src/
│   │   │   ├── main.tsx                  # React DOM entry point
│   │   │   ├── components/
│   │   │   │   ├── App.tsx               # Root component with theme
│   │   │   │   ├── agents/
│   │   │   │   │   ├── AgentPreview.tsx          # Main chat orchestration
│   │   │   │   │   ├── AgentPreviewChatBot.tsx   # Chat UI container
│   │   │   │   │   ├── AssistantMessage.tsx      # AI response display
│   │   │   │   │   ├── UserMessage.tsx           # User message display
│   │   │   │   │   ├── chatbot/ChatInput.tsx     # Input component
│   │   │   │   │   └── UsageInfo.tsx             # Token usage display
│   │   │   │   └── core/
│   │   │   │       ├── Markdown.tsx              # Markdown rendering
│   │   │   │       ├── ThinkBlock.tsx            # Reasoning display
│   │   │   │       ├── SettingsPanel.tsx         # Configuration UI
│   │   │   │       └── theme/                    # Dark/light theme
│   │   │   └── types/
│   │   │       └── chat.ts               # TypeScript interfaces
│   │   ├── package.json                  # pnpm dependencies
│   │   └── vite.config.ts                # Vite build config
│   │
│   ├── requirements.txt                  # Python dependencies
│   └── gunicorn.conf.py                  # Server startup config
│
├── infra/                                # Azure Infrastructure as Code
│   ├── main.bicep                        # Primary infrastructure template
│   ├── main.parameters.json              # Parameter values
│   ├── api.bicep                         # API container app config
│   └── core/                             # Shared Bicep modules
│
├── tests/
│   └── test_search_index_manager.py      # RAG search unit tests
│
├── docs/                                 # Documentation
│   ├── RAG.md                            # RAG setup guide
│   ├── deployment.md                     # Deployment instructions
│   ├── local_development.md              # Dev environment setup
│   ├── deploy_customization.md           # Model & resource customization
│   ├── other_features.md                 # Monitoring & tracing
│   ├── troubleshooting.md                # Common issues
│   └── sample_questions.md               # Test queries
│
├── scripts/                              # Deployment automation
│   ├── postdeploy.sh / .ps1
│   ├── setup_credential.sh / .ps1
│   ├── validate_env_vars.sh / .ps1
│   └── set_default_models.sh / .ps1
│
├── azure.yaml                            # Azure Developer CLI config
├── pyproject.toml                        # Python project metadata
└── README.md                             # Project overview
```

---

## Key Entry Points

### Backend Entry Points

| File | Purpose | Key Function/Line |
|------|---------|-------------------|
| `src/api/main.py` | FastAPI app initialization | `create_app()` (line 110), `lifespan()` (line 23) |
| `src/api/routes.py` | API endpoint definitions | `chat_stream_handler()` POST (line 87) |
| `src/gunicorn.conf.py` | WSGI server configuration | `on_starting()` hook (line 44) |

### Data & Processing Scripts

| File | Purpose | Usage |
|------|---------|-------|
| `src/api/upload_embeddings.py` | One-time embeddings upload | `python -m api.upload_embeddings` |
| `src/api/search_index_manager.py` | RAG helper class | Used by routes and gunicorn for search ops |

### Frontend Entry Points

| File | Purpose |
|------|---------|
| `src/frontend/src/main.tsx` | React DOM mount point |
| `src/frontend/src/components/App.tsx` | Root component with theme provider |
| `src/frontend/src/components/agents/AgentPreview.tsx` | Main chat orchestration |

---

## Feature Code Locations

### SearchIndexManager Key Methods

| Method | Lines | Purpose |
|--------|-------|---------|
| `__init__()` | 24-65 | Initialize with Azure AI Search credentials |
| `search()` | 67-86 | Query vector store for relevant context |
| `upload_documents()` | 88-108 | Load embeddings from CSV |
| `is_index_empty()` | 110-121 | Check document count |
| `delete_index()` | 134-139 | Remove index from search service |
| `ensure_index_created()` | 159-180 | Create index if missing |
| `build_embeddings_file()` | 294-351 | Generate embeddings from markdown |

### Routes Key Endpoints

| Endpoint | Method | Lines | Purpose |
|----------|--------|-------|---------|
| `/` | GET | 51-75 | Serve React frontend |
| `/index-name` | GET | 78-84 | Return current search index name |
| `/chat` | POST | 87-171 | Stream chat completions with optional RAG |

---

## Data Flow Diagrams

### Chat Completion Flow

```
Client Request
    ↓
routes.py:87-94 (POST /chat endpoint)
    ↓
routes.py:104-122 (Build prompt with optional RAG context)
    ↓
search_index_manager.py:67-86 (If RAG: search for context)
    ↓
main.py:66-70 (ChatCompletionsClient.complete() with streaming)
    ↓
routes.py:124-139 (Stream responses via SSE)
    ↓
routes.py:140-166 (Error handling with content filter processing)
    ↓
Client Response Stream
```

### RAG Search Pipeline

```
Query Input (routes.py:110)
    ↓
search_index_manager.py:75-76 (Embed query using EmbeddingsClient)
    ↓
search_index_manager.py:80-81 (Vector similarity search in Azure AI Search)
    ↓
search_index_manager.py:85-86 (Return top-5 results)
    ↓
routes.py:112-115 (Inject context into prompt template)
    ↓
LLM Response with Context
```

### Application Startup Flow

```
gunicorn startup
    ↓
gunicorn.conf.py:44-46 (on_starting hook)
    ↓
gunicorn.conf.py:11-41 (create_index_maybe() async function)
    ↓
search_index_manager.py:159-179 (ensure_index_created())
    ↓
search_index_manager.py:88-108 (upload_documents() from embeddings.csv)
    ↓
Application Ready
```

---

## Configuration & Environment Variables

### Required Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_AI_PROJECT_ENDPOINT` | AI Foundry project endpoint | - |
| `AZURE_AI_CHAT_DEPLOYMENT_NAME` | Chat model deployment | `gpt-4o-mini` |
| `AZURE_AI_EMBED_DEPLOYMENT_NAME` | Embedding model | `text-embedding-3-small` |

### Optional Variables (RAG)

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_AI_SEARCH_ENDPOINT` | Search service endpoint | - |
| `AZURE_AI_SEARCH_INDEX_NAME` | Vector index name | - |
| `AZURE_AI_EMBED_DIMENSIONS` | Embedding dimensions | `100` |

### Optional Features

| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_AZURE_MONITOR_TRACING` | Enable OpenTelemetry tracing | `false` |
| `WEB_APP_USERNAME` | Basic auth username | - |
| `WEB_APP_PASSWORD` | Basic auth password | - |
| `RUNNING_IN_PRODUCTION` | Production environment flag | `false` |

---

## Tech Stack & Dependencies

### Backend (Python 3.13)

| Category | Package | Version |
|----------|---------|---------|
| **Web Framework** | FastAPI | 0.115.13 |
| **ASGI Server** | Uvicorn | 0.29.0 |
| **WSGI Server** | Gunicorn | 23.0.0 |
| **Azure AI** | azure-ai-inference | 1.0.0b9 |
| **Azure Projects** | azure-ai-projects | 1.0.0 |
| **Azure Search** | azure-search-documents | latest |
| **Azure Auth** | azure-identity | 1.19.0 |
| **Monitoring** | azure-monitor-opentelemetry | 1.6.9 |

### Frontend (React 19.1.0 + TypeScript 5.8.3)

| Category | Package | Version |
|----------|---------|---------|
| **Build Tool** | Vite | 6.3.4 |
| **Package Manager** | pnpm | 10.4.1 |
| **UI Components** | @fluentui-copilot | latest |
| **Markdown** | react-markdown | 10.1.0 |
| **Syntax Highlighting** | react-syntax-highlighter | 15.5.0 |
| **Math Rendering** | rehype-katex | 7.0.0 |

---

## Features Not Implemented (Expansion Opportunities)

If you're using this as a learning testbed, here are Azure AI Foundry features you could add:

| Feature | Description | Azure Service |
|---------|-------------|---------------|
| **Prompt Flow** | Visual prompt orchestration and chaining | Azure AI Foundry |
| **Evaluation Framework** | Built-in model evaluation metrics | Azure AI Foundry |
| **Fine-tuning** | Custom model training on your data | Azure OpenAI |
| **Multi-agent Orchestration** | Multiple AI agents collaborating | Semantic Kernel / AutoGen |
| **Function Calling / Tools** | Let the model call external APIs | Azure OpenAI |
| **Image Generation** | Generate images from text | DALL-E / Azure OpenAI |
| **Speech Services** | Voice input/output | Azure Speech |
| **Document Intelligence** | PDF/form processing and extraction | Azure Document Intelligence |
| **Semantic Caching** | Cache similar queries for efficiency | Azure Redis / Custom |
| **Assistants API** | Stateful conversations with tools | Azure OpenAI Assistants |
| **Batch Processing** | Process large datasets asynchronously | Azure OpenAI Batch |

---

## Sample Data

The repository includes sample data for testing RAG functionality:

- **Location**: `src/api/data/embeddings.csv` (1.4 MB)
- **Content**: Hiking product embeddings
- **Model**: text-embedding-3-small (dimensions=100)
- **Test Questions**: See `docs/sample_questions.md`

---

## Testing

Unit tests are located in `tests/test_search_index_manager.py` (359 lines):

- Mock-based unit tests for index operations
- Index creation/deletion lifecycle tests
- Document upload & search tests
- Empty index checking
- E2E tests with live Azure services (marked as skip by default)
- Embeddings file generation tests

Run tests with:
```bash
cd src && python -m pytest ../tests/ -v
```
