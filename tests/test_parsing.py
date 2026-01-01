#!/usr/bin/env python3
"""Test the router config parsing logic."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from router_agent import RouterConfigAgent
from vector_store import VectorStore


def test_parsing():
    """Test that parsing correctly extracts all router configs."""

    # Create a mock response with 12 routers
    mock_response = ""
    for i in range(1, 13):
        mock_response += f"""
### ROUTER: router{i}
hostname router{i}
interface loopback0
  ip address 1.1.1.{i}/32
!
router ospf 1
  router-id 1.1.1.{i}
!
router bgp 65000
  router-id 1.1.1.{i}
!
username admin password admin
### END ROUTER
"""

    print("Mock Response Generated")
    print("=" * 80)
    print(mock_response[:500] + "...")
    print("=" * 80)

    # Initialize a dummy agent just to test parsing
    vector_store = VectorStore()
    agent = RouterConfigAgent(vector_store)

    # Parse the mock response
    configs = agent._parse_router_configs(mock_response, num_routers=12)

    print(f"\nParsing Results:")
    print("=" * 80)
    print(f"Total configs parsed: {len(configs)}")
    print(f"Router names: {sorted(configs.keys())}")

    # Verify all 12 routers are present
    expected_routers = [f"router{i}" for i in range(1, 13)]
    missing_routers = set(expected_routers) - set(configs.keys())
    extra_routers = set(configs.keys()) - set(expected_routers)

    if missing_routers:
        print(f"\n❌ MISSING routers: {sorted(missing_routers)}")
    if extra_routers:
        print(f"\n⚠ EXTRA routers: {sorted(extra_routers)}")

    if len(configs) == 12 and not missing_routers and not extra_routers:
        print("\n✓ SUCCESS: All 12 routers parsed correctly!")

        # Show sample from router1
        print("\n--- Sample: router1 config ---")
        print(configs["router1"][:200])
        print("\n--- Sample: router12 config ---")
        print(configs["router12"][:200])
    else:
        print(f"\n❌ FAILED: Expected 12 routers, got {len(configs)}")

    return len(configs) == 12


if __name__ == "__main__":
    success = test_parsing()
    exit(0 if success else 1)
