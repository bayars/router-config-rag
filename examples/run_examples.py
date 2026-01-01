#!/usr/bin/env python3
"""Run example prompts and save outputs to files."""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector_store import VectorStore
from router_agent import RouterConfigAgent

# Example prompts to test
EXAMPLE_PROMPTS = {
    "bgp_basic_config": """Configure an eBGP neighbor 10.0.0.2 with AS 65002.
My local AS is 65001. Set the router-id to 1.1.1.1""",

    "ospf_basic_setup": """Enable OSPF in area 0.0.0.0 on interfaces ethernet-1/1
and ethernet-1/2. Set router-id to 1.1.1.1""",

    "interface_config": """Configure ethernet-1/1 with IP address 10.0.0.1/30
and description "Link to core-router" """,

    "system_hostname": """Configure the system hostname as "spine-01" and set
the management interface with IP address 192.168.1.10/24""",

    "vlan_subinterface": """Create a subinterface on ethernet-1/2 with VLAN ID 100
and IP address 172.16.100.1/24""",
}


def main():
    # Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemma3:4b")  # Use smaller model for testing

    print(f"Using models:")
    print(f"  - Embedding: {EMBEDDING_MODEL}")
    print(f"  - LLM: {LLM_MODEL}")
    print()

    # Initialize vector store
    print("Loading vector store...")
    vector_store = VectorStore(embedding_model=EMBEDDING_MODEL)

    if vector_store.count() == 0:
        print("Error: Vector store is empty. Run 'python main.py --rebuild' first.")
        return 1

    print(f"Knowledge base has {vector_store.count()} document chunks")
    print()

    # Create agent
    agent = RouterConfigAgent(vector_store, model=LLM_MODEL)

    # Output directory
    output_dir = os.path.join(os.path.dirname(__file__), "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Run each prompt
    for name, prompt in EXAMPLE_PROMPTS.items():
        print(f"=" * 60)
        print(f"Running: {name}")
        print(f"=" * 60)
        print(f"Prompt: {prompt[:100]}...")
        print()

        try:
            # Generate response
            response = agent.generate_config(prompt)

            # Save to file
            output_file = os.path.join(output_dir, f"{name}.txt")
            with open(output_file, 'w') as f:
                f.write(f"# Prompt:\n{prompt}\n\n")
                f.write(f"# Model: {LLM_MODEL}\n\n")
                f.write(f"# Response:\n{response}\n")

            print(f"Output saved to: {output_file}")
            print()

            # Show preview
            preview = response[:500] + "..." if len(response) > 500 else response
            print(f"Preview:\n{preview}")
            print()

            # Reset conversation for next prompt
            agent.reset_conversation()

        except Exception as e:
            print(f"Error: {e}")
            print()

    print("=" * 60)
    print("Done! Check examples/outputs/ for results.")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
