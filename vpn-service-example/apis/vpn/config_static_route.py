#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#




import sys
from collections import OrderedDict
from ansible.module_utils.network.ne.common_module.ne_base import ConfigBase,GetBase, InputBase
from ansible.module_utils.network.ne.ne import get_nc_config, set_nc_config, ne_argument_spec

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

EXAMPLE = """
---
- name: config_static_route
  hosts: ne_test
  connection: netconf
  gather_facts: no
  vars:
    netconf:
      host: "{{ inventory_hostname }}"
      port: "{{ ansible_ssh_port }}"
      username: "{{ ansible_user }}"
      password: "{{ ansible_ssh_pass }}"
      transport: netconf

  tasks:

  - name: config_static_route_ipv4_example
    config_static_route:
      operation_type: config
      operation_specs: 
        - path: /config/dhcp/relay/global
          operation: merge
        - path: /config/network-instance/instances/instance/afs/af[1]/routing/static-routing/unicast-route2s/unicast-route2
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/vpn-ttlmode
          operation: merge
        - path: /config/network-instance/instances/instance/afs/af[2]/vpn-ttlmode
          operation: merge
        - path: /config/routing/static-routing/ipv4-site
          operation: merge
        - path: /config/routing/static-routing/ipv4-relay-tunnel
          operation: merge
        - path: /config/routing/static-routing/ipv6-site
          operation: merge
      dhcp: 
        relay: 
          global: 
            user-detect-interval: 20
            user-autosave-flag: false
            user-store-interval: 300
            distribute-flag: false
            opt82-inner-vlan-insert-flag: false
      network-instance: 
        instances: 
          - instance: 
              name: "vrf_ncc_oc_nat"
              afs: 
                - af: 
                    type: ipv4-unicast
                    routing: 
                      static-routing: 
                        unicast-route2s: 
                          - unicast-route2: 
                              topology-name: "base"
                              prefix: "51.1.1.0"
                              mask-length: 24
                              nexthop-addresses: 
                                - nexthop-address: 
                                    address: "192.168.51.2"
                                    preference: 60
                                    tag: 110
                    vpn-ttlmode: 
                      ttlmode: pipe
                - af: 
                    type: ipv6-unicast
                    vpn-ttlmode: 
                      ttlmode: pipe
      routing: 
        static-routing: 
          ipv4-site: 
            preference: 60
            relay-switch: false
            min-tx-interval: 50
            min-rx-interval: 50
            multiplier: 3
            relay-remote: true
            relay-arp-vlink: false
            inherit-cost-switch: false
            relay-srv6-nexthop: false
          ipv4-relay-tunnel: 
            enable: false
          ipv6-site: 
            preference: 60
            min-tx-interval: 50
            min-rx-interval: 50
            multiplier: 3
            relay-arp-vlink6: false
            relay-srv6-nexthop6: false
      provider: "{{ netconf }}"

  - name: config_static_route_ipv6_example
    config_static_route:
      operation_type: config
      operation_specs: 
        - path: /config/dhcp/relay/global
          operation: merge
        - path: /config/network-instance/instances/instance/afs/af[1]/vpn-ttlmode
          operation: merge
        - path: /config/network-instance/instances/instance/afs/af[2]/routing/static-routing/unicast-route2s/unicast-route2
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/vpn-ttlmode
          operation: merge
        - path: /config/routing/static-routing/ipv4-site
          operation: merge
        - path: /config/routing/static-routing/ipv4-relay-tunnel
          operation: merge
        - path: /config/routing/static-routing/ipv6-site
          operation: merge
      dhcp: 
        relay: 
          global: 
            user-detect-interval: 20
            user-autosave-flag: false
            user-store-interval: 300
            distribute-flag: false
            opt82-inner-vlan-insert-flag: false
      network-instance: 
        instances: 
          - instance: 
              name: "vrf_ncc_oc_nat"
              afs: 
                - af: 
                    type: ipv4-unicast
                    vpn-ttlmode: 
                      ttlmode: pipe
                - af: 
                    type: ipv6-unicast
                    routing: 
                      static-routing: 
                        unicast-route2s: 
                          - unicast-route2: 
                              topology-name: "base"
                              prefix: "AA:51::"
                              mask-length: 64
                              nexthop-addresses: 
                                - nexthop-address: 
                                    address: "2A01:C000:83:B000:10:20:51:1"
                                    preference: 60
                                    tag: 181
                    vpn-ttlmode: 
                      ttlmode: pipe
      routing: 
        static-routing: 
          ipv4-site: 
            preference: 60
            relay-switch: false
            min-tx-interval: 50
            min-rx-interval: 50
            multiplier: 3
            relay-remote: true
            relay-arp-vlink: false
            inherit-cost-switch: false
            relay-srv6-nexthop: false
          ipv4-relay-tunnel: 
            enable: false
          ipv6-site: 
            preference: 60
            min-tx-interval: 50
            min-rx-interval: 50
            multiplier: 3
            relay-arp-vlink6: false
            relay-srv6-nexthop6: false
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:config_static_route
version_added: "2.6"
short_description: Dynamic Host Configuration Protocol.
                   Layer 3 Virtual Private Network (L3VPN). An L3VPN is a virtual private network set up over public networks by Internet Service Providers 
                   (ISPs) and Network Service Providers (NSPs).
                   This YANG module defines essential components for the management
                   of a routing subsystem.
description:
    - Dynamic Host Configuration Protocol.
      Layer 3 Virtual Private Network (L3VPN). An L3VPN is a virtual private network set up over public networks by Internet Service Providers (ISPs) and 
      Network Service Providers (NSPs).
      This YANG module defines essential components for the management
      of a routing subsystem.
author:ansible_team@huawei
time:2021-10-28 09:58:12
options:
    opreation_type:config
        description:config
            - This is a helper node ,Choose from config, get
        type: str
        required:True
        choices: ["config","get","get-config","input_action"]
    dhcp:
        description:
            - Configure Dynamic Host Configuration Protocol.
        required:False
        relay:
            description:
                - Configure DHCP relay.
            required:False
            global:
                description:
                    - Configure DHCP relay global attributes.
                required:False
                user-detect-interval:
                    description:
                        - DHCP relay ARP user-detect interval.
                    required:False
                    default:20
                    type:int
                    range:[(0, 60)]
                user-autosave-flag:
                    description:
                        - Enable/disable a DHCP relay agent to store user entries.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                user-store-interval:
                    description:
                        - DHCP relay unnumbered table write-delay.
                    required:False
                    default:300
                    type:int
                    range:[(300, 86400)]
                distribute-flag:
                    description:
                        - Enable/disable DHCP relay distribute flag.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                opt82-inner-vlan-insert-flag:
                    description:
                        - Enable/disable DHCP option82 inner-VLAN change flag.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
    network-instance:
        description:
            - Layer 3 Virtual Private Network (L3VPN). An L3VPN is a virtual private network set up over public networks by Internet Service Providers (ISPs) 
              and Network Service Providers (NSPs).
        required:False
        instances:
            description:
                - List of VPN instances. VPN instances are established to separate VPN routes from public network routes, and separate the routes of different 
                  VPNs. Some software features can be bound to multiple VPN instances so that multiple instances can provide a same feature. For example, RIP, 
                  OSPF, IS-IS, and BGP multiple instances.
            required:False
            instance:
                description:
                    - Configure VPN instances. VPN instances are established to separate VPN routes from public network routes, and separate the routes of 
                      different VPNs. Multiple software features can be bound to multiple VPN instances to form a multi-instance that provides multiple 
                      features, for example, RIP multi-instance, OSPF multi-instance, IS-IS multi-instance, and BGP multi-instance. The _public_, dcn, ason, 
                      __mpp_vpn_inner__, __mpp_vpn_outer__, __mpp_vpn_inner_server__, and __LOCAL_OAM_VPN__ instances cannot be deleted.
                required:False
                name:
                    description:
                        - VPN instance name. It uniquely identifies a VPN instance. The name is a string of case-sensitive characters.
                    required:True
                    key:True
                    type:str
                    length:[(1, 31)]
                afs:
                    description:
                        - List of VPN address families. A VPN instance supports the
                          configurations and functions of an address family only
                          after the address family is configured on the instance.
                    required:False
                    af:
                        description:
                            - Configure address families of the VPN instance. A VPN instance
                              supports the configurations and functions of an
                              address family only after the address family is
                              configured on the instance. Neither of the address
                              families in the _public_ VPN instance can be deleted.
                              If either of a VPN instance's IPv4 and IPv6 address
                              families is referenced by BGP, the referenced address
                              family cannot be deleted. If one of the address
                              families is referenced by BGP, the non-referenced
                              address family in the VPN instance can be deleted.
                              If the VPN instance is referenced by BGP but its
                              address families are not referenced by BGP, neither
                              address family can be deleted.
                        required:False
                        type:
                            description:
                                - Types of the VPN address families.
                            required:True
                            key:True
                            type:enum
                            choices:['ipv4-unicast', 'ipv6-unicast']
                        routing:
                            description:
                                - Configure routing management.
                            required:False
                            static-routing:
                                description:
                                    - Configure a basic service package for static routes.
                                required:False
                                unicast-route2s:
                                    description:
                                        - List of configured static routes.
                                    required:False
                                    unicast-route2:
                                        description:
                                            - Configure static routes. Static routes can be configured on a network with a simple topology to ensure normal 
                                              running of the network, and can be configured when a router cannot run dynamic routing protocols or cannot 
                                              generate routes to destination networks. Reasonable configuration of static routes can improve network 
                                              performance and ensure bandwidths for important services.
                                        required:False
                                        topology-name:
                                            description:
                                                - Name of the specified topology.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:True
                                            key:True
                                            type:str
                                            length:[(1, 31)]
                                        prefix:
                                            description:
                                                - Destination IP address.
                                            required:True
                                            key:True
                                            type:str
                                            length:None
                                        mask-length:
                                            description:
                                                - Mask length of an IP address.
                                            required:True
                                            key:True
                                            type:int
                                            range:[(0, 128)]
                                        nexthop-addresses:
                                            description:
                                                - List of next hops.
                                            required:False
                                            nexthop-address:
                                                description:
                                                    - Configure next hops.
                                                must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                                required:False
                                                address:
                                                    description:
                                                        - Next hop IP address of a route.
                                                    must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                                    required:True
                                                    key:True
                                                    type:str
                                                    length:None
                                                preference:
                                                    description:
                                                        - Priority of a static route. If the parameter is not configured, the global default value is used.
                                                          To change the global default priority of IPv4 static routes, use the 
                                                          /rt:routing/rt:static-routing/rt:ipv4-site/rt:preference object or the PAF file. The global default 
                                                          priority varies according to hardware. To query the default value, you can perform a get operation.
                                                          To change the global default priority of IPv6 static routes, use the 
                                                          /rt:routing/rt:static-routing/rt:ipv6-site/rt:preference object or the PAF file. The global default 
                                                          priority varies according to hardware. To query the default value, you can perform a get operation.
                                                    required:False
                                                    type:int
                                                    range:[(1, 255)]
                                                tag:
                                                    description:
                                                        - Tag of a static route.
                                                    required:False
                                                    type:int
                                                    range:[(1, 4294967295)]
                        vpn-ttlmode:
                            description:
                                - Configure TTL mode.
                            required:False
                            ttlmode:
                                description:
                                    - TTL mode value.
                                required:False
                                default:pipe
                                type:enum
                                choices:['pipe', 'uniform']
    routing:
        description:
            - Configuration parameters for the routing module.
        required:False
        static-routing:
            description:
                - Configure a basic service package for static routes.
            required:False
            ipv4-site:
                description:
                    - Configure parameters for IPv4 static routes.
                required:False
                preference:
                    description:
                        - Default priority of IPv4 static routes. The default value can be controlled by the PAF file and varies according to hardware. To 
                          query the default value, you can perform a get operation.
                    required:False
                    type:int
                    range:[(1, 255)]
                relay-switch:
                    description:
                        - Enable/disable the function of selecting static routes based on recursion depths.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                min-tx-interval:
                    description:
                        - Default minimum interval expected at which IPv4 BFD packets are sent to the peer end. The default value can be controlled by the PAF 
                          file and varies according to hardware.
                    required:False
                    type:int
                    range:[(0, 4294967295)]
                min-rx-interval:
                    description:
                        - Default minimum interval expected at which IPv4 BFD packets are received from the peer end. The default value can be controlled by 
                          the PAF file and varies according to hardware.
                    required:False
                    type:int
                    range:[(0, 4294967295)]
                multiplier:
                    description:
                        - IPv4 Local detection multiplier.
                    required:False
                    default:3
                    type:int
                    range:[(3, 50)]
                relay-remote:
                    description:
                        - Enable/disable the function of recursing IPv4 unicast static routes to remotely leaked VPN routes.
                    required:False
                    default:True
                    type:bool
                    choices:['true', 'false']
                relay-arp-vlink:
                    description:
                        - Enable/disable the function of recursing IPv4 unicast static routes to ARP Vlink routes.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                inherit-cost-switch:
                    description:
                        - Enable/disable the function of comparing the costs of inherited routes during static route selection.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                relay-srv6-nexthop:
                    description:
                        - Enable/disable the function of recursing IPv4 unicast static routes to SRv6 routes.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
            ipv4-relay-tunnel:
                description:
                    - Configure route recursion to tunnel.
                required:False
                enable:
                    description:
                        - Enable/disable route recursion to tunnel. By default, this configuration takes effect for all routes. If an IP prefix list is 
                          configured, the configuration takes effect only for the routes that match the IP prefix list. If a tunnel policy is configured, 
                          routes carry the tunnel policy information when recursing to a tunnel.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
            ipv6-site:
                description:
                    - Configure parameters for IPv6 static routes.
                required:False
                preference:
                    description:
                        - Default priority of IPv6 static routes. The default value can be controlled by the PAF file and varies according to hardware. To 
                          query the default value, you can perform a get operation.
                    required:False
                    type:int
                    range:[(1, 255)]
                min-tx-interval:
                    description:
                        - Default minimum interval expected at which IPv6 BFD packets are sent to the peer end. The default value can be controlled by the PAF 
                          file and varies according to hardware.
                    required:False
                    type:int
                    range:[(0, 4294967295)]
                min-rx-interval:
                    description:
                        - Default minimum interval expected at which IPv6 BFD packets are received from the peer end. The default value can be controlled by 
                          the PAF file and varies according to hardware.
                    required:False
                    type:int
                    range:[(0, 4294967295)]
                multiplier:
                    description:
                        - IPv6 Local detection multiplier.
                    required:False
                    default:3
                    type:int
                    range:[(3, 50)]
                relay-arp-vlink6:
                    description:
                        - Enable/disable the function of recursing IPv6 unicast static routes to ARP Vlink routes.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                relay-srv6-nexthop6:
                    description:
                        - Enable/disable the function of recursing IPv6 unicast static routes to SRv6 routes.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/network-instance/instances/instance/name', '/network-instance/instances/instance/afs/af/type', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/topology-name', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/prefix', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/mask-length', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/address']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/routing': ['', '@xmlns="urn:huawei:yang:huawei-routing"', '/routing']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/routing/static-routing': ['', '', '/routing/static-routing']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/network-instance/instances/instance': ['', '', '/network-instance/instances/instance']}, {'/routing/static-routing/ipv4-site': ['', '', '/routing/static-routing/ipv4-site']}, {'/routing/static-routing/ipv4-relay-tunnel': ['', '', '/routing/static-routing/ipv4-relay-tunnel']}, {'/routing/static-routing/ipv6-site': ['', '', '/routing/static-routing/ipv6-site']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/network-instance/instances/instance/name': ['', '', '/network-instance/instances/instance/name']}, {'/network-instance/instances/instance/afs': ['', '@xmlns="urn:huawei:yang:huawei-l3vpn"', '/network-instance/instances/instance/afs']}, {'/routing/static-routing/ipv4-site/preference': ['', '', '/routing/static-routing/ipv4-site/preference']}, {'/routing/static-routing/ipv4-site/relay-switch': ['', '', '/routing/static-routing/ipv4-site/relay-switch']}, {'/routing/static-routing/ipv4-site/min-tx-interval': ['', '', '/routing/static-routing/ipv4-site/min-tx-interval']}, {'/routing/static-routing/ipv4-site/min-rx-interval': ['', '', '/routing/static-routing/ipv4-site/min-rx-interval']}, {'/routing/static-routing/ipv4-site/multiplier': ['', '', '/routing/static-routing/ipv4-site/multiplier']}, {'/routing/static-routing/ipv4-site/relay-remote': ['', '', '/routing/static-routing/ipv4-site/relay-remote']}, {'/routing/static-routing/ipv4-site/relay-arp-vlink': ['', '', '/routing/static-routing/ipv4-site/relay-arp-vlink']}, {'/routing/static-routing/ipv4-site/inherit-cost-switch': ['', '', '/routing/static-routing/ipv4-site/inherit-cost-switch']}, {'/routing/static-routing/ipv4-site/relay-srv6-nexthop': ['', '', '/routing/static-routing/ipv4-site/relay-srv6-nexthop']}, {'/routing/static-routing/ipv4-relay-tunnel/enable': ['', '', '/routing/static-routing/ipv4-relay-tunnel/enable']}, {'/routing/static-routing/ipv6-site/preference': ['', '', '/routing/static-routing/ipv6-site/preference']}, {'/routing/static-routing/ipv6-site/min-tx-interval': ['', '', '/routing/static-routing/ipv6-site/min-tx-interval']}, {'/routing/static-routing/ipv6-site/min-rx-interval': ['', '', '/routing/static-routing/ipv6-site/min-rx-interval']}, {'/routing/static-routing/ipv6-site/multiplier': ['', '', '/routing/static-routing/ipv6-site/multiplier']}, {'/routing/static-routing/ipv6-site/relay-arp-vlink6': ['', '', '/routing/static-routing/ipv6-site/relay-arp-vlink6']}, {'/routing/static-routing/ipv6-site/relay-srv6-nexthop6': ['', '', '/routing/static-routing/ipv6-site/relay-srv6-nexthop6']}, {'/network-instance/instances/instance/afs/af': ['', '', '/network-instance/instances/instance/afs/af']}, {'/network-instance/instances/instance/afs/af/type': ['', '', '/network-instance/instances/instance/afs/af/type']}, {'/network-instance/instances/instance/afs/af/routing': ['', '@xmlns="urn:huawei:yang:huawei-routing"', '/network-instance/instances/instance/afs/af/routing']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode': ['', '@xmlns="urn:huawei:yang:huawei-mpls-forward"', '/network-instance/instances/instance/afs/af/vpn-ttlmode']}, {'/network-instance/instances/instance/afs/af/routing/static-routing': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode': ['', '', '/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/topology-name': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/topology-name']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/prefix': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/prefix']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/mask-length': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/mask-length']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/address': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/address']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/preference': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/preference']}, {'/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/tag': ['', '', '/network-instance/instances/instance/afs/af/routing/static-routing/unicast-route2s/unicast-route2/nexthop-addresses/nexthop-address/tag']}]

business_tag = ['dhcp', 'network-instance', 'routing']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4-unicast', 'ipv6-unicast'], 'required': True}), ('routing', {'type': 'dict', 'options': OrderedDict([('static-routing', {'type': 'dict', 'options': OrderedDict([('unicast-route2s', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('unicast-route2', {'type': 'dict', 'options': OrderedDict([('topology-name', {'type': 'str', 'required': True}), ('prefix', {'type': 'str', 'required': True}), ('mask-length', {'type': 'int', 'required': True}), ('nexthop-addresses', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('nexthop-address', {'type': 'dict', 'options': OrderedDict([('address', {'type': 'str', 'required': True}), ('preference', {'type': 'int', 'required': False}), ('tag', {'type': 'int', 'required': False})])})])})])})])})])})])}), ('vpn-ttlmode', {'type': 'dict', 'options': OrderedDict([('ttlmode', {'choices': ['pipe', 'uniform'], 'default': 'pipe', 'required': False})])})])})])})])})])})])}), ('routing', {'type': 'dict', 'options': OrderedDict([('static-routing', {'type': 'dict', 'options': OrderedDict([('ipv4-site', {'type': 'dict', 'options': OrderedDict([('preference', {'type': 'int', 'required': False}), ('relay-switch', {'type': 'bool', 'required': False}), ('min-tx-interval', {'type': 'int', 'required': False}), ('min-rx-interval', {'type': 'int', 'required': False}), ('multiplier', {'type': 'int', 'default': 3, 'required': False}), ('relay-remote', {'type': 'bool', 'default': True, 'required': False}), ('relay-arp-vlink', {'type': 'bool', 'required': False}), ('inherit-cost-switch', {'type': 'bool', 'required': False}), ('relay-srv6-nexthop', {'type': 'bool', 'required': False})])}), ('ipv4-relay-tunnel', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False})])}), ('ipv6-site', {'type': 'dict', 'options': OrderedDict([('preference', {'type': 'int', 'required': False}), ('min-tx-interval', {'type': 'int', 'required': False}), ('min-rx-interval', {'type': 'int', 'required': False}), ('multiplier', {'type': 'int', 'default': 3, 'required': False}), ('relay-arp-vlink6', {'type': 'bool', 'required': False}), ('relay-srv6-nexthop6', {'type': 'bool', 'required': False})])})])})])})])

# Operation type
operation_dict = {'operation_type':{'type': 'str', 'required':True, 'choices': ['config','get','get-config','rpc']},
                  'operation_specs': {
                      'elements': 'dict', 'type': 'list','options': {
                          'path': {
                              'type': 'str'}, 'operation': {
                              'choices': ['merge', 'replace', 'create', 'delete', 'remove'],'default':'merge'}}}}

# Parameters passed to check params
leaf_info =  OrderedDict([('dhcp', OrderedDict([('relay', OrderedDict([('global', OrderedDict([('user-detect-interval', {
                'required': False, 'type': 'int', 'default': 20, 
                'pattern': [], 
                'key': False, 'range': [(0, 60)]}), 
            ('user-autosave-flag', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('user-store-interval', {
                'required': False, 'type': 'int', 'default': 300, 
                'pattern': [], 
                'key': False, 'range': [(300, 86400)]}), 
            ('distribute-flag', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('opt82-inner-vlan-insert-flag', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})]))]))])), 
            ('network-instance', OrderedDict([('instances', OrderedDict([('instance', OrderedDict([('name', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(1, 31)]}), 
            ('afs', OrderedDict([('af', OrderedDict([('type', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': True, 'choices': ['ipv4-unicast', 'ipv6-unicast']}), 
            ('routing', OrderedDict([('static-routing', OrderedDict([('unicast-route2s', OrderedDict([('unicast-route2', OrderedDict([('topology-name', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(1, 31)]}), 
            ('prefix', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': []}), 
            ('mask-length', {
                'required': True, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': True, 'range': [(0, 128)]}), 
            ('nexthop-addresses', OrderedDict([('nexthop-address', OrderedDict([('address', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': []}), 
            ('preference', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]}), 
            ('tag', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 4294967295)]})]))]))]))]))]))])), 
            ('vpn-ttlmode', OrderedDict([('ttlmode', {
                'required': False, 'type': 'enumeration', 'default': 'pipe', 
                'pattern': [], 
                'key': False, 'choices': ['pipe', 'uniform']})]))]))]))]))]))])), 
            ('routing', OrderedDict([('static-routing', OrderedDict([('ipv4-site', OrderedDict([('preference', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]}), 
            ('relay-switch', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('min-tx-interval', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(0, 4294967295)]}), 
            ('min-rx-interval', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(0, 4294967295)]}), 
            ('multiplier', {
                'required': False, 'type': 'int', 'default': 3, 
                'pattern': [], 
                'key': False, 'range': [(3, 50)]}), 
            ('relay-remote', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False}), 
            ('relay-arp-vlink', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('inherit-cost-switch', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('relay-srv6-nexthop', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})])), 
            ('ipv4-relay-tunnel', OrderedDict([('enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})])), 
            ('ipv6-site', OrderedDict([('preference', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]}), 
            ('min-tx-interval', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(0, 4294967295)]}), 
            ('min-rx-interval', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(0, 4294967295)]}), 
            ('multiplier', {
                'required': False, 'type': 'int', 'default': 3, 
                'pattern': [], 
                'key': False, 'range': [(3, 50)]}), 
            ('relay-arp-vlink6', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('relay-srv6-nexthop6', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})]))]))]))])


# User check params
class UserCheck(object):
    def __init__(self, params, infos):
        #  user configuration get from AnsibleModule().params
        self.params = params
        # leaf infos from yang files
        self.infos = infos

    # user defined check method need startswith "check_"
    # return 0 if not pass check logic, else 1
    def check_leaf_restrict(self):
        """
            if leaf_1 configured, leaf2 shouble be configured
            and range shouble be in [10, 20]
        """
        return 1   


# Call the ConfigBase base class
def config_base(config_args):
    class_object = ConfigBase(*config_args)
    class_object.run()


# Call the GetBase base class
def get_base(get_args):
    class_object = GetBase(*get_args)
    class_object.run()

def input_base(input_args):
    class_object = InputBase(*input_args)
    class_object.run()


# According to the type of message
def operation(operation_type,args):
    if operation_type == 'config':
        config_base(args)
    elif operation_type == 'get' or operation_type == 'get-config':
        get_base(args)
    else:
        input_base(args)


def filter_check(user_check_obj):
    return (list(
        filter(lambda m: m.startswith("check_"), [i + '()' for i in dir(user_check_obj)])))


def main():
    """Module main"""
    argument_spec.update(ne_argument_spec)
    argument_spec.update(operation_dict)
    args = (argument_spec, leaf_info, namespaces, business_tag, xml_head,xml_tail,key_list)
    module_params = ConfigBase(*args).get_operation_type()
    for check_func in filter_check(UserCheck):
        if not eval('UserCheck(module_params, leaf_info).' + check_func):
            ConfigBase(*args).init_module().fail_json(msg='UserCheck.'+ check_func)
    operation(module_params['operation_type'], args)


if __name__ == '__main__':
    main()
