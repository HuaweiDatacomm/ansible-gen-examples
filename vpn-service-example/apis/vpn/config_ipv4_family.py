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
- name: config_ipv4_family
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

  - name: config_ipv4_family_example
    config_ipv4_family:
      operation_type: config
      operation_specs: 
        - path: /config/dhcp/relay/global
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/reflector-cluster-ipv4
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/reflector-cluster-id
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/tunnel-selector-name
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/add-path-select-num
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/route-reflector-ext-community-filter
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/common
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/common/route-policy
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/common/filter-name
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/bit-error-detection
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/bit-error-detection/route-policy
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/bit-error-detection/filter-name
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/nexthop-recursive-lookup/bit-error-detection/filter-parameter
          operation: remove
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/afs/af/ipv4-vpn/slow-peer
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af
          operation: create
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af/ipv4-vpn
          operation: create
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af/ipv4-vpn/public-as-only
          operation: create
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af/ipv4-vpn/public-as-only-import
          operation: create
        - path: /config/network-instance/instances/instance[2]/afs/af/vpn-ttlmode
          operation: merge
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/common
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/preference
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route[1]
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route[2]
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/lsp-options
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/slow-peer
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv4-unicast/routing-table-rib-only
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/timer
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/graceful-restart
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/local-graceful-restart
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af/ipv4-unicast
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only-import
          operation: create
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
              name: "_public_"
              bgp: 
                base-process: 
                  afs: 
                    - af: 
                        type: ipv4vpn
                  peers: 
                    - peer: 
                        address: "5.5.5.5"
                        afs: 
                          - af: 
                              type: ipv4vpn
          - instance: 
              name: "vrf_ncc_oc_nat"
              afs: 
                - af: 
                    type: ipv4-unicast
                    vpn-ttlmode: 
                      ttlmode: pipe
              bgp: 
                base-process: 
                  afs: 
                    - af: 
                        type: ipv4uni
                        ipv4-unicast: 
                          common: 
                            auto-frr: false
                            maximum-load-balancing-ibgp: 1
                            maximum-load-balancing-ebgp: 1
                            nexthop-resolve-aigp: false
                            summary-automatic: false
                            best-route-bit-error-detection: false
                            supernet-unicast-advertise: false
                            supernet-label-advertise: true
                            lsp-mtu: 1500
                            label-free-delay: 0
                            bestroute-as-path-ignore: false
                            determin-med: false
                            attribute-set-enable: false
                            load-balanc-igp-metric-ignore: false
                            load-balanc-as-path-ignore: false
                            load-balanc-as-path-relax: false
                            maximum-load-balancing: 1
                            import-rib-nexthop-invariable: false
                            route-relay-tunnel: false
                            bestroute-med-plus-igp: false
                            bestroute-igp-metric-ignore: false
                            bestroute-router-id-prior-clusterlist: false
                            bestroute-med-none-as-maximum: false
                            load-balancing-eibgp-enable: false
                            prefix-origin-as-validation: false
                            advertise-route-mode: all
                            reoriginate-route: false
                            route-select-delay: 0
                            reflect-change-path: false
                            always-compare-med: false
                            default-med: 0
                            nexthop-third-party: false
                            default-local-preference: 100
                            default-route-import: false
                            routerid-neglect: false
                            reflect-between-client: true
                            ext-community-change: false
                            active-route-advertise: false
                            ebgp-interface-sensitive: true
                          preference: 
                            external: 255
                            internal: 255
                            local: 255
                          nexthop-recursive-lookup: 
                            common: 
                              restrain: true
                              default-route: false
                          import-routes: 
                            - import-route: 
                                protocol: direct
                                process-id: 0
                            - import-route: 
                                protocol: static
                                process-id: 0
                                policy-name: "GEN-POL-OUT-VPN-STATIC-TO-MPBGP"
                          lsp-options: 
                            ingress-protect-mode-bgp-frr: false
                            maximum-load-balancing-ingress: 1
                            maximum-load-balancing-transit: 1
                          slow-peer: 
                            detection: true
                            detection-threshold: 300
                            absolute-detection: true
                            absolute-detection-threshold: 9
                          routing-table-rib-only: 
                            enable: false
                  peers: 
                    - peer: 
                        address: "30.0.0.1"
                        remote-as: "65001"
                        ebgp-max-hop: 1
                        local-ifnet-disable: false
                        timer: 
                          keep-alive-time: 60
                          hold-time: 180
                          min-hold-time: 0
                          connect-retry-time: 32
                        graceful-restart: 
                          enable: default
                          peer-reset: default
                        local-graceful-restart: 
                          enable: default
                        afs: 
                          - af: 
                              type: ipv4uni
                              ipv4-unicast: 
                                import-policy: "GEN-POL-OUT-VPN-LOCAL-TO-EBGP"
                                export-policy: "GEN-POL-OUT-VPN-LOCAL-TO-EBGP"
                                route-update-interval: 30
                                public-as-only: 
                                  enable: false
                                public-as-only-import: 
                                  enable: default
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:config_ipv4_family
version_added: "2.6"
short_description: Dynamic Host Configuration Protocol.
                   Layer 3 Virtual Private Network (L3VPN). An L3VPN is a virtual private network set up over public networks by Internet Service Providers 
                   (ISPs) and Network Service Providers (NSPs).
description:
    - Dynamic Host Configuration Protocol.
      Layer 3 Virtual Private Network (L3VPN). An L3VPN is a virtual private network set up over public networks by Internet Service Providers (ISPs) and 
      Network Service Providers (NSPs).
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
                bgp:
                    description:
                        - Configure BGP network instance. All nodes of private VPN Instance in this container can be used only when the value of the global 
                          BGP enabling node (/bgp:bgp/bgp:global/bgp:yang-enable) is set to true.
                    required:False
                    base-process:
                        description:
                            - Enable/disable BGP instances.
                        when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                        required:False
                        afs:
                            description:
                                - List of BGP address family instances.
                            required:False
                            af:
                                description:
                                    - Configure BGP address family instance. In public network instances, all types of address families can be configured. In 
                                      IPv4 VPN instances, the IPv4 unicast, IPv4 flow, and IPv4 labeled unicast address families can be configured. In IPv6 
                                      VPN instances, the IPv6 unicast and IPv6 flow address families can be configured. The IPv4 address family in the BGP 
                                      _public_ VPN instance cannot be deleted.
                                required:False
                                type:
                                    description:
                                        - Address family type of a BGP instance.
                                    required:True
                                    key:True
                                    type:enum
                                    choices:['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan']
                                ipv4-unicast:
                                    description:
                                        - Configure IPv4 unicast options.
                                    when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                    required:False
                                    common:
                                        description:
                                            - Configure IPv4 unicast common options.
                                        required:False
                                        auto-frr:
                                            description:
                                                - Enable/disable BGP Auto FRR. If IP FRR, VPN FRR, and Auto FRR are all enabled, IP FRR and VPN FRR take 
                                                  precedence over Auto FRR. If a route fails to match the routing policy of IP FRR or VPN FRR, Auto FRR takes 
                                                  effect.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        maximum-load-balancing-ibgp:
                                            description:
                                                - Specify the maximum number of equal-cost IBGP routes.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:1
                                            type:int
                                            range:[(1, 65535)]
                                        maximum-load-balancing-ebgp:
                                            description:
                                                - Specify the maximum number of equal-cost EBGP routes.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:1
                                            type:int
                                            range:[(1, 65535)]
                                        nexthop-resolve-aigp:
                                            description:
                                                - Enable/disable route with AIGP attribute for route selection.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        summary-automatic:
                                            description:
                                                - Enable/disable automatic summarization for imported routes. Manual summarization takes precedence over 
                                                  automatic summarization. After automatic summarization is enabled, BGP summarizes routes based on the 
                                                  natural network segment (for example, 10.1.1.1/24 and 10.2.1.1/24 are summarized into 10.0.0.0/8, a Class A 
                                                  address), and sends only the summarized route to peers. This reduces the number of routes.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        best-route-bit-error-detection:
                                            description:
                                                - Enable/disable the function to reroute traffic when a bit error event occurs.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        supernet-unicast-advertise:
                                            description:
                                                - Enable/disable the function to advertise supernet unicast routes.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        supernet-label-advertise:
                                            description:
                                                - Enable/disable the function to advertise supernet labeled routes.
                                            required:False
                                            default:True
                                            type:bool
                                            choices:['true', 'false']
                                        lsp-mtu:
                                            description:
                                                - BGP LSP MTU.
                                            required:False
                                            default:1500
                                            type:int
                                            range:[(46, 65535)]
                                        label-free-delay:
                                            description:
                                                - Label Free Delay.
                                            required:False
                                            default:0
                                            type:int
                                            range:[(0, 180)]
                                        bestroute-as-path-ignore:
                                            description:
                                                - Enable/disable BGP to ignore the AS_Path attribute when selecting the optimal route. By default, BGP uses 
                                                  the AS_Path attribute as one of route selection rules, and a route with a shorter AS_Path is preferred. 
                                                  After bestroute-as-path-ignore is selected, BGP does not compare the AS_Path length.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        determin-med:
                                            description:
                                                - Enable/disable deterministic MED so that the route selection result is relevant to the sequence in which 
                                                  routes are received.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        attribute-set-enable:
                                            description:
                                                - Enable/disable the capability of processing attribute set.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        load-balanc-igp-metric-ignore:
                                            description:
                                                - Enable/disable BGP to ignore the IGP cost of each BGP route to the next hop when selecting routes for load 
                                                  balancing. By default, only the routes with the same IGP cost can participate in load balancing.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        load-balanc-as-path-ignore:
                                            description:
                                                - Enable/disable BGP to ignore the AS_Path of each BGP route to the next hop when selecting routes for load 
                                                  balancing. By default, only the routes with the same AS_Path can participate in load balancing.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        load-balanc-as-path-relax:
                                            description:
                                                - Enable/disable BGP to ignore comparison of AS_Path attributes with the same length. By default, only the 
                                                  routes with the same AS_Path can participate in load balancing.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        maximum-load-balancing:
                                            description:
                                                - Specify the maximum number of equal-cost routes in the BGP routing table. The value can be 1 or an integer 
                                                  greater than 1. The value depends on the associated license. Equal-cost BGP routes can be generated for load 
                                                  balancing only when the BGP routes meet the first nine rules of the route-selection policy and have the same 
                                                  AS-Path attribute.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:1
                                            type:int
                                            range:[(1, 65535)]
                                        import-rib-nexthop-invariable:
                                            description:
                                                - Enable/disable the function to advertise the route without modifying the next-hop.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        route-relay-tunnel:
                                            description:
                                                - Enable/disable unicast route recursive-lookup tunnel.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        bestroute-med-plus-igp:
                                            description:
                                                - Enable/disable the function to add the IGP cost to the next-hop destination to the MED before comparing MED 
                                                  values for path selection.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        bestroute-igp-metric-ignore:
                                            description:
                                                - Enable/disable BGP to ignore the IGP cost of each BGP route to the next hop in route selection. By default, 
                                                  a BGP route with a smaller IGP cost to the next hop is preferred.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        bestroute-router-id-prior-clusterlist:
                                            description:
                                                - Enable/disable BGP to compare originator before clusterlist in route selection.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        bestroute-med-none-as-maximum:
                                            description:
                                                - Enable/disable BGP considers its MED as the largest MED value (4294967295). If a route does not carry MED, 
                                                  BGP considers its MED as the default value (0) during route selection.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        load-balancing-eibgp-enable:
                                            description:
                                                - Enable/disable EIBGP route load balancing.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        prefix-origin-as-validation:
                                            description:
                                                - Enable/disable the BGP prefix origin validation.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        advertise-route-mode:
                                            description:
                                                - VPN advertise route mode.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:all
                                            type:enum
                                            choices:['all', 'best', 'valid']
                                        reoriginate-route:
                                            description:
                                                - Enable/disable route reorigination.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        route-select-delay:
                                            description:
                                                - Route selection delay.
                                            required:False
                                            default:0
                                            type:int
                                            range:[(0, 3600)]
                                        reflect-change-path:
                                            description:
                                                - Enable/disable an RR to use an export policy to change route AS_Path.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        always-compare-med:
                                            description:
                                                - Enable/disable BGP to compare the MEDs of routes from peers in different ASs in route selection. If
                                                  there are multiple reachable routes to the same destination, the route with the smallest MED is preferred. 
                                                  Do not use this option unless different ASs use the same IGP and route selection mode.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        default-med:
                                            description:
                                                - Specify the Multi-Exit-Discriminator (MED) of BGP routes. The value is an integer. This value is valid only 
                                                  for the imported routes and BGP summarized routes on the local router.
                                            required:False
                                            default:0
                                            type:int
                                            range:[(0, 4294967295)]
                                        nexthop-third-party:
                                            description:
                                                - Enable/disable BGP third-party next hop.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        default-local-preference:
                                            description:
                                                - The local preference of BGP routes.
                                            required:False
                                            default:100
                                            type:int
                                            range:[(0, 4294967295)]
                                        default-route-import:
                                            description:
                                                - Enable/disable the function to import default routes into the BGP routing table. Default-route-imported must 
                                                  be used with import-routes so that default routes can be imported to the BGP routing table. If only 
                                                  import-routes is used, no default routes can be added to the BGP routing table. In addition, 
                                                  default-route-imported can only import the default routes in the routing table into the BGP routing table.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        routerid-neglect:
                                            description:
                                                - Enable/disable BGP to ignore router IDs when selecting the optimal route. Comparing router IDs is the last 
                                                  resort in route selection. This means that if one optimal route must be selected and no other parameters can 
                                                  be used to break the tie, router IDs can be used. If this option is selected, the first received route will 
                                                  be selected as the optimal route, and BGP will ignore the router ID and peer address in route selection.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        reflect-between-client:
                                            description:
                                                - Enable/disable route reflection between clients. If clients of a route reflector (RR) are fully meshed, you 
                                                  can disable route reflection among clients to reduce the cost.
                                            required:False
                                            default:True
                                            type:bool
                                            choices:['true', 'false']
                                        ext-community-change:
                                            description:
                                                - Enable/disable the function to change the extended community attribute.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        active-route-advertise:
                                            description:
                                                - Enable/disable the function to advertise the optimal routes in the RM module to peers.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        ebgp-interface-sensitive:
                                            description:
                                                - Enable/disable the function of EBGP interface fast sensing. If this function is enabled, the sessions of 
                                                  directly connected EBGP peers are immediately cleared from the associated interface when the interface 
                                                  becomes down.
                                            required:False
                                            default:True
                                            type:bool
                                            choices:['true', 'false']
                                    preference:
                                        description:
                                            - Configure parameters relating to options for BGP routes preference.
                                        required:False
                                        external:
                                            description:
                                                - Set the protocol priority of EBGP routes. The value is an integer. An EBGP route is the optimal route 
                                                  learned from a peer outside the local AS.
                                            required:False
                                            default:255
                                            type:int
                                            range:[(1, 255)]
                                        internal:
                                            description:
                                                - Set the protocol priority of IBGP routes. The value is an integer. An IBGP route is a route learned from a 
                                                  peer inside the local AS.
                                            required:False
                                            default:255
                                            type:int
                                            range:[(1, 255)]
                                        local:
                                            description:
                                                - Set the protocol priority of a local BGP route. A local route refers to an automatically or manually 
                                                  summarized route.
                                            required:False
                                            default:255
                                            type:int
                                            range:[(1, 255)]
                                    nexthop-recursive-lookup:
                                        description:
                                            - Configure next hop iteration.
                                        required:False
                                        common:
                                            description:
                                                - Configure next hop iteration common options.
                                            required:False
                                            restrain:
                                                description:
                                                    - Enable/disable the function to restrain next hop iteration in case of next hop flapping.
                                                required:False
                                                default:True
                                                type:bool
                                                choices:['true', 'false']
                                            default-route:
                                                description:
                                                    - Enable/disable default route.
                                                required:False
                                                default:False
                                                type:bool
                                                choices:['true', 'false']
                                    import-routes:
                                        description:
                                            - List of imported routes.
                                        required:False
                                        import-route:
                                            description:
                                                - Configure route import. Routes of other protocol types can be imported by BGP. By default, BGP does not 
                                                  import routes of other protocol types.
                                            required:False
                                            protocol:
                                                description:
                                                    - Routing protocol from which routes can be imported.
                                                required:True
                                                key:True
                                                type:enum
                                                choices:['direct', 'ospf', 'isis', 'static', 'rip', 'unr', 'op-route']
                                            process-id:
                                                description:
                                                    - Process ID of an imported routing protocol. The process ID is 0, if the imported routing protocol is 
                                                      direct routes, static routes, UNRs, or OP-routes. The process ID must be specified range from 1 to 
                                                      4294967295, if the imported routing protocol is RIP, OSPF, ISIS.
                                                required:True
                                                key:True
                                                type:int
                                                range:[(0, 4294967295)]
                                            policy-name:
                                                description:
                                                    - When routes are imported from other routing protocols, the route-policy filter can be used to filter the 
                                                      routes and change route attributes.
                                                required:False
                                                type:str
                                                length:[(1, 200)]
                                    lsp-options:
                                        description:
                                            - Configure parameters for lsp.
                                        required:False
                                        ingress-protect-mode-bgp-frr:
                                            description:
                                                - Enable/disable ingress LSP protection mode to FRR.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                                        maximum-load-balancing-ingress:
                                            description:
                                                - Maximum number of ingress LSPs for load balancing. The default value is 1, indicating that this attribute is 
                                                  not configured. Configuring the number of ingress LSPs for load balancing and configuring BGP FRR of ingress 
                                                  LSPs are mutually exclusive.
                                            required:False
                                            default:1
                                            type:int
                                            range:[(1, 65535)]
                                        maximum-load-balancing-transit:
                                            description:
                                                - Maximum number of transit LSPs for load balancing.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:1
                                            type:int
                                            range:[(1, 65535)]
                                    slow-peer:
                                        description:
                                            - Configure peer advertising routes slowly.
                                        required:False
                                        detection:
                                            description:
                                                - Enable/disable detect slow peers.
                                            required:False
                                            default:True
                                            type:bool
                                            choices:['true', 'false']
                                        detection-threshold:
                                            description:
                                                - Specify the time in seconds lagging behind average when a peer is determined to be a slow peer.
                                            required:False
                                            default:300
                                            type:int
                                            range:[(120, 3600)]
                                        absolute-detection:
                                            description:
                                                - Enable/disable absolute-detect slow peers.
                                            required:False
                                            default:True
                                            type:bool
                                            choices:['true', 'false']
                                        absolute-detection-threshold:
                                            description:
                                                - Specify the packet send delay time in second when a peer is determined to be a slow peer.
                                            required:False
                                            default:9
                                            type:int
                                            range:[(3, 3600)]
                                    routing-table-rib-only:
                                        description:
                                            - Configure disable route delivery to the IP routing table.
                                        required:False
                                        enable:
                                            description:
                                                - Enable/disable prevent BGP routes from being added to the IP routing table.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            default:False
                                            type:bool
                                            choices:['true', 'false']
                        peers:
                            description:
                                - List of BGP peers.
                            required:False
                            peer:
                                description:
                                    - Configure a single BGP peer.
                                required:False
                                address:
                                    description:
                                        - Connection address of a peer, which can be an IPv4 or IPv6 address.
                                    required:True
                                    key:True
                                    type:str
                                    length:None
                                remote-as:
                                    description:
                                        - AS number of a peer, which must be selected or group name when creating, and which can be in either two-byte format 
                                          or four-byte format:
                                          The two-byte format is X. X is an integer ranging from 1 to 65535.
                                          The four-byte format is X.Y and X. When the format is X.Y, X and Y are both integers, with the value of X ranging 
                                          from 1 to 65535, and the value of Y ranging from 0 to 65535; when the format is X, X is an interger, with the value 
                                          of X ranging from 1 to 4294967295.
                                          The object cannot be modified.
                                    required:True
                                    mandatory:True
                                    pattern:['((([1-9]\\d{0,8})|([1-3]\\d{9})|(4[0-1]\\d{8})|(42[0-8]\\d{7})|(429[0-3]\\d{6})|(4294[0-8]\\d{5})|(42949[0-5]\\d{4})|(429496[0-6]\\d{3})|(4294967[0-1]\\d{2})|(42949672[0-8]\\d{1})|(429496729[0-5]))|((([1-9]\\d{0,3})|([1-5]\\d{4})|(6[0-4]\\d{3})|(65[0-4]\\d{2})|(655[0-2]\\d)|(6553[0-5]))[\\.](([0-9]\\d{0,3})|([1-5]\\d{4})|(6[0-4]\\d{3})|(65[0-4]\\d{2})|(655[0-2]\\d)|(6553[0-5]))))']
                                    type:str
                                    length:[(1, 11)]
                                ebgp-max-hop:
                                    description:
                                        - Maximum number of hops in an indirect EBGP connection. By default, EBGP connections can be established only between 
                                          directly connected peers. The function must be configured on both ends. By default, value is determined by the 
                                          neighbor type, the default value of EBGP is 1 and the default value of IBGP is 0.
                                    must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                    required:False
                                    type:int
                                    range:[(1, 255)]
                                local-ifnet-disable:
                                    description:
                                        - Enable/disable MPLS local IFNET tunnel creation on a BGP IPv4 peer. By default, MPLS local IFNET tunnels can be 
                                          created on an EBGP peer,but such tunnels cannot be created on an IBGP peer.
                                    required:False
                                    type:bool
                                    choices:['true', 'false']
                                timer:
                                    description:
                                        - Configure BGP peer timer parameters.
                                    required:False
                                    keep-alive-time:
                                        description:
                                            - If the value of a timer changes, the BGP peer relationship between the routers is disconnected. This is because 
                                              the peers need to re-negotiate the Keepalive time and hold time. Therefore, confirm the action before you change 
                                              the value of the timer. The Keepalive time should be at least three times of the hold time.
                                        must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                        required:False
                                        default:60
                                        type:int
                                        range:[(0, 21845)]
                                    hold-time:
                                        description:
                                            - Hold time. The value of the hold time can be 0 or range from 3 to 65535. When setting keepalive-time and 
                                              hold-time, note the following:
                                              1. The values of keepalive-time and hold-time cannot both be 0. Otherwise, the BGP timer becomes invalid. That 
                                              is, BGP does not detect link faults according to the timer.
                                              2. The value of hold-time is much greater than that of keepalive-time, such as, keepalive 1 and hold 65535. If 
                                              the value of hold-time is too large, BGP cannot detect link faults timely.
                                              The priority of a timer is lower than that of a peer timer.
                                              After a connection is established between peers, the values of keepalive-time and hold-time are negotiated by 
                                              the peers. The smaller value of hold-time contained in Open packets of both peers is taken as the value of 
                                              hold-time. The smaller value of the locally set value of keepalive-time and one third of the value of hold-time 
                                              is taken as the value of keepalive-time.
                                        must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                        required:False
                                        default:180
                                        type:int
                                        range:[(0, 65535)]
                                    min-hold-time:
                                        description:
                                            - The minimum hold time is either 0 or an integer ranging from 20 to 65535. If the value is changed, the new value 
                                              takes effect since the next peer relationship establishment. During the peer relationship establishment, the 
                                              local device checks the hold time of the remote end. If the hold time is less than the minimum hold time, the 
                                              local device sends an error packet with error code 02 and subcode 06, and the peer relationship fails to be 
                                              established.
                                        must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                        required:False
                                        default:0
                                        type:int
                                        range:[(0, 65535)]
                                    connect-retry-time:
                                        description:
                                            - ConnectRetry interval.
                                        required:False
                                        default:32
                                        type:int
                                        range:[(1, 65535)]
                                graceful-restart:
                                    description:
                                        - Configure graceful restart.
                                    required:False
                                    enable:
                                        description:
                                            - Enable/disable graceful restart capability.
                                        required:False
                                        default:default
                                        type:enum
                                        choices:['default', 'enable', 'disable']
                                    peer-reset:
                                        description:
                                            - Enable/disable reseting BGP peer graceful.
                                        required:False
                                        default:default
                                        type:enum
                                        choices:['default', 'enable', 'disable']
                                local-graceful-restart:
                                    description:
                                        - Configure local graceful restart.
                                    required:False
                                    enable:
                                        description:
                                            - Enable/disable graceful restart capability.
                                        required:False
                                        default:default
                                        type:enum
                                        choices:['default', 'enable', 'disable']
                                afs:
                                    description:
                                        - List of peers in a specified address family.
                                    required:False
                                    af:
                                        description:
                                            - Configure peer in a specified address family.
                                        required:False
                                        type:
                                            description:
                                                - Specify the address family type to set the peer enable.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:True
                                            key:True
                                            type:enum
                                            choices:['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan']
                                        ipv4-unicast:
                                            description:
                                                - Configure IPv4 unicast options.
                                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:False
                                            import-policy:
                                                description:
                                                    - Specify the filtering policy applied to the routes learned from a peer. By default, no such policy is 
                                                      specified.
                                                required:False
                                                type:str
                                                length:[(1, 200)]
                                            export-policy:
                                                description:
                                                    - Specify the filtering policy applied to the routes to be advertised to a peer. By default, no such 
                                                      policy is specified.
                                                required:False
                                                type:str
                                                length:[(1, 200)]
                                            route-update-interval:
                                                description:
                                                    - Specify the minimum interval at which Update packets are sent. By default, the interval at which Update 
                                                      packets are sent to IBGP peers is 15s,
                                                      and the interval at which Update packets are sent to EBGP peers is 30s. When routes change, a router 
                                                      will send Update packets to notify its peers.
                                                      If a route changes frequently, you can set an interval at which Update packets are sent to prevent the 
                                                      router from sending Update packets each time the route changes.
                                                      This configuration is valid only to the routes learned from peers.
                                                required:False
                                                type:int
                                                range:[(0, 600)]
                                            public-as-only:
                                                description:
                                                    - Configure BGP Remove private AS number from outbound updates parameters.
                                                required:False
                                                enable:
                                                    description:
                                                        - Enable/disable BGP to send Update packets carrying only public AS numbers.
                                                    required:False
                                                    default:False
                                                    type:bool
                                                    choices:['true', 'false']
                                            public-as-only-import:
                                                description:
                                                    - Configure BGP remove private AS number in received BGP update messages parameters.
                                                required:False
                                                enable:
                                                    description:
                                                        - Enable/disable BGP to receive update packets carrying only public AS numbers.
                                                    required:False
                                                    default:default
                                                    type:enum
                                                    choices:['default', 'enable', 'disable']

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/network-instance/instances/instance/name', '/network-instance/instances/instance/afs/af/type', '/network-instance/instances/instance/bgp/base-process/afs/af/type', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/protocol', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/process-id', '/network-instance/instances/instance/bgp/base-process/peers/peer/address', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/type']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/network-instance/instances/instance': ['', '', '/network-instance/instances/instance']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/network-instance/instances/instance/name': ['', '', '/network-instance/instances/instance/name']}, {'/network-instance/instances/instance/afs': ['', '@xmlns="urn:huawei:yang:huawei-l3vpn"', '/network-instance/instances/instance/afs']}, {'/network-instance/instances/instance/bgp': ['', '@xmlns="urn:huawei:yang:huawei-bgp"', '/network-instance/instances/instance/bgp']}, {'/network-instance/instances/instance/afs/af': ['', '', '/network-instance/instances/instance/afs/af']}, {'/network-instance/instances/instance/bgp/base-process': ['', '', '/network-instance/instances/instance/bgp/base-process']}, {'/network-instance/instances/instance/afs/af/type': ['', '', '/network-instance/instances/instance/afs/af/type']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode': ['', '@xmlns="urn:huawei:yang:huawei-mpls-forward"', '/network-instance/instances/instance/afs/af/vpn-ttlmode']}, {'/network-instance/instances/instance/bgp/base-process/afs': ['', '', '/network-instance/instances/instance/bgp/base-process/afs']}, {'/network-instance/instances/instance/bgp/base-process/peers': ['', '', '/network-instance/instances/instance/bgp/base-process/peers']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode': ['', '', '/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode']}, {'/network-instance/instances/instance/bgp/base-process/afs/af': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/type': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/type']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/address': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/address']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/remote-as': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/remote-as']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/ebgp-max-hop': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/ebgp-max-hop']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/local-ifnet-disable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/local-ifnet-disable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/routing-table-rib-only': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/routing-table-rib-only']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/keep-alive-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/keep-alive-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/hold-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/hold-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/min-hold-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/min-hold-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/connect-retry-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/connect-retry-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/peer-reset': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/peer-reset']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/auto-frr': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/auto-frr']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/maximum-load-balancing-ibgp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/maximum-load-balancing-ibgp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/maximum-load-balancing-ebgp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/maximum-load-balancing-ebgp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/nexthop-resolve-aigp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/nexthop-resolve-aigp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/summary-automatic': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/summary-automatic']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/best-route-bit-error-detection': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/best-route-bit-error-detection']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/supernet-unicast-advertise': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/supernet-unicast-advertise']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/supernet-label-advertise': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/supernet-label-advertise']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/lsp-mtu': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/lsp-mtu']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/label-free-delay': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/label-free-delay']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-as-path-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-as-path-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/determin-med': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/determin-med']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/attribute-set-enable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/attribute-set-enable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balanc-igp-metric-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balanc-igp-metric-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balanc-as-path-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balanc-as-path-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balanc-as-path-relax': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balanc-as-path-relax']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/maximum-load-balancing': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/maximum-load-balancing']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/import-rib-nexthop-invariable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/import-rib-nexthop-invariable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/route-relay-tunnel': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/route-relay-tunnel']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-med-plus-igp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-med-plus-igp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-igp-metric-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-igp-metric-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-router-id-prior-clusterlist': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-router-id-prior-clusterlist']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-med-none-as-maximum': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/bestroute-med-none-as-maximum']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balancing-eibgp-enable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/load-balancing-eibgp-enable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/prefix-origin-as-validation': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/prefix-origin-as-validation']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/advertise-route-mode': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/advertise-route-mode']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/reoriginate-route': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/reoriginate-route']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/route-select-delay': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/route-select-delay']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/reflect-change-path': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/reflect-change-path']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/always-compare-med': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/always-compare-med']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/default-med': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/default-med']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/nexthop-third-party': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/nexthop-third-party']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/default-local-preference': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/default-local-preference']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/default-route-import': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/default-route-import']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/routerid-neglect': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/routerid-neglect']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/reflect-between-client': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/reflect-between-client']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/ext-community-change': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/ext-community-change']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/active-route-advertise': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/active-route-advertise']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/ebgp-interface-sensitive': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/common/ebgp-interface-sensitive']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference/external': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference/external']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference/internal': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference/internal']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference/local': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/preference/local']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options/ingress-protect-mode-bgp-frr': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options/ingress-protect-mode-bgp-frr']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options/maximum-load-balancing-ingress': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options/maximum-load-balancing-ingress']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options/maximum-load-balancing-transit': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/lsp-options/maximum-load-balancing-transit']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/detection': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/detection']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/detection-threshold': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/detection-threshold']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/absolute-detection': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/absolute-detection']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/absolute-detection-threshold': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/slow-peer/absolute-detection-threshold']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/routing-table-rib-only/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/routing-table-rib-only/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/type': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/type']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common/restrain': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common/restrain']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common/default-route': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/nexthop-recursive-lookup/common/default-route']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/protocol': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/protocol']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/process-id': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/process-id']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/policy-name': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv4-unicast/import-routes/import-route/policy-name']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/import-policy': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/import-policy']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/export-policy': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/export-policy']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/route-update-interval': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/route-update-interval']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only-import': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only-import']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only-import/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv4-unicast/public-as-only-import/enable']}]

business_tag = ['dhcp', 'network-instance']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4-unicast', 'ipv6-unicast'], 'required': True}), ('vpn-ttlmode', {'type': 'dict', 'options': OrderedDict([('ttlmode', {'choices': ['pipe', 'uniform'], 'default': 'pipe', 'required': False})])})])})])}), ('bgp', {'type': 'dict', 'options': OrderedDict([('base-process', {'type': 'dict', 'options': OrderedDict([('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan'], 'required': True}), ('ipv4-unicast', {'type': 'dict', 'options': OrderedDict([('common', {'type': 'dict', 'options': OrderedDict([('auto-frr', {'type': 'bool', 'required': False}), ('maximum-load-balancing-ibgp', {'type': 'int', 'default': 1, 'required': False}), ('maximum-load-balancing-ebgp', {'type': 'int', 'default': 1, 'required': False}), ('nexthop-resolve-aigp', {'type': 'bool', 'required': False}), ('summary-automatic', {'type': 'bool', 'required': False}), ('best-route-bit-error-detection', {'type': 'bool', 'required': False}), ('supernet-unicast-advertise', {'type': 'bool', 'required': False}), ('supernet-label-advertise', {'type': 'bool', 'default': True, 'required': False}), ('lsp-mtu', {'type': 'int', 'default': 1500, 'required': False}), ('label-free-delay', {'type': 'int', 'required': False}), ('bestroute-as-path-ignore', {'type': 'bool', 'required': False}), ('determin-med', {'type': 'bool', 'required': False}), ('attribute-set-enable', {'type': 'bool', 'required': False}), ('load-balanc-igp-metric-ignore', {'type': 'bool', 'required': False}), ('load-balanc-as-path-ignore', {'type': 'bool', 'required': False}), ('load-balanc-as-path-relax', {'type': 'bool', 'required': False}), ('maximum-load-balancing', {'type': 'int', 'default': 1, 'required': False}), ('import-rib-nexthop-invariable', {'type': 'bool', 'required': False}), ('route-relay-tunnel', {'type': 'bool', 'required': False}), ('bestroute-med-plus-igp', {'type': 'bool', 'required': False}), ('bestroute-igp-metric-ignore', {'type': 'bool', 'required': False}), ('bestroute-router-id-prior-clusterlist', {'type': 'bool', 'required': False}), ('bestroute-med-none-as-maximum', {'type': 'bool', 'required': False}), ('load-balancing-eibgp-enable', {'type': 'bool', 'required': False}), ('prefix-origin-as-validation', {'type': 'bool', 'required': False}), ('advertise-route-mode', {'choices': ['all', 'best', 'valid'], 'default': 'all', 'required': False}), ('reoriginate-route', {'type': 'bool', 'required': False}), ('route-select-delay', {'type': 'int', 'required': False}), ('reflect-change-path', {'type': 'bool', 'required': False}), ('always-compare-med', {'type': 'bool', 'required': False}), ('default-med', {'type': 'int', 'required': False}), ('nexthop-third-party', {'type': 'bool', 'required': False}), ('default-local-preference', {'type': 'int', 'default': 100, 'required': False}), ('default-route-import', {'type': 'bool', 'required': False}), ('routerid-neglect', {'type': 'bool', 'required': False}), ('reflect-between-client', {'type': 'bool', 'default': True, 'required': False}), ('ext-community-change', {'type': 'bool', 'required': False}), ('active-route-advertise', {'type': 'bool', 'required': False}), ('ebgp-interface-sensitive', {'type': 'bool', 'default': True, 'required': False})])}), ('preference', {'type': 'dict', 'options': OrderedDict([('external', {'type': 'int', 'default': 255, 'required': False}), ('internal', {'type': 'int', 'default': 255, 'required': False}), ('local', {'type': 'int', 'default': 255, 'required': False})])}), ('nexthop-recursive-lookup', {'type': 'dict', 'options': OrderedDict([('common', {'type': 'dict', 'options': OrderedDict([('restrain', {'type': 'bool', 'default': True, 'required': False}), ('default-route', {'type': 'bool', 'required': False})])})])}), ('import-routes', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('import-route', {'type': 'dict', 'options': OrderedDict([('protocol', {'choices': ['direct', 'ospf', 'isis', 'static', 'rip', 'unr', 'op-route'], 'required': True}), ('process-id', {'type': 'int', 'required': True}), ('policy-name', {'type': 'str', 'required': False})])})])}), ('lsp-options', {'type': 'dict', 'options': OrderedDict([('ingress-protect-mode-bgp-frr', {'type': 'bool', 'required': False}), ('maximum-load-balancing-ingress', {'type': 'int', 'default': 1, 'required': False}), ('maximum-load-balancing-transit', {'type': 'int', 'default': 1, 'required': False})])}), ('slow-peer', {'type': 'dict', 'options': OrderedDict([('detection', {'type': 'bool', 'default': True, 'required': False}), ('detection-threshold', {'type': 'int', 'default': 300, 'required': False}), ('absolute-detection', {'type': 'bool', 'default': True, 'required': False}), ('absolute-detection-threshold', {'type': 'int', 'default': 9, 'required': False})])}), ('routing-table-rib-only', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False})])})])})])})])}), ('peers', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('peer', {'type': 'dict', 'options': OrderedDict([('address', {'type': 'str', 'required': True}), ('remote-as', {'type': 'str', 'required': True}), ('ebgp-max-hop', {'type': 'int', 'required': False}), ('local-ifnet-disable', {'type': 'bool', 'required': False}), ('timer', {'type': 'dict', 'options': OrderedDict([('keep-alive-time', {'type': 'int', 'default': 60, 'required': False}), ('hold-time', {'type': 'int', 'default': 180, 'required': False}), ('min-hold-time', {'type': 'int', 'required': False}), ('connect-retry-time', {'type': 'int', 'default': 32, 'required': False})])}), ('graceful-restart', {'type': 'dict', 'options': OrderedDict([('enable', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False}), ('peer-reset', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False})])}), ('local-graceful-restart', {'type': 'dict', 'options': OrderedDict([('enable', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False})])}), ('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan'], 'required': True}), ('ipv4-unicast', {'type': 'dict', 'options': OrderedDict([('import-policy', {'type': 'str', 'required': False}), ('export-policy', {'type': 'str', 'required': False}), ('route-update-interval', {'type': 'int', 'required': False}), ('public-as-only', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False})])}), ('public-as-only-import', {'type': 'dict', 'options': OrderedDict([('enable', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False})])})])})])})])})])})])})])})])})])})])})])})])

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
            ('vpn-ttlmode', OrderedDict([('ttlmode', {
                'required': False, 'type': 'enumeration', 'default': 'pipe', 
                'pattern': [], 
                'key': False, 'choices': ['pipe', 'uniform']})]))]))])), 
            ('bgp', OrderedDict([('base-process', OrderedDict([('afs', OrderedDict([('af', OrderedDict([('type', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': True, 'choices': ['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan']}), 
            ('ipv4-unicast', OrderedDict([('common', OrderedDict([('auto-frr', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('maximum-load-balancing-ibgp', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(1, 65535)]}), 
            ('maximum-load-balancing-ebgp', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(1, 65535)]}), 
            ('nexthop-resolve-aigp', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('summary-automatic', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('best-route-bit-error-detection', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('supernet-unicast-advertise', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('supernet-label-advertise', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False}), 
            ('lsp-mtu', {
                'required': False, 'type': 'int', 'default': 1500, 
                'pattern': [], 
                'key': False, 'range': [(46, 65535)]}), 
            ('label-free-delay', {
                'required': False, 'type': 'int', 'default': 0, 
                'pattern': [], 
                'key': False, 'range': [(0, 180)]}), 
            ('bestroute-as-path-ignore', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('determin-med', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('attribute-set-enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('load-balanc-igp-metric-ignore', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('load-balanc-as-path-ignore', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('load-balanc-as-path-relax', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('maximum-load-balancing', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(1, 65535)]}), 
            ('import-rib-nexthop-invariable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('route-relay-tunnel', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('bestroute-med-plus-igp', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('bestroute-igp-metric-ignore', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('bestroute-router-id-prior-clusterlist', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('bestroute-med-none-as-maximum', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('load-balancing-eibgp-enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('prefix-origin-as-validation', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('advertise-route-mode', {
                'required': False, 'type': 'enumeration', 'default': 'all', 
                'pattern': [], 
                'key': False, 'choices': ['all', 'best', 'valid']}), 
            ('reoriginate-route', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('route-select-delay', {
                'required': False, 'type': 'int', 'default': 0, 
                'pattern': [], 
                'key': False, 'range': [(0, 3600)]}), 
            ('reflect-change-path', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('always-compare-med', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('default-med', {
                'required': False, 'type': 'int', 'default': 0, 
                'pattern': [], 
                'key': False, 'range': [(0, 4294967295)]}), 
            ('nexthop-third-party', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('default-local-preference', {
                'required': False, 'type': 'int', 'default': 100, 
                'pattern': [], 
                'key': False, 'range': [(0, 4294967295)]}), 
            ('default-route-import', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('routerid-neglect', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('reflect-between-client', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False}), 
            ('ext-community-change', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('active-route-advertise', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('ebgp-interface-sensitive', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False})])), 
            ('preference', OrderedDict([('external', {
                'required': False, 'type': 'int', 'default': 255, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]}), 
            ('internal', {
                'required': False, 'type': 'int', 'default': 255, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]}), 
            ('local', {
                'required': False, 'type': 'int', 'default': 255, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]})])), 
            ('nexthop-recursive-lookup', OrderedDict([('common', OrderedDict([('restrain', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False}), 
            ('default-route', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})]))])), 
            ('import-routes', OrderedDict([('import-route', OrderedDict([('protocol', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': True, 'choices': ['direct', 'ospf', 'isis', 'static', 'rip', 'unr', 'op-route']}), 
            ('process-id', {
                'required': True, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': True, 'range': [(0, 4294967295)]}), 
            ('policy-name', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(1, 200)]})]))])), 
            ('lsp-options', OrderedDict([('ingress-protect-mode-bgp-frr', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('maximum-load-balancing-ingress', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(1, 65535)]}), 
            ('maximum-load-balancing-transit', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(1, 65535)]})])), 
            ('slow-peer', OrderedDict([('detection', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False}), 
            ('detection-threshold', {
                'required': False, 'type': 'int', 'default': 300, 
                'pattern': [], 
                'key': False, 'range': [(120, 3600)]}), 
            ('absolute-detection', {
                'required': False, 'type': 'boolean', 'default': True, 
                'pattern': [], 
                'key': False}), 
            ('absolute-detection-threshold', {
                'required': False, 'type': 'int', 'default': 9, 
                'pattern': [], 
                'key': False, 'range': [(3, 3600)]})])), 
            ('routing-table-rib-only', OrderedDict([('enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})]))]))]))])), 
            ('peers', OrderedDict([('peer', OrderedDict([('address', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': []}), 
            ('remote-as', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': ['((([1-9]\\d{0,8})|([1-3]\\d{9})|(4[0-1]\\d{8})|(42[0-8]\\d{7})|(429[0-3]\\d{6})|(4294[0-8]\\d{5})|(42949[0-5]\\d{4})|(429496[0-6]\\d{3})|(4294967[0-1]\\d{2})|(42949672[0-8]\\d{1})|(429496729[0-5]))|((([1-9]\\d{0,3})|([1-5]\\d{4})|(6[0-4]\\d{3})|(65[0-4]\\d{2})|(655[0-2]\\d)|(6553[0-5]))[\\.](([0-9]\\d{0,3})|([1-5]\\d{4})|(6[0-4]\\d{3})|(65[0-4]\\d{2})|(655[0-2]\\d)|(6553[0-5]))))'], 
                'key': False, 'length': [(1, 11)]}), 
            ('ebgp-max-hop', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 255)]}), 
            ('local-ifnet-disable', {
                'required': False, 'type': 'boolean', 'default': None, 
                'pattern': [], 
                'key': False}), 
            ('timer', OrderedDict([('keep-alive-time', {
                'required': False, 'type': 'int', 'default': 60, 
                'pattern': [], 
                'key': False, 'range': [(0, 21845)]}), 
            ('hold-time', {
                'required': False, 'type': 'int', 'default': 180, 
                'pattern': [], 
                'key': False, 'range': [(0, 65535)]}), 
            ('min-hold-time', {
                'required': False, 'type': 'int', 'default': 0, 
                'pattern': [], 
                'key': False, 'range': [(0, 65535)]}), 
            ('connect-retry-time', {
                'required': False, 'type': 'int', 'default': 32, 
                'pattern': [], 
                'key': False, 'range': [(1, 65535)]})])), 
            ('graceful-restart', OrderedDict([('enable', {
                'required': False, 'type': 'enumeration', 'default': 'default', 
                'pattern': [], 
                'key': False, 'choices': ['default', 'enable', 'disable']}), 
            ('peer-reset', {
                'required': False, 'type': 'enumeration', 'default': 'default', 
                'pattern': [], 
                'key': False, 'choices': ['default', 'enable', 'disable']})])), 
            ('local-graceful-restart', OrderedDict([('enable', {
                'required': False, 'type': 'enumeration', 'default': 'default', 
                'pattern': [], 
                'key': False, 'choices': ['default', 'enable', 'disable']})])), 
            ('afs', OrderedDict([('af', OrderedDict([('type', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': True, 'choices': ['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan']}), 
            ('ipv4-unicast', OrderedDict([('import-policy', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(1, 200)]}), 
            ('export-policy', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(1, 200)]}), 
            ('route-update-interval', {
                'required': False, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(0, 600)]}), 
            ('public-as-only', OrderedDict([('enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})])), 
            ('public-as-only-import', OrderedDict([('enable', {
                'required': False, 'type': 'enumeration', 'default': 'default', 
                'pattern': [], 
                'key': False, 'choices': ['default', 'enable', 'disable']})]))]))]))]))]))]))]))]))]))]))]))])


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
