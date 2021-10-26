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

  - name: 
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
                  address: 
                    ip: 192.168.51.1
                    mask: 255.255.255.252
                    type: main
              ipv6: 
                spread-mtu-flag: false
                auto-link-local: false
                addresses: 
                  address: 
                    ip: 2A01:C000:83:B000:10:20:51:0
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
time:2021-10-24 16:31:25
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
                        - Configure the bandwidth of an interface.
                    required:False
                    addresses:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        address:
                            description:
                                - Configure the bandwidth of an interface.
                            required:False
                            ip:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            mask:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            type:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                ipv6:
                    description:
                        - Configure the bandwidth of an interface.
                    required:False
                    spread-mtu-flag:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        pattern:None
                        type:None
                    auto-link-local:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        pattern:None
                        type:None
                    addresses:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        address:
                            description:
                                - Configure the bandwidth of an interface.
                            required:False
                            ip:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            prefix-length:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            type:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                    nd-collection:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        if-property:
                            description:
                                - Configure the bandwidth of an interface.
                            required:False
                            retrans-timer:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            nud-reach-time:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            attempts-value:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            max-dyn-nb-num:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            nud-attempts:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            na-glean:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ma-flag:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            o-flag:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ra-halt-flag:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            max-interval:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ra-preference:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ra-prefix-flag:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ra-mtu-flag:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            strict-flag:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ts-fuzz-factor:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ts-clock-drift:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            ts-delta:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            rsa-min-key-len:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            rsa-max-key-len:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            nud-interval:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                        proxys:
                            description:
                                - Configure the bandwidth of an interface.
                            required:False
                            route-proxy:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            inner-vlan-proxy:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            inter-vlan-proxy:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                            anyway-proxy:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                        ra-property:
                            description:
                                - Configure the bandwidth of an interface.
                            required:False
                            ra-control:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                unicast-send:
                                    description:
                                        - Configure the bandwidth of an interface.
                                    required:False
                                    pattern:None
                                    type:None
                ethernet:
                    description:
                        - Configure the bandwidth of an interface.
                    required:False
                    l3-sub-interface:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        vlan-type-dot1q:
                            description:
                                - Configure the bandwidth of an interface.
                            required:False
                            vlan-type-vid:
                                description:
                                    - Configure the bandwidth of an interface.
                                required:False
                                pattern:None
                                type:None
                multicast-bas:
                    description:
                        - Configure the bandwidth of an interface.
                    required:False
                    authorization-enable:
                        description:
                            - Configure the bandwidth of an interface.
                        required:False
                        pattern:None
                        type:None
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
key_list = ['/ifm/interfaces/interface/name', '/network-instance/instances/instance/name']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/ifm': ['', '@xmlns="urn:huawei:yang:huawei-ifm"', '/ifm']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/ifm/interfaces': ['', '', '/ifm/interfaces']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/ifm/interfaces/interface': ['', '', '/ifm/interfaces/interface']}, {'/network-instance/instances/instance': ['', '', '/network-instance/instances/instance']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/ifm/interfaces/interface/name': ['', '', '/ifm/interfaces/interface/name']}, {'/ifm/interfaces/interface/class': ['', '', '/ifm/interfaces/interface/class']}, {'/ifm/interfaces/interface/type': ['', '', '/ifm/interfaces/interface/type']}, {'/ifm/interfaces/interface/parent-name': ['', '', '/ifm/interfaces/interface/parent-name']}, {'/ifm/interfaces/interface/number': ['', '', '/ifm/interfaces/interface/number']}, {'/ifm/interfaces/interface/description': ['', '', '/ifm/interfaces/interface/description']}, {'/ifm/interfaces/interface/admin-status': ['', '', '/ifm/interfaces/interface/admin-status']}, {'/ifm/interfaces/interface/link-protocol': ['', '', '/ifm/interfaces/interface/link-protocol']}, {'/ifm/interfaces/interface/router-type': ['', '', '/ifm/interfaces/interface/router-type']}, {'/ifm/interfaces/interface/statistic-enable': ['', '', '/ifm/interfaces/interface/statistic-enable']}, {'/ifm/interfaces/interface/vrf-name': ['', '', '/ifm/interfaces/interface/vrf-name']}, {'/ifm/interfaces/interface/ipv4': ['', '@xmlns="urn:huawei:yang:huawei-ip"', '/ifm/interfaces/interface/ipv4']}, {'/ifm/interfaces/interface/ipv6': ['', '@xmlns="urn:huawei:yang:huawei-ip"', '/ifm/interfaces/interface/ipv6']}, {'/ifm/interfaces/interface/ethernet': ['', '@xmlns="urn:huawei:yang:huawei-ethernet"', '/ifm/interfaces/interface/ethernet']}, {'/ifm/interfaces/interface/multicast-bas': ['', '@xmlns="urn:huawei:yang:huawei-multicast-bas"', '/ifm/interfaces/interface/multicast-bas']}, {'/network-instance/instances/instance/name': ['', '', '/network-instance/instances/instance/name']}, {'/network-instance/instances/instance/traffic-statistic-enable': ['', '@xmlns="urn:huawei:yang:huawei-l3vpn"', '/network-instance/instances/instance/traffic-statistic-enable']}, {'/network-instance/instances/instance/description': ['', '', '/network-instance/instances/instance/description']}, {'/ifm/interfaces/interface/ipv4/addresses': ['', '', '/ifm/interfaces/interface/ipv4/addresses']}, {'/ifm/interfaces/interface/ipv6/spread-mtu-flag': ['', '', '/ifm/interfaces/interface/ipv6/spread-mtu-flag']}, {'/ifm/interfaces/interface/ipv6/auto-link-local': ['', '', '/ifm/interfaces/interface/ipv6/auto-link-local']}, {'/ifm/interfaces/interface/ipv6/addresses': ['', '', '/ifm/interfaces/interface/ipv6/addresses']}, {'/ifm/interfaces/interface/ipv6/nd-collection': ['', '@xmlns="urn:huawei:yang:huawei-ipv6-nd"', '/ifm/interfaces/interface/ipv6/nd-collection']}, {'/ifm/interfaces/interface/ethernet/l3-sub-interface': ['', '', '/ifm/interfaces/interface/ethernet/l3-sub-interface']}, {'/ifm/interfaces/interface/multicast-bas/authorization-enable': ['', '', '/ifm/interfaces/interface/multicast-bas/authorization-enable']}, {'/ifm/interfaces/interface/ipv4/addresses/address': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address']}, {'/ifm/interfaces/interface/ipv6/addresses/address': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys']}, {'/ifm/interfaces/interface/ipv6/nd-collection/ra-property': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/ra-property']}, {'/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q': ['', '', '/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q']}, {'/ifm/interfaces/interface/ipv4/addresses/address/ip': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address/ip']}, {'/ifm/interfaces/interface/ipv4/addresses/address/mask': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address/mask']}, {'/ifm/interfaces/interface/ipv4/addresses/address/type': ['', '', '/ifm/interfaces/interface/ipv4/addresses/address/type']}, {'/ifm/interfaces/interface/ipv6/addresses/address/ip': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address/ip']}, {'/ifm/interfaces/interface/ipv6/addresses/address/prefix-length': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address/prefix-length']}, {'/ifm/interfaces/interface/ipv6/addresses/address/type': ['', '', '/ifm/interfaces/interface/ipv6/addresses/address/type']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/retrans-timer': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/retrans-timer']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-reach-time': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-reach-time']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/attempts-value': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/attempts-value']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-dyn-nb-num': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-dyn-nb-num']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-attempts': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-attempts']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/na-glean': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/na-glean']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ma-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ma-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/o-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/o-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-halt-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-halt-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-interval': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/max-interval']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-preference': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-preference']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-prefix-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-prefix-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-mtu-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ra-mtu-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/strict-flag': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/strict-flag']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-fuzz-factor': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-fuzz-factor']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-clock-drift': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-clock-drift']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-delta': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/ts-delta']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-min-key-len': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-min-key-len']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-max-key-len': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/rsa-max-key-len']}, {'/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-interval': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/if-property/nud-interval']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/route-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/route-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/inner-vlan-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/inner-vlan-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/inter-vlan-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/inter-vlan-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/proxys/anyway-proxy': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/proxys/anyway-proxy']}, {'/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control']}, {'/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q/vlan-type-vid': ['', '', '/ifm/interfaces/interface/ethernet/l3-sub-interface/vlan-type-dot1q/vlan-type-vid']}, {'/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control/unicast-send': ['', '', '/ifm/interfaces/interface/ipv6/nd-collection/ra-property/ra-control/unicast-send']}]

business_tag = ['dhcp', 'ifm', 'network-instance']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('ifm', {'type': 'dict', 'options': OrderedDict([('interfaces', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('interface', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('class', {'choices': ['main-interface', 'sub-interface'], 'required': False}), ('type', {'choices': ['Ethernet', 'GigabitEthernet', 'Eth-Trunk', 'Ip-Trunk', 'Pos', 'Tunnel', 'NULL', 'LoopBack', 'Vlanif', '100GE', '200GE', '40GE', 'MTunnel', '10GE', 'GEBrief', 'MEth', 'IMEth', 'Stack-Port', 'Sip', 'Cpos', 'E1', 'Serial', 'Mp-group', 'Virtual-Ethernet', 'VMEth', 'Ima-group', 'Remote-Ap', 'VBridge', 'Atm-Bundle', 'Fiber-Channel', 'Infiniband', 'Lmpif', 'T1', 'T3', 'Global-VE', 'VC4', 'VC12', 'Vbdif', 'Fabric-Port', 'E3', 'Otn', 'Vp', 'DcnInterface', 'Cpos-Trunk', 'Pos-Trunk', 'Trunk-Serial', 'Global-Ima-Group', 'Global-Mp-Group', 'Gmpls-Uni', 'Wdm', 'Nve', 'FCoE-Port', 'Virtual-Template', 'FC', '4x10GE', '10x10GE', '3x40GE', '4x25GE', '25GE', 'ATM', 'XGigabitEthernet', 'ServiceIf', 'Virtual-ODUk', 'FlexE', 'FlexE-200GE', '50|100GE', '50GE', 'FlexE-50G', 'FlexE-100G', 'FlexE-50|100G', 'PW-VE', 'Virtual-Serial', '400GE', 'VX-Tunnel', 'HPGE', 'FlexE-400G', 'Virtual-if', 'Cellular'], 'required': False}), ('parent-name', {'type': 'str', 'required': False}), ('number', {'type': 'str', 'required': False}), ('description', {'type': 'str', 'required': False}), ('admin-status', {'choices': ['down', 'up'], 'required': False}), ('link-protocol', {'choices': ['ethernet', 'ppp', 'hdlc', 'fr', 'atm', 'tdm'], 'required': False}), ('router-type', {'choices': ['PtoP', 'PtoMP', 'broadcast', 'NBMA', 'invalid'], 'required': False}), ('statistic-enable', {'type': 'bool', 'required': False}), ('vrf-name', {'type': 'str', 'default': '_public_', 'required': False}), ('ipv4', {'type': 'dict', 'options': OrderedDict([('addresses', {'type': 'dict', 'options': OrderedDict([('address', {'type': 'dict', 'options': OrderedDict([('ip', {'type': None, 'required': False}), ('mask', {'type': None, 'required': False}), ('type', {'type': None, 'required': False})])})])})])}), ('ipv6', {'type': 'dict', 'options': OrderedDict([('spread-mtu-flag', {'type': None, 'required': False}), ('auto-link-local', {'type': None, 'required': False}), ('addresses', {'type': 'dict', 'options': OrderedDict([('address', {'type': 'dict', 'options': OrderedDict([('ip', {'type': None, 'required': False}), ('prefix-length', {'type': None, 'required': False}), ('type', {'type': None, 'required': False})])})])}), ('nd-collection', {'type': 'dict', 'options': OrderedDict([('if-property', {'type': 'dict', 'options': OrderedDict([('retrans-timer', {'type': None, 'required': False}), ('nud-reach-time', {'type': None, 'required': False}), ('attempts-value', {'type': None, 'required': False}), ('max-dyn-nb-num', {'type': None, 'required': False}), ('nud-attempts', {'type': None, 'required': False}), ('na-glean', {'type': None, 'required': False}), ('ma-flag', {'type': None, 'required': False}), ('o-flag', {'type': None, 'required': False}), ('ra-halt-flag', {'type': None, 'required': False}), ('max-interval', {'type': None, 'required': False}), ('ra-preference', {'type': None, 'required': False}), ('ra-prefix-flag', {'type': None, 'required': False}), ('ra-mtu-flag', {'type': None, 'required': False}), ('strict-flag', {'type': None, 'required': False}), ('ts-fuzz-factor', {'type': None, 'required': False}), ('ts-clock-drift', {'type': None, 'required': False}), ('ts-delta', {'type': None, 'required': False}), ('rsa-min-key-len', {'type': None, 'required': False}), ('rsa-max-key-len', {'type': None, 'required': False}), ('nud-interval', {'type': None, 'required': False})])}), ('proxys', {'type': 'dict', 'options': OrderedDict([('route-proxy', {'type': None, 'required': False}), ('inner-vlan-proxy', {'type': None, 'required': False}), ('inter-vlan-proxy', {'type': None, 'required': False}), ('anyway-proxy', {'type': None, 'required': False})])}), ('ra-property', {'type': 'dict', 'options': OrderedDict([('ra-control', {'type': 'dict', 'options': OrderedDict([('unicast-send', {'type': None, 'required': False})])})])})])})])}), ('ethernet', {'type': 'dict', 'options': OrderedDict([('l3-sub-interface', {'type': 'dict', 'options': OrderedDict([('vlan-type-dot1q', {'type': 'dict', 'options': OrderedDict([('vlan-type-vid', {'type': None, 'required': False})])})])})])}), ('multicast-bas', {'type': 'dict', 'options': OrderedDict([('authorization-enable', {'type': None, 'required': False})])})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('traffic-statistic-enable', {'type': 'bool', 'required': False}), ('description', {'type': 'str', 'required': False})])})])})])})])

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
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('mask', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('type', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})]))]))])), 
            ('ipv6', OrderedDict([('spread-mtu-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('auto-link-local', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('addresses', OrderedDict([('address', OrderedDict([('ip', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('prefix-length', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('type', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})]))])), 
            ('nd-collection', OrderedDict([('if-property', OrderedDict([('retrans-timer', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('nud-reach-time', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('attempts-value', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('max-dyn-nb-num', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('nud-attempts', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('na-glean', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ma-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('o-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ra-halt-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('max-interval', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ra-preference', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ra-prefix-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ra-mtu-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('strict-flag', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ts-fuzz-factor', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ts-clock-drift', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('ts-delta', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('rsa-min-key-len', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('rsa-max-key-len', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('nud-interval', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})])), 
            ('proxys', OrderedDict([('route-proxy', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('inner-vlan-proxy', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('inter-vlan-proxy', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False}), 
            ('anyway-proxy', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})])), 
            ('ra-property', OrderedDict([('ra-control', OrderedDict([('unicast-send', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})]))]))]))])), 
            ('ethernet', OrderedDict([('l3-sub-interface', OrderedDict([('vlan-type-dot1q', OrderedDict([('vlan-type-vid', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})]))]))])), 
            ('multicast-bas', OrderedDict([('authorization-enable', {
                'required': False, 'type': None, 'default': None, 
                'pattern': None, 'key': False})]))]))]))])), 
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
