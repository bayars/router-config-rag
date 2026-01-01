#!/usr/bin/env python3
"""Test script to generate full ContainerLab startup configs for a 5-node spine-leaf fabric."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector_store import VectorStore
from router_agent import RouterConfigAgent


def main():
    # Configuration
    EMBEDDING_MODEL = "nomic-embed-text"
    LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1:8b")

    print(f"Using Ollama models:")
    print(f"  - Embedding: {EMBEDDING_MODEL}")
    print(f"  - LLM: {LLM_MODEL}\n")

    # Initialize knowledge base (should already exist from previous run)
    print("Loading vector store...")
    vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)

    if vector_store.count() == 0:
        print("Error: Vector store is empty. Please run main.py first to build it.")
        return

    print(f"Knowledge base loaded with {vector_store.count()} document chunks\n")

    # Create agent
    print("Creating router configuration agent...")
    agent = RouterConfigAgent(vector_store, model=LLM_MODEL)

    # Test query - generate full ContainerLab configs for spine-leaf with BGP EVPN
    query = """Generate full ContainerLab startup configs for 5 nodes:
    2 spine switches and 3 leaf switches with BGP EVPN overlay.
    Configure eBGP underlay between spines and leaves.
    Include system loopbacks, fabric interfaces, and VXLAN tunnels."""

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

    # Verify the generated files
    print("\n" + "=" * 80)
    print("Verification:")
    print("=" * 80)

    if os.path.exists("configs"):
        cli_files = sorted([f for f in os.listdir("configs") if f.endswith(".cli")])
        print(f"\nTotal ContainerLab config files generated: {len(cli_files)}")

        if len(cli_files) == 5:
            print("✓ SUCCESS: All 5 node configs were generated!")
        else:
            print(f"⚠ WARNING: Expected 5 configs but found {len(cli_files)}")

        print("\nFiles:")
        for filename in cli_files:
            filepath = os.path.join("configs", filename)
            file_size = os.path.getsize(filepath)
            # Count set commands to verify full config
            with open(filepath, 'r') as f:
                content = f.read()
                set_count = content.count('set /')
            print(f"  • {filename} ({file_size} bytes, {set_count} set commands)")

        # Show sample from first router
        if cli_files:
            print(f"\n--- Sample from {cli_files[0]} ---")
            with open(os.path.join("configs", cli_files[0]), 'r') as f:
                lines = f.readlines()
                for line in lines[:25]:
                    print(line.rstrip())
                if len(lines) > 25:
                    print(f"... ({len(lines) - 25} more lines)")

        # Show ContainerLab topology example
        print("\n" + "=" * 80)
        print("Example ContainerLab Topology (clab-topology.yml):")
        print("=" * 80)
        print("""
name: srlinux-evpn-fabric

topology:
  kinds:
    nokia_srlinux:
      image: ghcr.io/nokia/srlinux:latest

  nodes:""")
        for cli_file in cli_files:
            node_name = cli_file.replace('.cli', '')
            print(f"""    {node_name}:
      kind: nokia_srlinux
      startup-config: configs/{cli_file}""")

        print("""
  links:
    # Spine-Leaf connections (configure based on your fabric design)
    - endpoints: ["spine1:e1-1", "leaf1:e1-49"]
    - endpoints: ["spine1:e1-2", "leaf2:e1-49"]
    - endpoints: ["spine1:e1-3", "leaf3:e1-49"]
    - endpoints: ["spine2:e1-1", "leaf1:e1-50"]
    - endpoints: ["spine2:e1-2", "leaf2:e1-50"]
    - endpoints: ["spine2:e1-3", "leaf3:e1-50"]
""")


if __name__ == "__main__":
    main()
