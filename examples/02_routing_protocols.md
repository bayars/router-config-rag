# Routing Protocol Prompts

These prompts help configure BGP, OSPF, and IS-IS on SR Linux.

## BGP Configuration

### Prompt 1: Basic eBGP neighbor
```
Configure an eBGP neighbor 10.0.0.2 with AS 65002. My local AS is 65001.
Set the router-id to 1.1.1.1
```

### Prompt 2: iBGP with route reflector
```
Set up iBGP in AS 65000 with this router as a route reflector. Add two
route reflector clients: 10.0.0.2 and 10.0.0.3
```

### Prompt 3: BGP peer group
```
Create a BGP peer-group called "spine-peers" with update-source loopback0,
next-hop-self enabled, and add neighbors 10.0.0.2 and 10.0.0.3 to this group
```

### Prompt 4: BGP with IPv6
```
Configure BGP to support both IPv4 and IPv6 address families. Peer with
neighbor 2001:db8::2 in AS 65002
```

### Prompt 5: BGP export policy
```
Create a routing policy to advertise only prefixes from 172.16.0.0/16 to
BGP neighbors and apply it as an export policy
```

## OSPF Configuration

### Prompt 6: Basic OSPF setup
```
Enable OSPF in area 0.0.0.0 on interfaces ethernet-1/1 and ethernet-1/2.
Set router-id to 1.1.1.1
```

### Prompt 7: OSPF with multiple areas
```
Configure OSPF with area 0 as backbone on ethernet-1/1, and area 1 on
ethernet-1/2 and ethernet-1/3. Make area 1 a stub area
```

### Prompt 8: OSPF interface tuning
```
Configure OSPF on ethernet-1/1 with hello-interval 5 seconds,
dead-interval 20 seconds, and interface cost 100
```

### Prompt 9: OSPF authentication
```
Enable MD5 authentication on OSPF interface ethernet-1/1 with key-id 1
and password "ospf-secret"
```

## IS-IS Configuration

### Prompt 10: Basic IS-IS
```
Configure IS-IS with NET address 49.0001.0000.0000.0001.00, enable on
interfaces ethernet-1/1 and ethernet-1/2 as level-2 only
```

### Prompt 11: IS-IS with segment routing
```
Set up IS-IS with segment routing enabled. Configure SRGB range
16000-23999 and assign node-SID 16001 to this router
```
