# Enterprise RAG Store Assistant - Team Reference Documentation

Welcome to the Developer Hub for the **Enterprise RAG Store Assistant**. This document serves as the single source of truth for our team, covering project setup, architectural guidelines, contribution standards, and scaling procedures. 

## 1. Project Overview
The Enterprise RAG Store Assistant is a state-of-the-art Natural Language Processing (NLP) chatbot pipeline specifically built to handle Arabic text. It leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers without hallucination. 

**Key Capabilities:**
*   Arabic intent classification using `aubmindlab/bert-base-arabertv02`.
*   Semantic vector search caching (ChromaDB) for lightning-fast repeated queries.
*   Local LLM integration (e.g., Qwen2.5) for high-privacy, context-injected generation.
*   Domain-Driven Design (DDD) to ensure infinite scalability and layer modification.

---

## 2. Getting Started & Setup

### Prerequisites
*   **Python 3.10+** (Recommended)
*   **CUDA Toolkit** (If running PyTorch models on GPU)

### Local Development Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hossamegy/Enterprise-Rag-Store-Assistant.git
   cd Enterprise-Rag-Store-Assistant
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > [!NOTE]
   > *Core packages include `fastapi`, `uvicorn`, `torch`, `transformers`, `sentence-transformers`, and `chromadb`.*

4. **Verify/Download Models:**
   Ensure your `DL_Models/` directory contains the necessary tuned weights (e.g., `arabic_intent_model.pt` and label encoders). 

5. **Run the Application:**
   * **For API Development:** Run the FastAPI server.
     ```bash
     uvicorn app:app --reload --host 0.0.0.0 --port 8000
     ```
   * **For Console/Pipeline Testing:** Run the main test script.
     ```bash
     python main.py
     ```

---

## 3. Architecture Deep Dive (DDD & Clean Architecture)

Our foundation is built on **Domain-Driven Design**. The codebase enforces strict boundaries so that our core logic never intimately knows about HTTP requests or specific database drivers.

### Directory Breakdown
```text
src/
├── core/               # The Heart of the App (No external dependencies)
│   ├── entities/       # e.g., MessageContext (Data object passing through the pipeline)
│   ├── ports/          # Interfaces (BaseLayer, BaseCache, BaseVectorStore)
│   └── prompts_templetes/ # RAG System prompts mapping strict Arabic generation rules
├── application/        # Business Use Cases
│   └── services/       # e.g., PipelineService (Orchestrator of the NLP chain)
├── infrastructure/     # Concrete Implementations of core ports
│   ├── nlp/            # The actual NLP layers (Pre-processing, Classifiers, LLM layer)
│   ├── cache/          # Semantic caching mechanisms
│   └── vector_store/   # ChromaDB implementations mapping to BaseVectorStore
├── api/                # Presentation Layer
│   ├── routers/        # FastAPI endpoints (e.g., vector_db_router.py)
│   └── schemas/        # Pydantic models for request/response validation
└── di/                 # Dependency Injection
    ├── nlp_di.py       # Wires the ML models and layers together
    ├── cache_di.py     # Sets up the Vector DB cache instance
    └── vector_store_di.py
```

### The Chain of Responsibility (NLP Pipeline)
When an API request arrives, the [PipelineService](file:///F:/Enterprise-Rag-Store-Assistant/src/application/services/pipeline_service.py#7-18) executes an ordered list of [BaseLayer](file:///F:/Enterprise-Rag-Store-Assistant/src/core/ports/base_layer.py#5-10) implementations. A typical request flows as follows:

1. **`GetCacheLayer`**: Performs a semantic search on previously asked questions. Short-circuits the pipeline if a >95% match is found.
2. **`PreprocessingLayer`**: Cleans Arabic text (removes emojis, normalizes characters).
3. **`ComplexityClassifierLayer`**: Flags if the question needs reasoning or is a simple FAQ.
4. **`IntentClassifierLayer`**: Predicts intent (`ask_price`, `compare_products`, etc.).
5. **`LocalLLMLayer`**: Injects context into the [rag_template.py](file:///f:/Enterprise-Rag-Store-Assistant/src/core/prompts_templetes/rag_template.py) prompt and invokes the local LLM.
6. **`SaveCacheLayer`**: Saves the LLM's new answer back to the semantic cache.

---

## 4. Team Contribution Guidelines

### Adding a New NLP Layer
Need to add a Translation or Profanity Filter layer? DO NOT modify existing layers. Create a new one.

1. **Create the Layer:** In `src/infrastructure/nlp/layers/`, implement the `BaseLayer` interface.
   ```python
   from src.core.ports.base_layer import BaseLayer
   from src.core.entities.message_context import MessageContext

   class TranslationLayer(BaseLayer):
       def handle(self, context: MessageContext) -> MessageContext:
           # 1. Read context.processed_input
           # 2. Perform translation
           # 3. Save to context.processed_input
           return context
   ```
2. **Inject the Layer:** Open `src/di/nlp_di.py` and add `TranslationLayer()` to the `layers` list inside `build_nlp_pipeline()`. The order in the list *is* the order of execution.

### Modifying Prompts
All LLM prompts live in `src/core/prompts_templetes/`. 
> [!WARNING]
> If the local LLM starts hallucinating or ignoring Arabic constraints, **do not** write code to fix it. First, attempt to update `rag_template.py` with stricter instructions. The system prompt is our primary defense against hallucinations.

### Coding Standards
* **Type Hinting:** Mandatory everywhere. (`def func(a: int) -> str:`)
* **Docstrings:** Required for all classes and complex pipeline layers explaining *what* it modifies in the `MessageContext`.
* **Testing:** Write isolated unit tests for core entities, and mock the `BaseVectorStore` when testing the `PipelineService`. 

---

## 5. Deployment & Scaling 

### Caching Strategy
* Our `vector_store` effectively acts as an intelligent semantic cache. For high availability, monitor the cache size. 
* By default, components in `di/*.py` use standard Python `@lru_cache(maxsize=1)` ensuring heavy objects (like HuggingFace models and DB clients) are strictly instantiated as **Singletons**.

### Horizontal Scaling
1. **API Scalability**: Because the FastAPI layer is entirely stateless, you can easily scale by running multiple Uvicorn workers (`uvicorn app:app --workers 4`). 
2. **LLM Inference**: If the system is bottlenecked by text generation, the `LocalLLMLayer` should be refactored to point to a dedicated inference server (like vLLM, Ollama, or Triton Inference Server) hosted on dedicated GPU machines, rather than loading model weights into the FastAPI process memory.
3. **Database Externalization**: ChromaDB currently runs locally. For production with multiple nodes, transition ChromaDB to a client-server setup by updating the `build_cache_chroma_db()` function in `di/cache_di.py` to point to the remote Chroma host.
