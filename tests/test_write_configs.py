#!/usr/bin/env python3
"""Test script to generate full ContainerLab startup configs for 3 leaf switches with BGP EVPN."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector_store import VectorStore
from router_agent import RouterConfigAgent


def main():
    # Configuration
    EMBEDDING_MODEL = "nomic-embed-text"
    LLM_MODEL = "llama3.1:8b"

    print(f"Using Ollama models:")
    print(f"  - Embedding: {EMBEDDING_MODEL}")
    print(f"  - LLM: {LLM_MODEL}\n")

    # Initialize knowledge base (should already exist from previous run)
    print("Loading vector store...")
    vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)
    print(f"Knowledge base loaded with {vector_store.count()} document chunks\n")

    # Create agent
    print("Creating router configuration agent...")
    agent = RouterConfigAgent(vector_store, model=LLM_MODEL)

    # Test query - generate full ContainerLab startup configs
    query = "Generate full ContainerLab startup configs for 3 leaf nodes with BGP EVPN and VXLAN"

    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)
    print()

    # Generate and write configs
    response = agent.chat(query)

    print("\n" + "=" * 80)
    print("Agent Response:")
    print("=" * 80)
    print(response)
    print()

    # Show the generated files
    print("\n" + "=" * 80)
    print("Generated ContainerLab Configuration Files:")
    print("=" * 80)

    if os.path.exists("configs"):
        for filename in sorted(os.listdir("configs")):
            if filename.endswith(".cli"):
                filepath = os.path.join("configs", filename)
                print(f"\n📄 {filepath}")
                print("-" * 80)
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Show first 40 lines (full configs are longer)
                    lines = content.split('\n')
                    for line in lines[:40]:
                        print(line)
                    if len(lines) > 40:
                        print(f"... ({len(lines) - 40} more lines)")
                print("-" * 80)

        # Show ContainerLab topology example
        print("\n" + "=" * 80)
        print("Example ContainerLab Topology Usage:")
        print("=" * 80)
        cli_files = [f for f in os.listdir("configs") if f.endswith(".cli")]
        if cli_files:
            print("""
topology:
  nodes:""")
            for cli_file in sorted(cli_files)[:3]:
                node_name = cli_file.replace('.cli', '')
                print(f"""    {node_name}:
      kind: nokia_srlinux
      startup-config: configs/{cli_file}""")


if __name__ == "__main__":
    main()
