# Multi-Router Configuration Prompts

These prompts generate configurations for multiple routers at once.
Use keywords like "write", "save", or "generate files" to save configs to files.

## Data Center Spine-Leaf

### Prompt 1: Basic spine-leaf (3 routers)
```
Write configurations for a spine-leaf topology with 1 spine and 2 leaf
switches. Configure OSPF area 0 between all nodes. Use sequential loopback
IPs starting at 10.0.0.1/32. Set hostnames as spine-01, leaf-01, leaf-02
```

### Prompt 2: Spine-leaf with BGP (5 routers)
```
Generate configs for 5 routers: 2 spines and 3 leaves. Configure eBGP
between spine and leaf using private ASNs (spine: 65000, leaves: 65001-65003).
Enable ECMP. Set admin user with password "admin123"
```

### Prompt 3: Large spine-leaf (12 routers)
```
Save configurations for 12 routers: 4 spines and 8 leaves. Use eBGP
underlay with unique ASN per device (65001-65012). Configure loopbacks
1.1.1.1-1.1.1.12. Set OSPF as IGP in area 0. Configure hostname pattern
spine-0X and leaf-0X
```

## Service Provider Network

### Prompt 4: Simple ISP core (4 routers)
```
Write configs for 4 PE routers in a service provider network. Configure
IS-IS as IGP with level-2 only. Enable LDP for MPLS. Set up iBGP mesh
in AS 65000 with route reflectors on router1 and router2. Use loopbacks
10.255.0.1-10.255.0.4
```

### Prompt 5: MPLS VPN PE routers (6 routers)
```
Generate configurations for 6 PE routers with MPLS L3VPN capability.
Configure OSPF area 0 as IGP, LDP for label distribution, and MP-BGP
for VPNv4. Create a sample VRF called "CUSTOMER-A" with RD 65000:100
```

## Enterprise Network

### Prompt 6: Campus distribution (4 routers)
```
Write configs for 4 distribution routers in a campus network. Configure
OSPF with area 0 for backbone links and area 1 for access. Enable VRRP
on VLAN interfaces for gateway redundancy. Set STP root priority
```

### Prompt 7: Branch office (3 routers)
```
Save configurations for 3 branch routers connecting to headquarters.
Configure eBGP to HQ with AS 65100 (branches use 65201-65203). Add
default route pointing to HQ. Configure basic QoS with 3 queues
```

## Lab/Testing

### Prompt 8: Quick test topology (3 routers)
```
Write simple test configs for 3 routers in a triangle topology.
Each router connects to the other two. Configure OSPF area 0 on all links.
Use hostnames r1, r2, r3 and loopbacks 1.1.1.1, 2.2.2.2, 3.3.3.3
```

### Prompt 9: Protocol comparison lab (4 routers)
```
Generate configs for 4 routers to compare routing protocols. Configure
OSPF on links between r1-r2 and r2-r3. Configure IS-IS on links between
r3-r4 and r4-r1. Enable redistribution at r2 and r4
```
