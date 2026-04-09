# Enterprise RAG Store Assistant

## Overview
The Enterprise RAG (Retrieval-Augmented Generation) Store Assistant is a sophisticated NLP-driven API built to serve as an intelligent, context-aware conversational agent for enterprise environments. It provides capabilities to classify user intent, gauge question complexity, fetch context dynamically from a vector database, and formulate accurate responses using Local and Cloud-based LLMs.

## Architecture

This project is built with maintainability, scalability, and loose coupling in mind. It deeply adheres to the **Clean Architecture** principles and leverages the **Pipeline Design Pattern** to execute its NLP workflows.

### 1. Clean Architecture Components
The components of the system are highly decoupled:
- **Core (`src/core`)**: Contains business entities (e.g., `MessageContext`, `Order`, `Product`), exceptions, and interfaces (Ports like `BaseLayer` and `ClassfierModel`). It has zero dependencies on external frameworks.
- **Application (`src/application`)**: Houses the application logic. The primary business process runner is `PipelineService`, which orchestrates the execution of incoming requests.
- **Infrastructure (`src/infrastructure`)**: Contains the concrete implementations of interfaces, dealing directly with technology such as:
  - ChromaDB (`vector_store`)
  - NLP Layers (`nlp/layers` like classifiers and LLM interactions)
  - Caching and specific LLM clients (Local LLM via Qwen and Cloud via Gemini API).
- **API (`src/api`)**: The delivery layer written in FastAPI, responsible for defining REST endpoints (`routers/chat_router.py`, `routers/vector_db_router.py`) and schemas.
- **DI (`src/di`)**: Uses basic factory functions grouped as an IoC (Inversion of Control) composition root to build our dependencies seamlessly and provide them to our routers.

### 2. The Pipeline Design Pattern
The NLP processing is primarily built around a structured **Pipeline Design Pattern**. We pass a single `MessageContext` state object through a sequential set of transformation layers.

Current Pipeline Flow (as defined in `src/di/nlp_di.py`):
1. **Cache Layer**: Check if a similar query exists in cache.
2. **Preprocessing**: Sanitize the incoming message.
3. **Complexity Classifier**: Classify if the query requires heavy processing.
4. **Intent Classifier**: Identify the goal of the user's request.
5. **Context Retrieval**: Pull context from the Chroma VectorDB based on embeddings.
6. **Local LLM Layer**: Attempt to query a local fast LLM.
7. **Gemini LLM Layer**: Call the Gemini GenAI model if local models defer or fail.
8. **Save Cache Layer**: Store the successfully generated response back to the cache.

---

## Scalability: How to Add or Remove Components

Due to the architectural choices, modifying the structure is extremely trivial and does not break existing logic.

### Modifying the Pipeline
Layers are fully independent. Each layer simply expects a `MessageContext` object, modifies it, and returns it.

**To Remove a Layer:**
Navigate to `src/di/nlp_di.py` inside `build_nlp_pipeline()`. Remove the unneeded layer instance from the `layers` array.

**To Add a New Layer:**
1. Create a new layer inside `src/infrastructure/nlp/layers/`. 
2. Inherit from `BaseLayer` imported from `src.core.ports.base_layer`.
3. Implement the abstract `handle` method.
```python
from src.core.ports.base_layer import BaseLayer
from src.core.entities.message_context import MessageContext

class TranslationLayer(BaseLayer):
    def handle(self, context: MessageContext) -> MessageContext:
        # Perform translations logic here...
        # Store results back in context 
        return context
```
4. Register it within the `layers` list inside `src/di/nlp_di.py` where it belongs functionally.

---

## Requirements and Installation

### Prerequisites
- Python 3.11.x (Managed via Conda is advised)
- PyTorch models and Tokenizers (Intent Model, Complexity Model, Sentence Transformers for embedding, and Qwen Local LLM)

### Setup Steps
1. **Create and Activate a Conda Environment**
   ```bash
   conda create -n test python=3.11.15 -y
   conda activate test
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note on GPU/CUDA Acceleration:** If you plan to run the AI features on your GPU for significantly faster inference, you must explicitly install the CUDA-enabled PyTorch version before or after installing the requirements. Refer to the [PyTorch Get Started](https://pytorch.org/get-started/locally/) page for the command matching your local CUDA version. For example (for CUDA 12.1):
   > ```bash
   > pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   > ```

3. **Configure Environment Variables**
   Create a `.env` file either in your root directory or inside `src/`, containing your API credentials:
   ```env
   GOOGLE_API_KEY="your gemini key"
   ```

4. **Prepare Machine Learning Artifacts**
   Before running the project, you **must substitute** your model paths in `src/config/settings.py` (or override them in the `.env` file). Ensure the following are downloaded and placed into `src/core/models/` (or paths modified in settings):
   - PyTorch model (`.pth`) classifying intent & complexity
   - Tokenizations & Label Encoders (`.pkl`)
   - Transformer Embedding model (e.g. `all-MiniLM-L6-v2`)
   - Local RAG LLM model (e.g., `Qwen2.5-1.5B-Instruct`)

### Running the Application

Start the FastAPI application using `uvicorn`:
```bash
uvicorn app:app --reload
```
Once started, the application connects to your database natively and builds the NLP pipeline asynchronously. Use `/docs` on the application's root URL to view and test all endpoints via Swagger UI.
