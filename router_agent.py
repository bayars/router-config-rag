"""SR Linux Router Configuration Agent using RAG with Nomic embeddings via Ollama."""

from typing import List, Dict
import os
import re
import ollama
from vector_store import VectorStore


class RouterConfigAgent:
    """Agent that generates SR Linux router configurations using RAG with Ollama."""

    def __init__(self, vector_store: VectorStore, model: str = "llama3.2"):
        """
        Initialize the router configuration agent.

        Args:
            vector_store: VectorStore instance with SR Linux documentation
            model: Ollama model name to use for generation
        """
        self.vector_store = vector_store
        self.model = model
        self.conversation_history = []

    def retrieve_context(self, query: str, n_results: int = 5) -> str:
        """
        Retrieve relevant documentation context for a query.

        Args:
            query: User query
            n_results: Number of relevant chunks to retrieve

        Returns:
            Formatted context string
        """
        results = self.vector_store.search(query, n_results=n_results)

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Context {i}]\n{result['text']}\n")

        return "\n".join(context_parts)

    def generate_config(self, user_request: str, n_context_chunks: int = 5) -> str:
        """
        Generate router configuration based on user request.

        Args:
            user_request: User's configuration request
            n_context_chunks: Number of context chunks to retrieve

        Returns:
            Generated configuration and explanation
        """
        # Retrieve relevant documentation
        context = self.retrieve_context(user_request, n_results=n_context_chunks)

        # Build system prompt
        system_prompt = """You are an expert SR Linux router configuration assistant.
You have access to SR Linux documentation and help users configure Nokia SR Linux routers.

Your tasks:
1. Understand the user's configuration requirements
2. Use the provided documentation context to generate accurate SR Linux CLI commands
3. Provide clear explanations of what each configuration does
4. Include best practices and warnings where appropriate
5. Format configurations clearly with proper SR Linux CLI syntax

Always base your answers on the provided documentation context."""

        # Build user message with context
        user_message = f"""Based on the following SR Linux documentation:

{context}

---

User Request: {user_request}

Please provide the appropriate SR Linux configuration commands and explain what they do."""

        # Build messages for Ollama
        messages = []

        # Add system message if this is the first message
        if len(self.conversation_history) == 0:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        # Add conversation history
        messages.extend(self.conversation_history)

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Generate response using Ollama
        response = ollama.chat(
            model=self.model,
            messages=messages
        )

        assistant_message = response['message']['content']

        # Add user message and assistant response to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def write_config_to_file(self, router_name: str, config: str, output_dir: str = "configs") -> str:
        """
        Write configuration to a file in ContainerLab CLI format.

        Args:
            router_name: Name of the router (e.g., 'spine1', 'leaf1')
            config: Configuration content
            output_dir: Directory to save configs

        Returns:
            Path to the written file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Sanitize router name for filename
        safe_name = re.sub(r'[^\w\-]', '_', router_name.lower())
        filename = f"{safe_name}.cli"  # Use .cli extension for ContainerLab
        filepath = os.path.join(output_dir, filename)

        # Write config to file
        with open(filepath, 'w') as f:
            f.write(config)

        return filepath

    def generate_and_write_configs(self, user_request: str, num_routers: int = 3,
                                   output_dir: str = "configs") -> Dict[str, str]:
        """
        Generate configurations for multiple routers and write to files.

        Args:
            user_request: User's configuration request
            num_routers: Number of routers to configure
            output_dir: Directory to save configs

        Returns:
            Dictionary mapping router names to file paths
        """
        # Retrieve relevant documentation
        context = self.retrieve_context(user_request, n_results=7)

        # Build system prompt with stronger formatting requirements for FULL ContainerLab configs
        system_prompt = f"""You are an expert SR Linux router configuration assistant for ContainerLab deployments.

⚠️ CRITICAL INSTRUCTION ⚠️
You MUST generate ALL {num_routers} COMPLETE, FULL startup configurations.
These configs will be used DIRECTLY in ContainerLab as startup-config files.
DO NOT use placeholders like "..." or "(continue for ALL routers)".
ACTUALLY GENERATE ALL {num_routers} COMPLETE CONFIGURATIONS.

MANDATORY FORMAT - Use this EXACT format for EACH of the {num_routers} routers:

### ROUTER: leaf1
<complete full config>
### END ROUTER

### ROUTER: leaf2
<complete full config>
### END ROUTER

(continue for ALL {num_routers} routers)

SR LINUX CLI FORMAT REQUIREMENTS:
Use the SR Linux "set /" CLI format. Each config MUST be a COMPLETE startup config including:

1. SYSTEM CONFIGURATION:
   set / system hostname <router-name>

2. INTERFACE CONFIGURATION (include ALL interfaces needed):
   set / interface ethernet-1/1 admin-state enable
   set / interface ethernet-1/1 subinterface 0 ipv4 admin-state enable
   set / interface ethernet-1/1 subinterface 0 ipv4 address <ip>/<mask>

   set / interface system0 admin-state enable
   set / interface system0 subinterface 0 ipv4 admin-state enable
   set / interface system0 subinterface 0 ipv4 address <loopback-ip>/32

3. NETWORK-INSTANCE (VRF) CONFIGURATION:
   set / network-instance default type default
   set / network-instance default admin-state enable
   set / network-instance default interface ethernet-1/1.0
   set / network-instance default interface system0.0

4. ROUTING POLICY:
   set / routing-policy policy all default-action policy-result accept

5. BGP CONFIGURATION (within network-instance):
   set / network-instance default protocols bgp admin-state enable
   set / network-instance default protocols bgp autonomous-system <as-number>
   set / network-instance default protocols bgp router-id <router-id>
   set / network-instance default protocols bgp group <group-name> export-policy [all]
   set / network-instance default protocols bgp group <group-name> import-policy [all]
   set / network-instance default protocols bgp neighbor <peer-ip> peer-as <peer-as>
   set / network-instance default protocols bgp neighbor <peer-ip> peer-group <group-name>

6. FOR BGP EVPN - ADD THESE:
   set / network-instance default protocols bgp group overlay peer-as <as>
   set / network-instance default protocols bgp group overlay afi-safi evpn admin-state enable
   set / network-instance default protocols bgp group overlay afi-safi ipv4-unicast admin-state disable
   set / network-instance default protocols bgp group overlay local-as as-number <as>

   set / tunnel-interface vxlan1 vxlan-interface 1 type bridged ingress vni <vni>

   set / network-instance mac-vrf-1 type mac-vrf
   set / network-instance mac-vrf-1 interface <access-interface>
   set / network-instance mac-vrf-1 vxlan-interface vxlan1.1
   set / network-instance mac-vrf-1 protocols bgp-evpn bgp-instance 1 admin-state enable
   set / network-instance mac-vrf-1 protocols bgp-evpn bgp-instance 1 vxlan-interface vxlan1.1
   set / network-instance mac-vrf-1 protocols bgp-evpn bgp-instance 1 evi <evi>
   set / network-instance mac-vrf-1 protocols bgp-vpn bgp-instance 1 route-target export-rt target:<as>:<id>
   set / network-instance mac-vrf-1 protocols bgp-vpn bgp-instance 1 route-target import-rt target:<as>:<id>

STRICT REQUIREMENTS:
1. Generate EXACTLY {num_routers} COMPLETE configurations - NO SHORTCUTS
2. Use proper naming: leaf1, leaf2, spine1, spine2 (or router1, router2, etc.)
3. Use ### ROUTER: and ### END ROUTER markers for EACH router
4. NO markdown code blocks (no ```)
5. NO explanatory text, NO placeholders
6. ONLY raw "set /" CLI commands inside each router section
7. Each config must be COMPLETE and directly usable in ContainerLab

ADDRESSING SCHEME:
- System loopbacks: 10.0.0.1/32, 10.0.0.2/32, ..., 10.0.0.{num_routers}/32
- Router IDs: Match loopback (10.0.0.1, 10.0.0.2, ...)
- Spine-Leaf links: 100.64.X.Y/31 point-to-point
- For iBGP EVPN: Use AS 65100 for all routers
- For eBGP underlay: Spines AS 65000, Leaves AS 65001, 65002, etc.
- VNI for EVPN: Start at 10000
- EVI: Match router number (1, 2, 3, ...)

User request: {user_request}

START GENERATING ALL {num_routers} FULL CONTAINERLAB CONFIGURATIONS NOW."""

        # Build user message
        user_message = f"""Documentation context:

{context}

---

Task: Generate {num_routers} COMPLETE SR Linux startup configurations for ContainerLab with these requirements:
{user_request}

CRITICAL REMINDERS:
- Generate EXACTLY {num_routers} FULL configs (not partial configs)
- Each config must be complete and ready to use as ContainerLab startup-config
- Use "set /" CLI format for all commands
- Include: system, interfaces, network-instance, routing-policy, BGP, and any EVPN/VXLAN config
- Use ### ROUTER: <name> and ### END ROUTER markers
- Proper coordinated IP addressing across all routers"""

        # Build messages for Ollama
        messages = [{
            "role": "system",
            "content": system_prompt
        }, {
            "role": "user",
            "content": user_message
        }]

        # Generate response using Ollama
        # Increase num_predict for large config generation (each router ~300 tokens, 12 routers = ~3600 tokens)
        # Add buffer for formatting and safety
        estimated_tokens = num_routers * 400  # 400 tokens per router config (with safety margin)
        max_tokens = max(4096, estimated_tokens)  # At least 4096, more if needed

        print(f"Generating configurations for {num_routers} routers...")
        print(f"  (Setting max tokens to {max_tokens} to ensure all configs are generated)")
        response = ollama.chat(
            model=self.model,
            messages=messages,
            options={'num_predict': max_tokens}
        )
        full_response = response['message']['content']

        # Debug: Save LLM response to file for inspection
        debug_file = "debug_llm_response.txt"
        with open(debug_file, 'w') as f:
            f.write(full_response)
        print(f"📝 Debug: LLM response saved to {debug_file}")

        # Check if LLM used placeholders (common with smaller models)
        placeholder_patterns = [
            r'\.\.\.\s*\(continued',
            r'\.\.\.\s*\(continue for',
            r'\.\.\.\s*\(repeat for',
            r'\.\.\.\s*through router',
        ]
        used_placeholder = any(re.search(pattern, full_response, re.IGNORECASE) for pattern in placeholder_patterns)

        if used_placeholder:
            print("⚠️  WARNING: LLM used placeholders instead of generating all configs!")
            print(f"   Model '{self.model}' may be too small for this task.")
            print("   Recommendation: Use a larger model like 'llama3.1:8b' or 'gemma3:12b'")
            print("   Example: LLM_MODEL='llama3.1:8b' python main.py")

        # Parse the response to extract individual router configs
        router_configs = self._parse_router_configs(full_response, num_routers)

        # Filter out configs that match expected naming patterns
        # Accept: router1, leaf1, spine1, node1, srl1, pe1, ce1, etc.
        expected_pattern = re.compile(r'^(router|leaf|spine|node|srl|pe|ce|p|rr|border|core|edge|access)\d+$', re.IGNORECASE)
        filtered_configs = {
            name: config for name, config in router_configs.items()
            if expected_pattern.match(name)
        }

        # If we filtered some out, report it
        extra_configs = set(router_configs.keys()) - set(filtered_configs.keys())
        if extra_configs:
            print(f"ℹ️  Filtered out {len(extra_configs)} extra section(s): {', '.join(sorted(extra_configs))}")

        # Use filtered configs
        router_configs = filtered_configs

        # Validate we got the right number
        if len(router_configs) != num_routers:
            print(f"⚠ Warning: Expected {num_routers} configs but got {len(router_configs)}")
            if len(router_configs) < num_routers:
                print(f"   The LLM may not have generated all requested configurations.")
            else:
                print(f"   The LLM generated more configs than requested.")

        # Write each config to a file
        written_files = {}
        for router_name, config in router_configs.items():
            filepath = self.write_config_to_file(router_name, config, output_dir)
            written_files[router_name] = filepath
            print(f"✓ Written {router_name} configuration to {filepath}")

        return written_files

    def _parse_router_configs(self, response: str, num_routers: int = 3) -> Dict[str, str]:
        """
        Parse router configurations from LLM response.

        Args:
            response: LLM response containing multiple router configs
            num_routers: Expected number of routers

        Returns:
            Dictionary mapping router names to configurations
        """
        configs = {}

        # First, try to find ### ROUTER: markers with ### END ROUTER
        # Split the response by ### ROUTER: to get sections
        router_sections = re.split(r'###\s*ROUTER:\s*', response, flags=re.IGNORECASE)

        # First section is usually empty or contains preamble, skip it
        print(f"🔍 Debug: Found {len(router_sections)} sections after splitting by ### ROUTER:")
        for i, section in enumerate(router_sections[1:], 1):
            # Extract router name (first word on the line)
            lines = section.strip().split('\n', 1)
            if not lines:
                continue

            router_name = lines[0].strip()
            if len(lines) > 1:
                config = lines[1]
            else:
                config = ""

            # Remove ### END ROUTER marker and everything after it
            end_marker_match = re.search(r'###\s*END\s*ROUTER', config, re.IGNORECASE)
            if end_marker_match:
                config = config[:end_marker_match.start()]

            # Clean up the config
            config = config.strip()

            # Remove any markdown code block markers
            config = re.sub(r'^```(?:bash|cli|cfg|srlinux)?\s*\n?', '', config, flags=re.MULTILINE)
            config = re.sub(r'\n?```\s*$', '', config)

            if config:  # Only add if there's actual content
                configs[router_name] = config
                print(f"  ✓ Parsed {router_name} ({len(config)} chars)")
            else:
                print(f"  ✗ Skipped section {i}: no config content for '{router_name}'")

        # If we found configs using markers, return them
        if configs:
            print(f"✓ Primary parsing found {len(configs)} configs")
            return configs

        # Fallback 1: Try to extract from markdown code blocks
        print("⚠ Warning: LLM did not use ### ROUTER: markers, attempting fallback parsing...")
        code_blocks = re.findall(r'```(?:bash|cli|cfg|srlinux)?\s*\n(.*?)\n```', response, re.DOTALL)

        if code_blocks:
            for i, config in enumerate(code_blocks, 1):
                configs[f"router{i}"] = config.strip()
            return configs

        # Fallback 2: Try to split by common config delimiters
        # Look for patterns like "Router 1:", "# Router 1", etc.
        section_pattern = r'(?:^|\n)(?:#\s*)?(?:Router|CONFIG|Configuration)\s+(\d+).*?\n(.*?)(?=(?:\n(?:#\s*)?(?:Router|CONFIG|Configuration)\s+\d+)|$)'
        section_matches = re.findall(section_pattern, response, re.DOTALL | re.IGNORECASE)

        if section_matches:
            for router_num, config in section_matches:
                config = config.strip()
                # Remove markdown code blocks if present
                config = re.sub(r'^```(?:bash|cli|cfg|srlinux)?\s*\n', '', config, flags=re.MULTILINE)
                config = re.sub(r'\n```\s*$', '', config)
                configs[f"router{router_num}"] = config
            return configs

        # Fallback 3: If still nothing and expecting only one router, use full response
        if not configs and num_routers == 1:
            clean_response = response.strip()
            # Remove markdown code blocks
            clean_response = re.sub(r'^```(?:bash|cli|cfg|srlinux)?\s*\n', '', clean_response, flags=re.MULTILINE)
            clean_response = re.sub(r'\n```\s*$', '', clean_response)
            configs["router1"] = clean_response

        return configs

    def chat(self, user_input: str) -> str:
        """
        Interactive chat interface for router configuration.

        Args:
            user_input: User's message or configuration request

        Returns:
            Agent's response
        """
        # Check if user wants to write configs to files
        write_keywords = ['write', 'save', 'generate files', 'create files', 'output to file',
                          'containerlab', 'clab', 'startup-config', 'startup config', 'full config']
        should_write = any(keyword in user_input.lower() for keyword in write_keywords)

        # Extract number of routers if specified
        # Match patterns like: "5 nodes", "5 routers", "5 leaves", "5 srlinux", etc.
        num_match = re.search(r'(\d+)\s+(?:different\s+)?(?:routers?|srlinux|nodes?|leaf|leaves|spines?|devices?)', user_input.lower())
        num_routers = int(num_match.group(1)) if num_match else 3

        if should_write:
            # Generate and write configs to files
            written_files = self.generate_and_write_configs(user_input, num_routers=num_routers)

            # Create response message
            response = f"Successfully generated {len(written_files)} ContainerLab startup configurations:\n\n"
            for router_name, filepath in written_files.items():
                response += f"  • {router_name}: {filepath}\n"

            response += f"\nAll .cli configuration files are saved in the 'configs/' directory."
            response += f"\n\nTo use in ContainerLab topology, reference them like:"
            response += f"\n  startup-config: configs/<router-name>.cli"
            return response
        else:
            # Normal chat interaction
            return self.generate_config(user_input)

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")

    def show_stats(self):
        """Show statistics about the knowledge base."""
        doc_count = self.vector_store.count()
        conv_length = len(self.conversation_history)

        return f"""
Knowledge Base Stats:
- Documents in vector store: {doc_count}
- Conversation turns: {conv_length}
"""
