# Example Prompts

This directory contains example prompts organized by category for the Nokia SR Linux Router Configuration Agent.

## Prompt Categories

| File | Description | Skill Level |
|------|-------------|-------------|
| [01_basic_config.md](01_basic_config.md) | System, interface, and basic setup | Beginner |
| [02_routing_protocols.md](02_routing_protocols.md) | BGP, OSPF, IS-IS configuration | Intermediate |
| [03_multi_router.md](03_multi_router.md) | Generate configs for multiple routers | Intermediate |
| [04_advanced_services.md](04_advanced_services.md) | EVPN, MPLS, SR, QoS | Advanced |
| [05_troubleshooting.md](05_troubleshooting.md) | Monitoring and diagnostics | All levels |

## Using the Prompts

### Interactive Mode

Copy any prompt and paste it into the agent:

```bash
python main.py

You: Configure ethernet-1/1 with IP address 10.0.0.1/30
```

### Generate Config Files

For multi-router prompts, include keywords like "write", "save", or "generate":

```bash
You: Write configurations for 3 routers with OSPF area 0
```

Config files will be saved to `configs/` directory.

## Output Examples

Example outputs are stored in the `outputs/` subdirectory (when available):

```
examples/
├── README.md
├── 01_basic_config.md
├── 02_routing_protocols.md
├── 03_multi_router.md
├── 04_advanced_services.md
├── 05_troubleshooting.md
└── outputs/
    ├── bgp_neighbor_config.txt
    ├── ospf_basic_setup.txt
    └── multi_router_3_ospf.txt
```

## Tips for Good Prompts

### Be Specific

```
# Good
Configure eBGP neighbor 10.0.0.2 with AS 65002, set hold-time to 90 seconds

# Too vague
Configure BGP
```

### Include Context

```
# Good
Set up OSPF area 0 on interfaces ethernet-1/1 and ethernet-1/2 with
router-id 1.1.1.1. This is for a spine switch in a data center fabric.

# Missing context
Configure OSPF on some interfaces
```

### Specify Output Format

```
# Good
Write configurations for 5 routers in SR Linux CLI format with comments
explaining each section

# Unclear format
Give me configs for 5 routers
```

## Model Recommendations by Prompt Type

| Prompt Type | Recommended Model | Notes |
|-------------|-------------------|-------|
| Basic config | Any model | Even `tinyllama` works |
| Single protocol | `llama3.2` or better | Default is good |
| Multi-router (3-6) | `llama3.2` or `mistral` | May need retry |
| Multi-router (7-12) | `llama3.1:8b` | Larger model needed |
| Advanced services | `llama3.1:8b` or `gemma2:9b` | Complex output |

## Creating Your Own Prompts

1. Start with a clear objective
2. Include specific values (IPs, AS numbers, VLANs)
3. Reference SR Linux-specific features when possible
4. Test with different models to find what works best

## Contributing

Feel free to add your own prompts! Create a new markdown file or add to existing categories.
