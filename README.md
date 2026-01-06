# Nokia SR Linux Router Configuration Agent

A fully local RAG (Retrieval Augmented Generation) agent that helps configure Nokia SR Linux routers using official documentation. Runs 100% locally with Ollama - no cloud APIs or API keys required.

## Features

- **100% Local**: Runs entirely on your machine using Ollama
- **RAG Pipeline**: Semantic search over SR Linux documentation
- **Multi-Router Config Generation**: Generate configs for multiple routers at once
- **Interactive Chat**: Natural language interface with conversation history
- **Web Scraping**: Can ingest documentation from websites
- **Persistent Knowledge Base**: ChromaDB vector store

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        USER INTERACTION LAYER                               │
│  ┌─────────────┐                                                            │
│  │   main.py   │  Interactive CLI / Commands: stats, reset, quit           │
│  └──────┬──────┘                                                            │
└─────────┼───────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           RAG AGENT LAYER                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     router_agent.py                                   │   │
│  │  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐   │   │
│  │  │  Query Analysis │───▶│ Context Builder │───▶│  LLM Generation │   │   │
│  │  │  (intent detect)│    │  (top-k chunks) │    │   (via Ollama)  │   │   │
│  │  └─────────────────┘    └─────────────────┘    └─────────────────┘   │   │
│  │           │                                              │            │   │
│  │           │         ┌─────────────────────┐              │            │   │
│  │           └────────▶│ Config File Writer  │◀─────────────┘            │   │
│  │                     │  (multi-router .cfg)│                           │   │
│  │                     └─────────────────────┘                           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         KNOWLEDGE BASE LAYER                                │
│                                                                             │
│  ┌─────────────────┐         ┌─────────────────┐         ┌──────────────┐  │
│  │ vector_store.py │◀───────▶│    ChromaDB     │◀───────▶│   Ollama     │  │
│  │                 │         │  (chroma_db/)   │         │  Embeddings  │  │
│  │  - add_documents│         │                 │         │              │  │
│  │  - search       │         │  Persisted      │         │ nomic-embed  │  │
│  │  - clear        │         │  Vectors        │         │    -text     │  │
│  └─────────────────┘         └─────────────────┘         └──────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
          ▲
          │
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DOCUMENT PROCESSING LAYER                             │
│                                                                             │
│  ┌─────────────────┐                           ┌─────────────────┐          │
│  │ pdf_processor.py│                           │ web_scraper.py  │          │
│  │                 │                           │                 │          │
│  │  PDF ──▶ Text   │                           │  URL ──▶ Text   │          │
│  │  Text ──▶ Chunks│                           │  HTML ──▶ Chunks│          │
│  │                 │                           │                 │          │
│  │  1000 chars/chunk                           │  BeautifulSoup  │          │
│  │  200 char overlap                           │  Nav removal    │          │
│  └────────┬────────┘                           └────────┬────────┘          │
│           │                                             │                   │
│           ▼                                             ▼                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         docs/ Directory                              │   │
│  │   srlinux.pdf, sros.pdf, routing_protocols_guide.pdf, etc.          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## RAG Pipeline Flow

```
┌──────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│  User    │    │   Embedding   │    │   Vector    │    │   Top-K      │
│  Query   │───▶│   (Ollama)    │───▶│   Search    │───▶│   Chunks     │
└──────────┘    └───────────────┘    └─────────────┘    └──────┬───────┘
                                                               │
                                                               ▼
┌──────────┐    ┌───────────────┐    ┌─────────────┐    ┌──────────────┐
│ Response │◀───│  LLM (Ollama) │◀───│   Prompt    │◀───│   Context    │
│          │    │               │    │  + Context  │    │   Building   │
└──────────┘    └───────────────┘    └─────────────┘    └──────────────┘
```

## Video Presentation

![Video](./docs/nomic.mp4)

<video src="https://github.com/bayars/router-config-rag/blob/main/docs/nomic.mp4" controls></video>

## Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- 4GB+ RAM (8GB+ recommended)

### Installation

```bash
# 1. Clone and enter directory
cd nokia-srlinux-agent

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Ollama
ollama serve

# 5. Pull required models (in another terminal)
ollama pull nomic-embed-text   # Embedding model (required)
ollama pull llama3.2           # Default LLM
```

### Download Documentation

Place Nokia SR Linux PDFs in the `docs/` directory:

```bash
mkdir -p docs
# Download PDFs from Nokia documentation portal
# See docs section below for download links
```

### Run the Agent

```bash
# First run (builds vector database)
python main.py

# Force rebuild after adding new documents
python main.py --rebuild
```

## LLM Model Selection

### Model Comparison

| Model | Parameters | RAM Required | Speed | Quality | Best For |
|-------|------------|--------------|-------|---------|----------|
| `tinyllama` | 1.1B | 2-4 GB | Fastest | Basic | Testing, low-end hardware |
| `phi3:mini` | 3.8B | 4-6 GB | Fast | Good | Edge devices, quick responses |
| `gemma2:2b` | 2B | 4-6 GB | Fast | Good | Balanced performance |
| `llama3.2` | 3B | 6-8 GB | Fast | Good | **Default - recommended** |
| `mistral` | 7B | 8-12 GB | Medium | Better | General use |
| `llama3.1:8b` | 8B | 10-16 GB | Medium | Better | Multi-router configs |
| `gemma2:9b` | 9B | 12-16 GB | Medium | Better | Complex configs |
| `llama3.1:70b` | 70B | 48+ GB | Slow | Best | Maximum accuracy |

### Using Different Models

```bash
# Environment variable
export LLM_MODEL="tinyllama"
python main.py

# Or inline
LLM_MODEL="phi3:mini" python main.py

# For multi-router generation (need larger models)
LLM_MODEL="llama3.1:8b" python main.py
```

### Smallest Models for Low-End Hardware

```bash
# Absolute minimum (1.1B params, ~2GB RAM)
ollama pull tinyllama
LLM_MODEL="tinyllama" python main.py

# Good balance for low memory (3.8B params, ~4GB RAM)
ollama pull phi3:mini
LLM_MODEL="phi3:mini" python main.py

# Google's compact model (2B params)
ollama pull gemma2:2b
LLM_MODEL="gemma2:2b" python main.py
```

## Usage

### Interactive Commands

| Command | Description |
|---------|-------------|
| `stats` | Show knowledge base statistics |
| `reset` | Clear conversation history |
| `quit` / `exit` / `q` | Exit the agent |

### Example Session

```
$ python main.py

SR Linux Router Configuration Agent
============================================================
I can help you configure Nokia SR Linux routers!

You: How do I configure a BGP neighbor?

Agent: To configure a BGP neighbor on SR Linux, use the following commands:

    enter candidate

    /network-instance default {
        protocols {
            bgp {
                autonomous-system 65001
                router-id 10.0.0.1
                neighbor 10.0.0.2 {
                    peer-as 65002
                    peer-group ebgp-peers
                }
            }
        }
    }

    commit now

You: write configs for 3 routers with OSPF

Agent: I'll generate configurations for 3 routers...
[Writes router1.cfg, router2.cfg, router3.cfg to configs/]
```

## Documentation Sources

### Included PDFs (download to `docs/`)

| Document | Description | Download |
|----------|-------------|----------|
| `srlinux.pdf` | SR Linux base documentation | Nokia portal |
| `sros.pdf` | Service Router OS documentation | Nokia portal |
| `config_basics_guide_24.7.pdf` | Configuration basics | [Link](https://documentation.nokia.com/srlinux/24-7/books/pdf/Configuration_Basics_Guide_24.7.pdf) |
| `routing_protocols_guide.pdf` | BGP, OSPF, IS-IS | [Link](https://documentation.nokia.com/srlinux/23-3/books/pdf/Routing-Protocols-Guide_23.3.pdf) |
| `interface_config_guide.pdf` | Interface configuration | Nokia portal |
| `system_mgmt_guide_24.7.pdf` | CLI, gNMI, JSON-RPC | [Link](https://documentation.nokia.com/srlinux/24-7/books/pdf/System_Management_Guide_24.7.pdf) |
| `vpn_services_guide_25.7.pdf` | EVPN, MPLS, VPN | [Link](https://documentation.nokia.com/srlinux/25-7/books/pdf/VPN_Services_Guide_25.7.pdf) |

### Adding New Sources

Edit `main.py` to add PDFs or websites:

```python
PDF_PATHS = [
    "docs/srlinux.pdf",
    "docs/your_new_doc.pdf",  # Add new PDF
]

WEB_URLS = [
    "https://documentation.nokia.com/srlinux/24-7/",  # Add website
]
```

Then rebuild: `python main.py --rebuild`

## Project Structure

```
.
├── main.py                 # CLI entry point
├── router_agent.py         # RAG agent implementation
├── vector_store.py         # ChromaDB + Ollama embeddings
├── pdf_processor.py        # PDF text extraction/chunking
├── web_scraper.py          # Website scraping
├── requirements.txt        # Python dependencies
├── tests/                  # Test scripts
│   ├── test_agent.py
│   ├── test_write_configs.py
│   ├── test_12_routers.py
│   └── test_parsing.py
├── docs/                   # PDF documentation (gitignored)
├── examples/               # Example prompts and outputs
├── configs/                # Generated .cfg files (gitignored)
└── chroma_db/              # Vector database (gitignored)
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| LLM Inference | [Ollama](https://ollama.ai/) |
| Embeddings | nomic-embed-text via Ollama |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| PDF Processing | pypdf |
| Web Scraping | BeautifulSoup4 |

## Troubleshooting

### Connection Errors

```bash
# Ensure Ollama is running
ollama serve

# Check Ollama status
curl http://localhost:11434/api/tags
```

### Model Not Found

```bash
# List installed models
ollama list

# Pull missing models
ollama pull nomic-embed-text
ollama pull llama3.2
```

### Out of Memory

```bash
# Use a smaller model
LLM_MODEL="tinyllama" python main.py

# Or use quantized versions
ollama pull llama3.2:1b-q4_0
```

### Slow Performance

- Use smaller models (tinyllama, phi3:mini)
- Reduce chunk retrieval: edit `router_agent.py` to lower `top_k`
- Ensure you're using GPU acceleration if available

## License

MIT License - See LICENSE file for details.

## Resources

- [Nokia SR Linux Documentation](https://documentation.nokia.com/srlinux/)
- [Learn SR Linux](https://learn.srlinux.dev/)
- [Ollama](https://ollama.ai/)
- [ChromaDB](https://www.trychroma.com/)
