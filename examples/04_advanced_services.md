# Advanced Services Prompts

These prompts cover EVPN, VXLAN, VPN services, and advanced features.

## EVPN-VXLAN

### Prompt 1: Basic EVPN-VXLAN fabric
```
Configure EVPN-VXLAN for a layer 2 service. Create mac-vrf "TENANT-1"
with VNI 10001. Set up BGP EVPN peering to spine at 10.0.0.1. Enable
VXLAN interface with source IP from loopback
```

### Prompt 2: EVPN with IRB (Layer 3)
```
Set up EVPN-VXLAN with integrated routing and bridging (IRB). Create
mac-vrf for VLAN 100 with VNI 100100. Create ip-vrf "VRF-PROD" and
associate IRB interface. Configure anycast gateway 192.168.100.1/24
```

### Prompt 3: EVPN multi-homing
```
Configure EVPN multi-homing for dual-connected host. Set up ethernet
segment ES-1 with ESI 00:11:22:33:44:55:66:77:88:99. Enable all-active
multi-homing with LACP
```

## MPLS Services

### Prompt 4: MPLS LDP configuration
```
Enable MPLS with LDP on SR Linux. Configure LDP on interfaces ethernet-1/1
and ethernet-1/2. Set transport address to loopback IP 10.0.0.1
```

### Prompt 5: L3VPN configuration
```
Configure an MPLS L3VPN service. Create VRF "CUSTOMER-B" with RD 65000:200
and RT import/export 65000:200. Add interface ethernet-1/5.100 to the VRF.
Configure MP-BGP VPNv4 peering
```

### Prompt 6: VPLS service
```
Set up a VPLS service for layer 2 VPN. Create VPLS instance "L2VPN-1"
with service ID 1001. Add PE neighbors 10.0.0.2 and 10.0.0.3 as
pseudowire endpoints
```

## Segment Routing

### Prompt 7: SR-MPLS with IS-IS
```
Configure Segment Routing with MPLS data plane using IS-IS as IGP.
Set SRGB 16000-23999, assign prefix-SID 16001 to loopback. Enable
TI-LFA for fast reroute
```

### Prompt 8: SR-TE policy
```
Create an SR-TE policy to route traffic via specific path. Define
explicit segment list through nodes with SIDs 16002, 16003, 16004.
Apply policy for traffic to destination 10.10.10.0/24
```

## QoS and Traffic Management

### Prompt 9: Basic QoS policy
```
Configure QoS with 4 traffic classes: network-control (strict priority),
real-time (40% bandwidth), business (40%), best-effort (20%). Apply
DSCP-based classification
```

### Prompt 10: Interface rate limiting
```
Configure ingress rate limiting on ethernet-1/1 to 1 Gbps with burst
size of 10MB. Apply egress shaping to 500 Mbps
```

## ACL and Security

### Prompt 11: IPv4 ACL
```
Create an IPv4 ACL to permit SSH (port 22) and HTTPS (port 443) from
management network 10.0.0.0/8, permit ICMP, and deny all other traffic.
Apply to management interface
```

### Prompt 12: Control plane protection
```
Configure control plane policing to protect the CPU. Rate-limit ICMP
to 1000 pps, BGP to 5000 pps, OSPF to 5000 pps, SSH to 100 pps
```
