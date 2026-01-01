# Basic Configuration Prompts

These prompts help with fundamental SR Linux configuration tasks.

## System Configuration

### Prompt 1: Set hostname and management IP
```
Configure the system hostname as "spine-01" and set the management interface
with IP address 192.168.1.10/24 and default gateway 192.168.1.1
```

### Prompt 2: Configure NTP
```
Set up NTP on SR Linux with server 10.0.0.1 as primary and 10.0.0.2 as backup
```

### Prompt 3: Configure users and authentication
```
Create a user called "netadmin" with password "secure123" and assign
network-admin role permissions
```

### Prompt 4: Configure logging
```
Configure syslog to send logs to server 10.10.10.100 with facility local7
and severity info level
```

## Interface Configuration

### Prompt 5: Basic interface setup
```
Configure ethernet-1/1 with IP address 10.0.0.1/30 and description
"Link to core-router"
```

### Prompt 6: VLAN subinterface
```
Create a subinterface on ethernet-1/2 with VLAN ID 100 and IP address
172.16.100.1/24
```

### Prompt 7: LAG configuration
```
Configure a LAG (Link Aggregation Group) using interfaces ethernet-1/3
and ethernet-1/4 with LACP enabled
```

### Prompt 8: Loopback interface
```
Create a loopback interface with IP address 1.1.1.1/32 for use as
router-id and BGP peering
```
