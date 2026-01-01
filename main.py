#!/usr/bin/env python3
"""Main script for SR Linux Router Configuration Agent."""

import os
import sys
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from router_agent import RouterConfigAgent
from web_scraper import WebScraper


def initialize_knowledge_base(pdf_paths: list = None, web_urls: list = None,
                              force_rebuild: bool = False,
                              embedding_model: str = "nomic-embed-text") -> VectorStore:
    """
    Initialize the knowledge base from PDFs and websites.

    Args:
        pdf_paths: List of paths to PDF documentation files
        web_urls: List of website URLs to scrape and add
        force_rebuild: Force rebuild of the vector store
        embedding_model: Ollama embedding model to use

    Returns:
        Initialized VectorStore
    """
    if pdf_paths is None:
        pdf_paths = ["srlinux.pdf"]
    if web_urls is None:
        web_urls = []

    vector_store = VectorStore(embedding_model=embedding_model)

    # Check if we need to process sources
    if vector_store.count() == 0 or force_rebuild:
        if force_rebuild:
            vector_store.clear()

        total_sources = len(pdf_paths) + len(web_urls)
        print(f"Processing {total_sources} documentation source(s)...")

        # Process PDFs
        for pdf_path in pdf_paths:
            if not os.path.exists(pdf_path):
                print(f"⚠ Warning: {pdf_path} not found, skipping...")
                continue

            print(f"\n📄 Processing {pdf_path}...")
            processor = PDFProcessor(pdf_path)
            chunks = processor.process()

            # Add source metadata and make IDs unique per PDF
            pdf_name = os.path.basename(pdf_path).replace('.pdf', '')
            for chunk in chunks:
                chunk['source'] = os.path.basename(pdf_path)
                # Prepend PDF name to make IDs unique across all sources
                chunk['id'] = f"{pdf_name}_{chunk['id']}"

            print("  Adding to vector store...")
            vector_store.add_documents(chunks)

        # Process websites
        if web_urls:
            print(f"\n🌐 Processing {len(web_urls)} website(s)...")
            scraper = WebScraper()
            for url in web_urls:
                chunks = scraper.process_url(url)
                if chunks:
                    print("  Adding to vector store...")
                    vector_store.add_documents(chunks)

        print(f"\n✓ Knowledge base ready with {vector_store.count()} document chunks")
    else:
        print(f"Using existing knowledge base with {vector_store.count()} document chunks")

    return vector_store


def run_interactive_mode(agent: RouterConfigAgent):
    """
    Run the agent in interactive chat mode.

    Args:
        agent: RouterConfigAgent instance
    """
    print("\n" + "=" * 60)
    print("SR Linux Router Configuration Agent")
    print("=" * 60)
    print("\nI can help you configure Nokia SR Linux routers!")
    print("\nCommands:")
    print("  - Type your configuration request normally")
    print("  - 'stats' - Show knowledge base statistics")
    print("  - 'reset' - Clear conversation history")
    print("  - 'quit' or 'exit' - Exit the agent")
    print("\nExample prompts for ContainerLab configs:")
    print("  - 'Generate full ContainerLab configs for 5 nodes with BGP EVPN'")
    print("  - 'Create startup-config for 3 leaf switches with VXLAN'")
    print("  - 'Write clab configs for a spine-leaf fabric with eBGP underlay'")
    print("\nGenerated .cli files will be saved to configs/ directory")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if user_input.lower() == 'stats':
                print(agent.show_stats())
                continue

            if user_input.lower() == 'reset':
                agent.reset_conversation()
                continue

            # Generate response
            print("\nAgent: ", end="", flush=True)
            response = agent.chat(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


def main():
    """Main entry point."""
    # Configuration - Add all your documentation sources here
    # PDFs are stored in the docs/ directory
    PDF_PATHS = [
        "docs/srlinux.pdf",
        "docs/sros.pdf",
        "docs/sr-sim.pdf",
        "docs/config_basics_guide_24.7.pdf",
        "docs/routing_protocols_guide.pdf",
        "docs/interface_config_guide.pdf",
        "docs/system_mgmt_guide_24.7.pdf",
        "docs/vpn_services_guide_25.7.pdf",
        "docs/software_install_guide_24.7.pdf",
    ]

    # Add website URLs here
    WEB_URLS = [
        # "https://documentation.nokia.com/srlinux/latest/",
        # "https://documentation.nokia.com/sros/",
        # Add more URLs as needed
    ]

    FORCE_REBUILD = "--rebuild" in sys.argv

    # Ollama models
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

    print(f"Using Ollama models:")
    print(f"  - Embedding: {EMBEDDING_MODEL}")
    print(f"  - LLM: {LLM_MODEL}")
    print(f"\nMake sure these models are installed in Ollama:")
    print(f"  ollama pull {EMBEDDING_MODEL}")
    print(f"  ollama pull {LLM_MODEL}\n")

    try:
        # Initialize knowledge base
        vector_store = initialize_knowledge_base(
            pdf_paths=PDF_PATHS,
            web_urls=WEB_URLS,
            force_rebuild=FORCE_REBUILD,
            embedding_model=EMBEDDING_MODEL
        )

        # Create agent
        agent = RouterConfigAgent(vector_store, model=LLM_MODEL)

        # Run interactive mode
        run_interactive_mode(agent)

    except Exception as e:
        print(f"Fatal error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check that required models are installed:")
        print(f"   ollama pull {EMBEDDING_MODEL}")
        print(f"   ollama pull {LLM_MODEL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
