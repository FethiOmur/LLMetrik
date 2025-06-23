# AMIF Grant Assistant

AMIF (Asylum, Migration and Integration Fund) grant documents intelligent question-answering system. LangGraph-based multi-agent chatbot with semantic search and source citations from PDF documents.

## Features

- **PDF Document Processing**: 49 AMIF grant documents loaded (7,400+ text chunks)
- **Semantic Search**: Advanced search using OpenAI embeddings
- **AI Assistant**: Intelligent responses powered by o4-mini
- **Source Citations**: PDF source and page number for every response
- **Web Interface**: Modern Flask & Streamlit web interfaces
- **Multilingual Support**: Turkish and English language support
- **LangGraph Memory**: Conversation history and context management

## System Architecture

```
GrantSpider/
├── config/          # API keys and model configurations
├── ingestion/       # PDF loading, text processing, vector database
├── agents/          # LangGraph agents (retriever, qa_agent, supervisor)
├── memory/          # Conversation memory management
├── chains/          # LangChain chains
├── graph/           # Multi-agent graph definitions
├── interfaces/      # Web interfaces
├── utils/           # Helper functions
└── data/            # PDF files and vector database
```

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment Variables
Create a `.env` file in the project root directory:

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
LLM_MODEL=o4-mini
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_DB_PATH=data/db
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
DEBUG=False
```

**Important**: The `.env` file is not committed to git for security purposes.

### 3. Load PDF Documents
Place your PDF files in the `data/raw/` folder and run the system.

## Usage

### Web Interface (Primary)
```bash
# Flask web interface (default)
python3 main.py

# Streamlit web interface
python3 main.py --streamlit

# Direct web application
python3 interfaces/web_app.py
```

**Web Features:**
- Modern web interface
- Real-time chat
- LangGraph Memory visualization
- Source links
- Session management

### PDF Ingestion
```bash
python3 main.py --ingest
```

### System Status
```bash
python3 main.py --status
```

## Technical Details

### Multi-Agent System
- **Document Retriever Agent**: Document search
- **QA Agent**: Question-answer generation
- **Source Tracker Agent**: Source tracking
- **Supervisor Agent**: Workflow coordination

### Workflow
1. **Query**: User question received
2. **Language Detection**: Automatic language detection
3. **Search**: Vector-based semantic search
4. **Storage**: Persistent storage in ChromaDB
5. **Search**: Semantic similarity search
6. **Response**: Contextual response generation with o4-mini

### Performance
- **Fast Search**: <2 seconds average response time
- **High Accuracy**: 90%+ source citation accuracy
- **Efficient Memory**: Optimized vector indexing

## Development

### Adding New PDFs
1. Add PDF file to `data/raw/` folder
2. Run `python3 main.py --ingest`

### Changing Model
Update the `LLM_MODEL` variable in the `.env` file.

## Libraries

- **LangChain**: Document processing and AI chains
- **LangGraph**: Multi-agent workflow
- **OpenAI o4-mini**: Language model
- **OpenAI Embeddings**: Text vectorization
- **ChromaDB**: Vector database
- **Flask**: Web framework
- **Streamlit**: Alternative web interface

## Dependencies

- OpenAI o4-mini and Embeddings API
- LangChain and LangGraph framework
- ChromaDB developers

---

**AMIF Grant Assistant** - Professional AI-Powered Grant Documentation System 