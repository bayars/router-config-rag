#!/usr/bin/env python3
"""Test script to run the agent with a BGP EVPN spine-leaf configuration request."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pdf_processor import PDFProcessor
from vector_store import VectorStore
from router_agent import RouterConfigAgent


def main():
    # Configuration
    PDF_PATH = "srlinux.pdf"
    EMBEDDING_MODEL = "nomic-embed-text"
    LLM_MODEL = "llama3.1:8b"

    print(f"Using Ollama models:")
    print(f"  - Embedding: {EMBEDDING_MODEL}")
    print(f"  - LLM: {LLM_MODEL}\n")

    # Initialize knowledge base
    print("Initializing vector store...")
    vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)

    # Check if we need to process the PDF
    if vector_store.count() == 0:
        print("Processing SR Linux documentation...")
        processor = PDFProcessor(PDF_PATH)
        chunks = processor.process()

        print("Building vector store with Nomic embeddings via Ollama...")
        print("This may take a few minutes on first run...\n")
        vector_store.add_documents(chunks)
        print(f"\nKnowledge base ready with {vector_store.count()} document chunks\n")
    else:
        print(f"Using existing knowledge base with {vector_store.count()} document chunks\n")

    # Create agent
    print("Creating router configuration agent...")
    agent = RouterConfigAgent(vector_store, model=LLM_MODEL)

    # Test query - asking about BGP EVPN configuration (without file generation)
    query = "Explain how to configure BGP EVPN with VXLAN overlay on a spine-leaf fabric"

    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)
    print("\nGenerating response...\n")

    # Generate response
    response = agent.chat(query)

    print("=" * 80)
    print("Response:")
    print("=" * 80)
    print(response)
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
