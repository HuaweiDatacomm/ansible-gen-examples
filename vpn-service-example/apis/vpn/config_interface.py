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
- name: config_interface
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

  - name: config_interface_example
    config_interface:
      operation_type: config
      operation_specs: 
        - path: /config/dhcp/relay/global
          operation: merge
        - path: /config/ifm/interfaces/interface
          operation: create
        - path: /config/ifm/interfaces/interface/ipv4/addresses/address
          operation: create
        - path: /config/ifm/interfaces/interface/ipv6
          operation: create
        - path: /config/ifm/interfaces/interface/ipv6/addresses/address
          operation: create
        - path: /config/ifm/interfaces/interface/ipv6/nd-collection/if-property
          operation: create
        - path: /config/ifm/interfaces/interface/ipv6/nd-collection/proxys
          operation: create
        - path: /config/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control
          operation: create
        - path: /config/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q
          operation: create
        - path: /config/ifm/interfaces/interface/multicast-bas
          operation: create
        - path: /config/network-instance/instances/instance
          operation: merge
        - path: /config/network-instance/instances/instance/description
          operation: remove
      dhcp: 
        relay: 
          global: 
            user-detect-interval: 20
            user-autosave-flag: false
            user-store-interval: 300
            distribute-flag: false
            opt82-inner-vlan-insert-flag: false
      ifm: 
        interfaces: 
          - interface: 
              name: "GigabitEthernet0/3/8.4091"
              class: sub-interface
              type: GigabitEthernet
              parent-name: "GigabitEthernet0/3/8"
              number: "4091"
              description: "OC Customer Access"
              admin-status: up
              link-protocol: ethernet
              router-type: broadcast
              statistic-enable: false
              vrf-name: "vrf_ncc_oc_nat"
              ipv4: 
                addresses: 
                  - address: 
                      ip: "192.168.51.1"
                      mask: "255.255.255.252"
                      type: main
              ipv6: 
                spread-mtu-flag: false
                auto-link-local: false
                addresses: 
                  - address: 
                      ip: "2A01:C000:83:B000:10:20:51:0"
                      prefix-length: 127
                      type: global
                nd-collection: 
                  if-property: 
                    retrans-timer: 1000
                    nud-reach-time: 1200000
                    attempts-value: 1
                    max-dyn-nb-num: 0
                    nud-attempts: 3
                    na-glean: off
                    ma-flag: off
                    o-flag: off
                    ra-halt-flag: on
                    max-interval: 600
                    ra-preference: medium
                    ra-prefix-flag: on
                    ra-mtu-flag: on
                    strict-flag: false
                    ts-fuzz-factor: 1
                    ts-clock-drift: 1
                    ts-delta: 300
                    rsa-min-key-len: 512
                    rsa-max-key-len: 2048
                    nud-interval: 5000
                  proxys: 
                    route-proxy: off
                    inner-vlan-proxy: off
                    inter-vlan-proxy: off
                    anyway-proxy: off
                  ra-property: 
                    ra-control: 
                      unicast-send: off
              ethernet: 
                l3-sub-interface: 
                  vlan-type-dot1q: 
                    vlan-type-vid: 4091
              multicast-bas: 
                authorization-enable: false
      network-instance: 
        instances: 
          - instance: 
              name: "vrf_ncc_oc_nat"
              traffic-statistic-enable: false
              description: ""
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:config_interface
version_added: "2.6"
short_description: Dynamic Host Configuration Protocol.
                   Common interface management, which includes the public configuration of interfaces.
                   Layer 3 Virtual Private Network (L3VPN). An L3VPN is a virtual private network set up over public networks by Internet Service Providers 
                   (ISPs) and Network Service Providers (NSPs).
description:
    - Dynamic Host Configuration Protocol.
      Common interface management, which includes the public configuration of interfaces.
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
    ifm:
        description:
            - Common interface management. It includes the public configuration of interfaces.
        required:False
        interfaces:
            description:
                - List of configuring information on an interface.
            required:False
            interface:
                description:
                    - Configure information on an interface. Physical, NULL, Virtual-if, and Virtual-Template0 interfaces cannot be created or deleted.
                required:False
                name:
                    description:
                        - The textual name of the interface. It should be the name of the interface as assigned by the local device. It should be suitable for 
                          use in commands which entered at the device's 'console'. This might be a text name, such as 'NULL0', depending on the interface 
                          naming syntax of the device.
                    required:True
                    key:True
                    type:str
                    length:[(1, 63)]
                class:
                    description:
                        - Identify a main interface or a sub-interface.
                    required:False
                    suppor-filter:True
                    type:enum
                    choices:['main-interface', 'sub-interface']
                type:
                    description:
                        - Type of an interface. Interfaces include physical and logical interfaces.
                    required:False
                    suppor-filter:True
                    type:enum
                    choices:['Ethernet', 'GigabitEthernet', 'Eth-Trunk', 'Ip-Trunk', 'Pos', 'Tunnel', 'NULL', 'LoopBack', 'Vlanif', '100GE', '200GE', '40GE', 'MTunnel', '10GE', 'GEBrief', 'MEth', 'IMEth', 'Stack-Port', 'Sip', 'Cpos', 'E1', 'Serial', 'Mp-group', 'Virtual-Ethernet', 'VMEth', 'Ima-group', 'Remote-Ap', 'VBridge', 'Atm-Bundle', 'Fiber-Channel', 'Infiniband', 'Lmpif', 'T1', 'T3', 'Global-VE', 'VC4', 'VC12', 'Vbdif', 'Fabric-Port', 'E3', 'Otn', 'Vp', 'DcnInterface', 'Cpos-Trunk', 'Pos-Trunk', 'Trunk-Serial', 'Global-Ima-Group', 'Global-Mp-Group', 'Gmpls-Uni', 'Wdm', 'Nve', 'FCoE-Port', 'Virtual-Template', 'FC', '4x10GE', '10x10GE', '3x40GE', '4x25GE', '25GE', 'ATM', 'XGigabitEthernet', 'ServiceIf', 'Virtual-ODUk', 'FlexE', 'FlexE-200GE', '50|100GE', '50GE', 'FlexE-50G', 'FlexE-100G', 'FlexE-50|100G', 'PW-VE', 'Virtual-Serial', '400GE', 'VX-Tunnel', 'HPGE', 'FlexE-400G', 'Virtual-if', 'Cellular']
                parent-name:
                    description:
                        - Name of the main interface. For example, Ethernet0/1/0.
                    when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                    required:False
                    type:str
                    length:[(1, 63)]
                number:
                    description:
                        - Number of an interface. For example,1, 0/1/0, or 2:1.
                    required:False
                    pattern:['(\\d+/\\d+/\\d+/\\d+)|(\\d+/\\d+/\\d+)|(\\d+/\\d+)|(\\d+)|(\\d+/\\d+/\\d+[:]\\d+)|(\\d+/\\d+/\\d+[:]\\d+[:]\\d+[:]\\d+)|(\\d+/\\d+/\\d+/\\d+[:]\\d+)|(\\d+/\\d+/\\d+/\\d+[:]\\d+[:]\\d+[:]\\d+)|(\\d+/\\d+/\\d+/\\d+/\\d+[:]\\d+)|(\\d+/\\d+[:]\\d+)']
                    type:str
                    length:[(1, 63)]
                description:
                    description:
                        - Description of an interface.
                    required:False
                    type:str
                    length:[(1, 242)]
                admin-status:
                    description:
                        - Administrative status of an interface. Capabilities supported by this node vary according to interface types.
                    required:False
                    type:enum
                    choices:['down', 'up']
                link-protocol:
                    description:
                        - Link protocol. Capabilities supported by this node vary according to interface types.
                    required:False
                    type:enum
                    choices:['ethernet', 'ppp', 'hdlc', 'fr', 'atm', 'tdm']
                router-type:
                    description:
                        - Route attribute of an interface. Capabilities supported by this node vary according to interface types.
                    required:False
                    type:enum
                    choices:['PtoP', 'PtoMP', 'broadcast', 'NBMA', 'invalid']
                statistic-enable:
                    description:
                        - Enable/disable the statistics function on an interface. The default value of this node varies according to different interface 
                          types. Capabilities supported by this node vary according to interface types.
                    required:False
                    type:bool
                    choices:['true', 'false']
                vrf-name:
                    description:
                        - Name of a VPN instance. It uniquely identifies a VPN instance. The VRF name of the DCN interface cannot be created, modified, or 
                          deleted.
                    required:False
                    default:_public_
                    type:str
                    length:[(1, 31)]
                ipv4:
                    description:
                        - Configure IPv4 addresses.
                    must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                    required:False
                    addresses:
                        description:
                            - List of common addresses. The IPv4 address of the DCN interface cannot be created, modified, or deleted.
                        must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                        required:False
                        address:
                            description:
                                - Configure IPv4 address.
                            required:False
                            ip:
                                description:
                                    - IPv4 address.
                                required:True
                                key:True
                                pattern:['[0-9\\.]*']
                                type:str
                            mask:
                                description:
                                    - IPv4 address mask.
                                required:True
                                mandatory:True
                                pattern:['((([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))']
                                type:str
                                length:[(9, 15)]
                            type:
                                description:
                                    - IPv4 address type.
                                required:True
                                mandatory:True
                                type:enum
                                choices:['main', 'sub']
                ipv6:
                    description:
                        - Enable/disable the IPv6 capability on an interface.
                    required:False
                    spread-mtu-flag:
                        description:
                            - Enable/disable the function of spreading the IPv6 MTU of main interface to subinterface.
                        required:False
                        default:False
                        type:bool
                        choices:['true', 'false']
                    auto-link-local:
                        description:
                            - Enable/disable an interface with the auto linklocal address function.
                        must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                        required:False
                        default:False
                        type:bool
                        choices:['true', 'false']
                    addresses:
                        description:
                            - List of IPv6 addresses.
                        must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                        required:False
                        address:
                            description:
                                - Configure IPv6 address.
                            required:False
                            ip:
                                description:
                                    - IPv6 address.
                                required:True
                                key:True
                                pattern:['[0-9a-fA-F:\\.]*']
                                type:str
                            prefix-length:
                                description:
                                    - Length of the IPv6 address prefix.
                                required:True
                                mandatory:True
                                type:int
                                range:[(1, 128)]
                            type:
                                description:
                                    - IPv6 address type.
                                required:True
                                mandatory:True
                                type:enum
                                choices:['global', 'link-local', 'anycast']
                    nd-collection:
                        description:
                            - Configure ND interface configurations.
                        required:False
                        if-property:
                            description:
                                - Configure ND interface configurations.
                            required:False
                            retrans-timer:
                                description:
                                    - To set the retransmission timer of a router.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:1000
                                type:int
                                range:[(1000, 4294967295)]
                            nud-reach-time:
                                description:
                                    - To set the reachable time of a neighbor.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:1200000
                                type:int
                                range:[(1, 3600000)]
                            attempts-value:
                                description:
                                    - To set the number of sent NS messages during DAD.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:1
                                type:int
                                range:[(0, 600)]
                            max-dyn-nb-num:
                                description:
                                    - The maximum of limitation of dynamic neighbor.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:0
                                type:int
                                range:[(0, 65536)]
                            nud-attempts:
                                description:
                                    - ND entries NUD attempts.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:3
                                type:int
                                range:[(1, 10)]
                            na-glean:
                                description:
                                    - Flag of generating NB when receiving NA packet.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                            ma-flag:
                                description:
                                    - Flag of obtaining the routable address through state-based automatic configuration.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                            o-flag:
                                description:
                                    - Flag of setting state-based automatic configuration.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                            ra-halt-flag:
                                description:
                                    - To suppress the advertisement of RA packets.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:on
                                type:enum
                                choices:['off', 'on']
                            max-interval:
                                description:
                                    - The Maximum interval between periodic RA packets sent on this interface.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:600
                                type:int
                                range:[(4, 1800)]
                            ra-preference:
                                description:
                                    - RA router preference.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:medium
                                type:enum
                                choices:['medium', 'high', 'low']
                            ra-prefix-flag:
                                description:
                                    - Flag of RA packet carry prefix information.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:on
                                type:enum
                                choices:['off', 'on']
                            ra-mtu-flag:
                                description:
                                    - Flag of RA packet carry MTU option.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:on
                                type:enum
                                choices:['off', 'on']
                            strict-flag:
                                description:
                                    - Enable/disable strict security mode.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:False
                                type:bool
                                choices:['true', 'false']
                            ts-fuzz-factor:
                                description:
                                    - Fuzz factor for timestamp option.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:1
                                type:int
                                range:[(0, 1000)]
                            ts-clock-drift:
                                description:
                                    - Drift for timestamp option.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:1
                                type:int
                                range:[(0, 100)]
                            ts-delta:
                                description:
                                    - Delta for timestamp option.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:300
                                type:int
                                range:[(0, 1000)]
                            rsa-min-key-len:
                                description:
                                    - The minimum length of acceptable RSA key pair.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:512
                                type:int
                                range:[(384, 3072)]
                            rsa-max-key-len:
                                description:
                                    - The maximum length of acceptable RSA key pair.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:2048
                                type:int
                                range:[(384, 3072)]
                            nud-interval:
                                description:
                                    - ND entries NUD interval.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:5000
                                type:int
                                range:[(1000, 4294967295)]
                        proxys:
                            description:
                                - Configure list of ND proxy.
                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                            required:False
                            route-proxy:
                                description:
                                    - Router proxy.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                            inner-vlan-proxy:
                                description:
                                    - InnerVLAN proxy.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                            inter-vlan-proxy:
                                description:
                                    - InterVLAN proxy.
                                when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                            anyway-proxy:
                                description:
                                    - Anyway proxy.
                                required:False
                                default:off
                                type:enum
                                choices:['off', 'on']
                        ra-property:
                            description:
                                - Configure ND RA configurations under the interface.
                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                            required:False
                            ra-control:
                                description:
                                    - Configure ND RA configurations.
                                required:False
                                unicast-send:
                                    description:
                                        - Flag of Sending RA unicast packet when receive a RS packet.
                                    required:False
                                    default:off
                                    type:enum
                                    choices:['off', 'on']
                ethernet:
                    description:
                        - Configure ethernet interface.
                    required:False
                    l3-sub-interface:
                        description:
                            - Configure l3 sub-interface attribute.
                        when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                        required:False
                        vlan-type-dot1q:
                            description:
                                - Configure VLAN-type dot1q.
                            required:False
                            vlan-type-vid:
                                description:
                                    - VLAN ID of the VLAN sub-interface;
                                required:True
                                mandatory:True
                                type:int
                                range:[(1, 4094)]
                multicast-bas:
                    description:
                        - Configure multicast BAS.
                    must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                    required:False
                    authorization-enable:
                        description:
                            - Enable/disable authorization.
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
                traffic-statistic-enable:
                    description:
                        - Enable/disable L3VPN traffic statistics.
                    when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                    required:False
                    default:False
                    type:bool
                    choices:['true', 'false']
                description:
                    description:
                        - The description of a VPN instance. The value is a string, spaces supported.
                    when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                    required:False
                    pattern:['([^?]*)']
                    type:str
                    length:[(1, 242)]

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/ifm/interfaces/interface/name', '/ifm/interfaces/interface/ipv4/addresses/address/ip', '/ifm/interfaces/interface/ipv6/addresses/address/ip', '/network-instance/instances/instance/name']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/ifm': ['', '@xmlns="urn:huawei:yang:huawei-ifm"', '/ifm']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/ifm/interfaces': ['', '', '/ifm/interfaces']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/ifm/interfaces/interface': ['', '', '/ifm/interfaces/interface']}, {'/network-instance/instances/instance': ['', '', '/network-instance/instances/instance']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/ifm/interfaces/interface/name': ['', '', '/ifm/interfaces/interface/name']}, {'/ifm/interfaces/interface/class': ['', '', '/ifm/interfaces/interface/class']}, {'/ifm/interfaces/interface/type': ['', '', '/ifm/interfaces/interface/type']}, {'/ifm/interfaces/interface/parent-name': ['', '', '/ifm/interfaces/interface/parent-name']}, {'/ifm/interfaces/interface/number': ['', '', '/ifm/interfaces/interface/number']}, {'/ifm/interfaces/interface/description': ['', '', '/ifm/interfaces/interface/description']}, {'/ifm/interfaces/interface/admin-status': ['', '', '/ifm/interfaces/interface/admin-status']}, {'/ifm/interfaces/interface/link-protocol': ['', '', '/ifm/interfaces/interface/link-protocol']}, {'/ifm/interfaces/interface/router-type': ['', '', '/ifm/interfaces/interface/router-type']}, {'/ifm/interfaces/interface/statistic-enable': ['', '', '/ifm/interfaces/interface/statistic-enable']}, {'/ifm/interfaces/interface/vrf-name': ['', '', '/ifm/interfaces/interface/vrf-name']}, {'/ifm/interfaces/interface/ipv4': ['', '@xmlns="urn:huawei:yang:huawei-ip"', '/ifm/interfaces/interface/ipv4']}, {'/ifm/interfaces/interface/ipv6': ['', '@xmlns="urn:huawei:yang:huawei-ip"', '/ifm/interfaces/interface/ipv6']}, {'/ifm/interfaces/interface/ethernet': ['', '@xmlns="urn:huawei:yang:huawei-ethernet"', '/ifm/interfaces/interface/ethernet']}, {'/ifm/interfaces/interface/multicast-bas': ['', '@xmlns="urn:huawei:yang:huawei-multicast-bas"', '/ifm/interfaces/interface/multicast-bas']}, {'/network-instance/instances/instance/name': ['', '', '/network-instance/instances/instance/name']}, {'/network-instance/instances/instance/traffic-statistic-enable': ['', '@xmlns="urn:huawei:yang:huawei-l3vpn"', '/network-instance/instances/instance/traffic-statistic-enable']}, {'/network-instance/instances/instance/description': ['', '', '/network-instance/instances/instance/description']}, {'/ifm/interfaces/interface/ipv4/addresses': ['', '', '/ifm/interfaces/interface/ipv4/addresses']}, {'/ifm/interfaces/interface/ipv6/spread-mtu-flag': ['', '', '/ifm/interfaces/interface/ipv6/spread-mtu-flag']}, {'/ifm/interfaces/interface/ipv6/auto-link-local': ['', '', '/ifm/interfaces/interface/ipv6/auto-link-local']}, {'/ifm/interfaces/interface/ipv6/addresses': ['', '', '/ifm/interfaces/interface/ipv6/addresses']}, {'/ifm/interfaces/interface/ipv6/nd-collection': ['', '@xmlns="urn:huawei:yang:huawei-ipv6-nd"', '/ifm/interfaces/interface/ipv6/nd-collection']}, {'/ifm/interfaces/interface/ethernet/l3-sub-interface': ['', '', '/ifm/interfaces/interface/ethernet/l3-sub-interface']}, {'/ifm/interfaces/interface/multicast-bas/authorization-enable': ['', '', '/ifm/interfaces/interface/multicast-bas/authorization-enable']}, {'/ifm/interfaces/interface/ipv4/addresses/address': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address']}, {'/ifm/interfaces/interface/ipv6/addresses/address': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys']}, {'/ifm/interfaces/interface/ipv6/nd-collection/ra-property': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/ra-property']}, {'/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q': ['', '', '/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q']}, {'/ifm/interfaces/interface/ipv4/addresses/address/ip': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address/ip']}, {'/ifm/interfaces/interface/ipv4/addresses/address/mask': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address/mask']}, {'/ifm/interfaces/interface/ipv4/addresses/address/type': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address/type']}, {'/ifm/interfaces/interface/ipv6/addresses/address/ip': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address/ip']}, {'/ifm/interfaces/interface/ipv6/addresses/address/prefix-length': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address/prefix-length']}, {'/ifm/interfaces/interface/ipv6/addresses/address/type': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address/type']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/retrans-timer': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/retrans-timer']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-reach-time': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-reach-time']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/attempts-value': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/attempts-value']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-dyn-nb-num': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-dyn-nb-num']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-attempts': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-attempts']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/na-glean': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/na-glean']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ma-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ma-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/o-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/o-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-halt-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-halt-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-interval': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-interval']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-preference': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-preference']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-prefix-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-prefix-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-mtu-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-mtu-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/strict-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/strict-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-fuzz-factor': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-fuzz-factor']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-clock-drift': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-clock-drift']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-delta': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-delta']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-min-key-len': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-min-key-len']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-max-key-len': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-max-key-len']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-interval': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-interval']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/route-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/route-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/inner-vlan-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/inner-vlan-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/inter-vlan-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/inter-vlan-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/anyway-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/anyway-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control']}, {'/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q/vlan-type-vid': ['', '', '/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q/vlan-type-vid']}, {'/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control/unicast-send': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control/unicast-send']}]

business_tag = ['dhcp', 'ifm', 'network-instance']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('ifm', {'type': 'dict', 'options': OrderedDict([('interfaces', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('interface', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('class', {'choices': ['main-interface', 'sub-interface'], 'required': False}), ('type', {'choices': ['Ethernet', 'GigabitEthernet', 'Eth-Trunk', 'Ip-Trunk', 'Pos', 'Tunnel', 'NULL', 'LoopBack', 'Vlanif', '100GE', '200GE', '40GE', 'MTunnel', '10GE', 'GEBrief', 'MEth', 'IMEth', 'Stack-Port', 'Sip', 'Cpos', 'E1', 'Serial', 'Mp-group', 'Virtual-Ethernet', 'VMEth', 'Ima-group', 'Remote-Ap', 'VBridge', 'Atm-Bundle', 'Fiber-Channel', 'Infiniband', 'Lmpif', 'T1', 'T3', 'Global-VE', 'VC4', 'VC12', 'Vbdif', 'Fabric-Port', 'E3', 'Otn', 'Vp', 'DcnInterface', 'Cpos-Trunk', 'Pos-Trunk', 'Trunk-Serial', 'Global-Ima-Group', 'Global-Mp-Group', 'Gmpls-Uni', 'Wdm', 'Nve', 'FCoE-Port', 'Virtual-Template', 'FC', '4x10GE', '10x10GE', '3x40GE', '4x25GE', '25GE', 'ATM', 'XGigabitEthernet', 'ServiceIf', 'Virtual-ODUk', 'FlexE', 'FlexE-200GE', '50|100GE', '50GE', 'FlexE-50G', 'FlexE-100G', 'FlexE-50|100G', 'PW-VE', 'Virtual-Serial', '400GE', 'VX-Tunnel', 'HPGE', 'FlexE-400G', 'Virtual-if', 'Cellular'], 'required': False}), ('parent-name', {'type': 'str', 'required': False}), ('number', {'type': 'str', 'required': False}), ('description', {'type': 'str', 'required': False}), ('admin-status', {'choices': ['down', 'up'], 'required': False}), ('link-protocol', {'choices': ['ethernet', 'ppp', 'hdlc', 'fr', 'atm', 'tdm'], 'required': False}), ('router-type', {'choices': ['PtoP', 'PtoMP', 'broadcast', 'NBMA', 'invalid'], 'required': False}), ('statistic-enable', {'type': 'bool', 'required': False}), ('vrf-name', {'type': 'str', 'default': '_public_', 'required': False}), ('ipv4', {'type': 'dict', 'options': OrderedDict([('addresses', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('address', {'type': 'dict', 'options': OrderedDict([('ip', {'type': 'str', 'required': True}), ('mask', {'type': 'str', 'required': True}), ('type', {'choices': ['main', 'sub'], 'required': True})])})])})])}), ('ipv6', {'type': 'dict', 'options': OrderedDict([('spread-mtu-flag', {'type': 'bool', 'required': False}), ('auto-link-local', {'type': 'bool', 'required': False}), ('addresses', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('address', {'type': 'dict', 'options': OrderedDict([('ip', {'type': 'str', 'required': True}), ('prefix-length', {'type': 'int', 'required': True}), ('type', {'choices': ['global', 'link-local', 'anycast'], 'required': True})])})])}), ('nd-collection', {'type': 'dict', 'options': OrderedDict([('if-property', {'type': 'dict', 'options': OrderedDict([('retrans-timer', {'type': 'int', 'default': 1000, 'required': False}), ('nud-reach-time', {'type': 'int', 'default': 1200000, 'required': False}), ('attempts-value', {'type': 'int', 'default': 1, 'required': False}), ('max-dyn-nb-num', {'type': 'int', 'required': False}), ('nud-attempts', {'type': 'int', 'default': 3, 'required': False}), ('na-glean', {'choices': ['off', 'on'], 'default': 'off', 'required': False}), ('ma-flag', {'choices': ['off', 'on'], 'default': 'off', 'required': False}), ('o-flag', {'choices': ['off', 'on'], 'default': 'off', 'required': False}), ('ra-halt-flag', {'choices': ['off', 'on'], 'default': 'on', 'required': False}), ('max-interval', {'type': 'int', 'default': 600, 'required': False}), ('ra-preference', {'choices': ['medium', 'high', 'low'], 'default': 'medium', 'required': False}), ('ra-prefix-flag', {'choices': ['off', 'on'], 'default': 'on', 'required': False}), ('ra-mtu-flag', {'choices': ['off', 'on'], 'default': 'on', 'required': False}), ('strict-flag', {'type': 'bool', 'required': False}), ('ts-fuzz-factor', {'type': 'int', 'default': 1, 'required': False}), ('ts-clock-drift', {'type': 'int', 'default': 1, 'required': False}), ('ts-delta', {'type': 'int', 'default': 300, 'required': False}), ('rsa-min-key-len', {'type': 'int', 'default': 512, 'required': False}), ('rsa-max-key-len', {'type': 'int', 'default': 2048, 'required': False}), ('nud-interval', {'type': 'int', 'default': 5000, 'required': False})])}), ('proxys', {'type': 'dict', 'options': OrderedDict([('route-proxy', {'choices': ['off', 'on'], 'default': 'off', 'required': False}), ('inner-vlan-proxy', {'choices': ['off', 'on'], 'default': 'off', 'required': False}), ('inter-vlan-proxy', {'choices': ['off', 'on'], 'default': 'off', 'required': False}), ('anyway-proxy', {'choices': ['off', 'on'], 'default': 'off', 'required': False})])}), ('ra-property', {'type': 'dict', 'options': OrderedDict([('ra-control', {'type': 'dict', 'options': OrderedDict([('unicast-send', {'choices': ['off', 'on'], 'default': 'off', 'required': False})])})])})])})])}), ('ethernet', {'type': 'dict', 'options': OrderedDict([('l3-sub-interface', {'type': 'dict', 'options': OrderedDict([('vlan-type-dot1q', {'type': 'dict', 'options': OrderedDict([('vlan-type-vid', {'type': 'int', 'required': True})])})])})])}), ('multicast-bas', {'type': 'dict', 'options': OrderedDict([('authorization-enable', {'type': 'bool', 'required': False})])})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('traffic-statistic-enable', {'type': 'bool', 'required': False}), ('description', {'type': 'str', 'required': False})])})])})])})])

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
            ('ifm', OrderedDict([('interfaces', OrderedDict([('interface', OrderedDict([('name', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(1, 63)]}), 
            ('class', {
                'required': False, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['main-interface', 'sub-interface']}), 
            ('type', {
                'required': False, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['Ethernet', 'GigabitEthernet', 'Eth-Trunk', 'Ip-Trunk', 'Pos', 'Tunnel', 'NULL', 'LoopBack', 'Vlanif', '100GE', '200GE', '40GE', 'MTunnel', '10GE', 'GEBrief', 'MEth', 'IMEth', 'Stack-Port', 'Sip', 'Cpos', 'E1', 'Serial', 'Mp-group', 'Virtual-Ethernet', 'VMEth', 'Ima-group', 'Remote-Ap', 'VBridge', 'Atm-Bundle', 'Fiber-Channel', 'Infiniband', 'Lmpif', 'T1', 'T3', 'Global-VE', 'VC4', 'VC12', 'Vbdif', 'Fabric-Port', 'E3', 'Otn', 'Vp', 'DcnInterface', 'Cpos-Trunk', 'Pos-Trunk', 'Trunk-Serial', 'Global-Ima-Group', 'Global-Mp-Group', 'Gmpls-Uni', 'Wdm', 'Nve', 'FCoE-Port', 'Virtual-Template', 'FC', '4x10GE', '10x10GE', '3x40GE', '4x25GE', '25GE', 'ATM', 'XGigabitEthernet', 'ServiceIf', 'Virtual-ODUk', 'FlexE', 'FlexE-200GE', '50|100GE', '50GE', 'FlexE-50G', 'FlexE-100G', 'FlexE-50|100G', 'PW-VE', 'Virtual-Serial', '400GE', 'VX-Tunnel', 'HPGE', 'FlexE-400G', 'Virtual-if', 'Cellular']}), 
            ('parent-name', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(1, 63)]}), 
            ('number', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': ['(\\d+/\\d+/\\d+/\\d+)|(\\d+/\\d+/\\d+)|(\\d+/\\d+)|(\\d+)|(\\d+/\\d+/\\d+[:]\\d+)|(\\d+/\\d+/\\d+[:]\\d+[:]\\d+[:]\\d+)|(\\d+/\\d+/\\d+/\\d+[:]\\d+)|(\\d+/\\d+/\\d+/\\d+[:]\\d+[:]\\d+[:]\\d+)|(\\d+/\\d+/\\d+/\\d+/\\d+[:]\\d+)|(\\d+/\\d+[:]\\d+)'], 
                'key': False, 'length': [(1, 63)]}), 
            ('description', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(1, 242)]}), 
            ('admin-status', {
                'required': False, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['down', 'up']}), 
            ('link-protocol', {
                'required': False, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['ethernet', 'ppp', 'hdlc', 'fr', 'atm', 'tdm']}), 
            ('router-type', {
                'required': False, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['PtoP', 'PtoMP', 'broadcast', 'NBMA', 'invalid']}), 
            ('statistic-enable', {
                'required': False, 'type': 'boolean', 'default': None, 
                'pattern': [], 
                'key': False}), 
            ('vrf-name', {
                'required': False, 'type': 'string', 'default': '_public_', 
                'pattern': [], 
                'key': False, 'length': [(1, 31)]}), 
            ('ipv4', OrderedDict([('addresses', OrderedDict([('address', OrderedDict([('ip', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': ['[0-9\\.]*'], 
                'key': True, 'length': []}), 
            ('mask', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': ['((([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.){3}([1-9]?[0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5]))'], 
                'key': False, 'length': [(9, 15)]}), 
            ('type', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['main', 'sub']})]))]))])), 
            ('ipv6', OrderedDict([('spread-mtu-flag', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('auto-link-local', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('addresses', OrderedDict([('address', OrderedDict([('ip', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': ['[0-9a-fA-F:\\.]*'], 
                'key': True, 'length': []}), 
            ('prefix-length', {
                'required': True, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 128)]}), 
            ('type', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['global', 'link-local', 'anycast']})]))])), 
            ('nd-collection', OrderedDict([('if-property', OrderedDict([('retrans-timer', {
                'required': False, 'type': 'int', 'default': 1000, 
                'pattern': [], 
                'key': False, 'range': [(1000, 4294967295)]}), 
            ('nud-reach-time', {
                'required': False, 'type': 'int', 'default': 1200000, 
                'pattern': [], 
                'key': False, 'range': [(1, 3600000)]}), 
            ('attempts-value', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(0, 600)]}), 
            ('max-dyn-nb-num', {
                'required': False, 'type': 'int', 'default': 0, 
                'pattern': [], 
                'key': False, 'range': [(0, 65536)]}), 
            ('nud-attempts', {
                'required': False, 'type': 'int', 'default': 3, 
                'pattern': [], 
                'key': False, 'range': [(1, 10)]}), 
            ('na-glean', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('ma-flag', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('o-flag', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('ra-halt-flag', {
                'required': False, 'type': 'enumeration', 'default': 'on', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('max-interval', {
                'required': False, 'type': 'int', 'default': 600, 
                'pattern': [], 
                'key': False, 'range': [(4, 1800)]}), 
            ('ra-preference', {
                'required': False, 'type': 'enumeration', 'default': 'medium', 
                'pattern': [], 
                'key': False, 'choices': ['medium', 'high', 'low']}), 
            ('ra-prefix-flag', {
                'required': False, 'type': 'enumeration', 'default': 'on', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('ra-mtu-flag', {
                'required': False, 'type': 'enumeration', 'default': 'on', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('strict-flag', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('ts-fuzz-factor', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(0, 1000)]}), 
            ('ts-clock-drift', {
                'required': False, 'type': 'int', 'default': 1, 
                'pattern': [], 
                'key': False, 'range': [(0, 100)]}), 
            ('ts-delta', {
                'required': False, 'type': 'int', 'default': 300, 
                'pattern': [], 
                'key': False, 'range': [(0, 1000)]}), 
            ('rsa-min-key-len', {
                'required': False, 'type': 'int', 'default': 512, 
                'pattern': [], 
                'key': False, 'range': [(384, 3072)]}), 
            ('rsa-max-key-len', {
                'required': False, 'type': 'int', 'default': 2048, 
                'pattern': [], 
                'key': False, 'range': [(384, 3072)]}), 
            ('nud-interval', {
                'required': False, 'type': 'int', 'default': 5000, 
                'pattern': [], 
                'key': False, 'range': [(1000, 4294967295)]})])), 
            ('proxys', OrderedDict([('route-proxy', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('inner-vlan-proxy', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('inter-vlan-proxy', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']}), 
            ('anyway-proxy', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']})])), 
            ('ra-property', OrderedDict([('ra-control', OrderedDict([('unicast-send', {
                'required': False, 'type': 'enumeration', 'default': 'off', 
                'pattern': [], 
                'key': False, 'choices': ['off', 'on']})]))]))]))])), 
            ('ethernet', OrderedDict([('l3-sub-interface', OrderedDict([('vlan-type-dot1q', OrderedDict([('vlan-type-vid', {
                'required': True, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': False, 'range': [(1, 4094)]})]))]))])), 
            ('multicast-bas', OrderedDict([('authorization-enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})]))]))]))])), 
            ('network-instance', OrderedDict([('instances', OrderedDict([('instance', OrderedDict([('name', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(1, 31)]}), 
            ('traffic-statistic-enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('description', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': ['([^?]*)'], 
                'key': False, 'length': [(1, 242)]})]))]))]))])


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
