# Troubleshooting and Operational Prompts

These prompts help with monitoring, verification, and troubleshooting.

## Show Commands

### Prompt 1: Check BGP status
```
What commands do I use to check BGP neighbor status, view received
routes, and see advertised routes on SR Linux?
```

### Prompt 2: Verify OSPF
```
How do I verify OSPF adjacencies, view the OSPF database, and check
interface OSPF status on SR Linux?
```

### Prompt 3: Interface diagnostics
```
What commands show interface statistics, errors, and optical levels
on SR Linux? How do I check for CRC errors and drops?
```

### Prompt 4: Routing table verification
```
How do I view the routing table, check specific route details, and
see which protocol installed a route on SR Linux?
```

## Troubleshooting Scenarios

### Prompt 5: BGP not establishing
```
My BGP session to 10.0.0.2 is stuck in Active state. What should I
check? Give me the commands and common issues to look for
```

### Prompt 6: OSPF neighbor stuck in EXSTART
```
OSPF neighbor is stuck in EXSTART/EXCHANGE state. What are the
common causes and how do I diagnose this on SR Linux?
```

### Prompt 7: Traffic blackholing
```
Traffic to 192.168.100.0/24 is being dropped. How do I trace the
path, check the routing table, and verify forwarding on SR Linux?
```

### Prompt 8: High CPU usage
```
Router CPU is showing high usage. What commands show CPU statistics
by process and how do I identify the cause on SR Linux?
```

## Configuration Verification

### Prompt 9: Compare configurations
```
How do I compare the running configuration with a saved checkpoint
on SR Linux? How do I rollback if needed?
```

### Prompt 10: Validate before commit
```
What commands verify configuration changes before committing on
SR Linux? How do I use the confirmed commit feature?
```

## Logging and Events

### Prompt 11: Check system logs
```
How do I view system logs, filter by severity or component, and
find specific events on SR Linux?
```

### Prompt 12: Enable debug logging
```
How do I enable debug logging for BGP on SR Linux? What's the
proper way to enable and disable debugging?
```

## Performance Monitoring

### Prompt 13: Interface utilization
```
How do I monitor real-time interface utilization and throughput
statistics on SR Linux?
```

### Prompt 14: Memory usage
```
What commands show memory usage by process and buffer statistics
on SR Linux?
```
