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
- name: config_vpn_instance
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

  - name: create_vpn_instance_example
    config_vpn_instance:
      operation_type: config
      operation_specs: 
        - path: /config/dhcp/relay/global
          operation: merge
        - path: /config/network-instance/instances/instance
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/vpn-targets/vpn-target[1]
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/vpn-targets/vpn-target[2]
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/routing/routing-manage/option
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/routing/routing-manage/topologys/topology
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[1]/vpn-ttlmode
          operation: merge
        - path: /config/network-instance/instances/instance/afs/af[2]
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/vpn-targets/vpn-target[1]
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/vpn-targets/vpn-target[2]
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/routing/routing-manage/option
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/routing/routing-manage/topologys/topology
          operation: create
        - path: /config/network-instance/instances/instance/afs/af[2]/vpn-ttlmode
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
                    route-distinguisher: "3215:4091"
                    label-mode: per-route
                    vpn-targets: 
                      - vpn-target: 
                          value: "3215:4091"
                          type: export-extcommunity
                      - vpn-target: 
                          value: "3215:4091"
                          type: import-extcommunity
                    routing: 
                      routing-manage: 
                        option: 
                          frr-enable: false
                        topologys: 
                          - topology: 
                              name: "base"
                    vpn-ttlmode: 
                      ttlmode: pipe
                - af: 
                    type: ipv6-unicast
                    route-distinguisher: "3215:4091"
                    label-mode: per-route
                    vpn-targets: 
                      - vpn-target: 
                          value: "3215:4091"
                          type: export-extcommunity
                      - vpn-target: 
                          value: "3215:4091"
                          type: import-extcommunity
                    routing: 
                      routing-manage: 
                        option: 
                          frr-enable: false
                        topologys: 
                          - topology: 
                              name: "base"
                    vpn-ttlmode: 
                      ttlmode: pipe
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:config_vpn_instance
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
                        route-distinguisher:
                            description:
                                - A VPN address family takes effect only after it is
                                  configured with a RD.The object allows configuration
                                  and deletion, it cannot be modified. The format of
                                  an RD are as follows:
                                  (1) 16-bit AS number :32-bit user-defined number,
                                      for example, 101:3. An AS number ranges from 0 to 65535,
                                      and a user-defined number ranges from 0 to 4294967295.
                                      The AS number and user-defined number cannot be both 0s.
                                      This means that the RD value cannot be 0:0.
                                  (2) 32-bit IP address:16-bit user-defined number,
                                      for example: 192.168.122.15:1.The IP address ranges from
                                      0.0.0.0 to 255.255.255.255, and the user-defined number
                                      ranges from 0 to 65535.
                                  (3) 32-bit AS number :16-bit user-defined number,
                                      for example, 10.11:3. An AS number ranges from 0.0 to
                                      65535.65535 or 0 to 4294967295, and a user-defined number
                                      ranges from 0 to 65535. The AS number and user-defined
                                      number cannot be both 0s. This means that the RD value
                                      cannot be 0.0:0. If a VPN instance's IPv4 or IPv6 address
                                      family to which the node belongs is referenced by BGP,
                                      the node cannot be deleted. If the IPv4 or IPv6 address
                                      family to which the node belongs is not referenced by
                                      BGP and the other address family is referenced by BGP,
                                      the node can be deleted. If the VPN instance is referenced
                                      by BGP but its address families are not referenced by BGP,
                                      the nodes in the address families cannot be deleted.
                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                            required:False
                            type:str
                            length:[(3, 21)]
                        label-mode:
                            description:
                                - Method of distributing labels to VPN instance routes.
                                  The way which assigns the label depends on the paf value.
                                  If there are a large number of routes in a VPN instance,
                                  assign a label for each instance. This allows all routes
                                  in the instance to use one label.
                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                            required:False
                            default:per-instance
                            type:enum
                            choices:['per-instance', 'per-route', 'per-nexthop']
                        vpn-targets:
                            description:
                                - List of RTs. The number of RTs in the group ranges from 1 to 8.
                            when: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                            required:False
                            vpn-target:
                                description:
                                    - Configure RT (VPN Target) s to control route advertisement
                                      between network nodes. Before sending a VPN route to a PE,
                                      the local PE adds an Export RT to the route. After receiving
                                      a route from another PE, the local PE determines whether the
                                      route will be added to the VPN instance based on the local
                                      Import RT and the Export RT that is added to the VPN route.
                                required:False
                                value:
                                    description:
                                        - The formats of a VPN target value are as follows:
                                          (1) 16-bit AS number : 32-bit user-defined number,
                                              for example, 1:3. An AS number ranges from 0
                                              to 65535, and a user-defined number ranges from
                                              0 to 4294967295. The AS number and user-defined
                                              number cannot be both 0s. This means that the
                                              VPN Target value cannot be 0:0.
                                          (2) 32-bit IP address: 16-bit user-defined number,
                                              for example: 192.168.122.15:1.The IP address
                                              ranges from 0.0.0.0 to 255.255.255.255, and
                                              the user-defined number ranges from 0 to 65535.
                                          (3) 32-bit AS number :16-bit user-defined number,
                                              for example, 10.11:3. An AS number ranges from
                                              0.0 to 65535.65535 or 0 to 4294967295, and a
                                              user-defined number ranges from 0 to 65535.
                                              The AS number and user-defined number cannot
                                              be both 0s. This means that the VPN Target
                                              value cannot be 0.0:0.
                                    required:True
                                    key:True
                                    type:str
                                    length:[(3, 21)]
                                type:
                                    description:
                                        - RT types are as follows:
                                          export-extcommunity: Specifies the value of the
                                            extended community attribute of the route from
                                            an outbound interface to the destination VPN.
                                          import-extcommunity: Receives routes that carry
                                            the specified extended community attribute value.
                                    required:True
                                    key:True
                                    type:enum
                                    choices:['export-extcommunity', 'import-extcommunity']
                        routing:
                            description:
                                - Configure routing management.
                            required:False
                            routing-manage:
                                description:
                                    - Configure a basic service package for routing management.
                                required:False
                                option:
                                    description:
                                        - Configure routing management options.
                                    required:False
                                    frr-enable:
                                        description:
                                            - Enable/disable inter-protocol FRR. In the case where primary and secondary links are created between different 
                                              protocols, if the primary link is faulty, services can be quickly switched to the secondary link.
                                        required:False
                                        default:False
                                        type:bool
                                        choices:['true', 'false']
                                topologys:
                                    description:
                                        - List of topology instances.
                                    required:False
                                    topology:
                                        description:
                                            - Configure a topology instance. Different logical topologies can be planned on a physical network for different 
                                              services.
                                        required:False
                                        name:
                                            description:
                                                - Topology name. The base topology cannot be created or deleted. The letters in the topology name should be 
                                                  lowercase.
                                            must: The configuration of this object takes effect only when certain conditions are met. For details, check the definition in the YANG model.
                                            required:True
                                            key:True
                                            type:str
                                            length:[(1, 31)]
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

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/network-instance/instances/instance/name', '/network-instance/instances/instance/afs/af/type', '/network-instance/instances/instance/afs/af/vpn-targets/vpn-target/value', '/network-instance/instances/instance/afs/af/vpn-targets/vpn-target/type', '/network-instance/instances/instance/afs/af/routing/routing-manage/topologys/topology/name']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/network-instance/instances/instance': ['', '', '/network-instance/instances/instance']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/network-instance/instances/instance/name': ['', '', '/network-instance/instances/instance/name']}, {'/network-instance/instances/instance/afs': ['', '@xmlns="urn:huawei:yang:huawei-l3vpn"', '/network-instance/instances/instance/afs']}, {'/network-instance/instances/instance/afs/af': ['', '', '/network-instance/instances/instance/afs/af']}, {'/network-instance/instances/instance/afs/af/type': ['', '', '/network-instance/instances/instance/afs/af/type']}, {'/network-instance/instances/instance/afs/af/route-distinguisher': ['', '', '/network-instance/instances/instance/afs/af/route-distinguisher']}, {'/network-instance/instances/instance/afs/af/label-mode': ['', '', '/network-instance/instances/instance/afs/af/label-mode']}, {'/network-instance/instances/instance/afs/af/vpn-targets': ['', '', '/network-instance/instances/instance/afs/af/vpn-targets']}, {'/network-instance/instances/instance/afs/af/routing': ['', '@xmlns="urn:huawei:yang:huawei-routing"', '/network-instance/instances/instance/afs/af/routing']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode': ['', '@xmlns="urn:huawei:yang:huawei-mpls-forward"', '/network-instance/instances/instance/afs/af/vpn-ttlmode']}, {'/network-instance/instances/instance/afs/af/vpn-targets/vpn-target': ['', '', '/network-instance/instances/instance/afs/af/vpn-targets/vpn-target']}, {'/network-instance/instances/instance/afs/af/routing/routing-manage': ['', '', '/network-instance/instances/instance/afs/af/routing/routing-manage']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode': ['', '', '/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode']}, {'/network-instance/instances/instance/afs/af/vpn-targets/vpn-target/value': ['', '', '/network-instance/instances/instance/afs/af/vpn-targets/vpn-target/value']}, {'/network-instance/instances/instance/afs/af/vpn-targets/vpn-target/type': ['', '', '/network-instance/instances/instance/afs/af/vpn-targets/vpn-target/type']}, {'/network-instance/instances/instance/afs/af/routing/routing-manage/option': ['', '', '/network-instance/instances/instance/afs/af/routing/routing-manage/option']}, {'/network-instance/instances/instance/afs/af/routing/routing-manage/topologys': ['', '', '/network-instance/instances/instance/afs/af/routing/routing-manage/topologys']}, {'/network-instance/instances/instance/afs/af/routing/routing-manage/option/frr-enable': ['', '', '/network-instance/instances/instance/afs/af/routing/routing-manage/option/frr-enable']}, {'/network-instance/instances/instance/afs/af/routing/routing-manage/topologys/topology': ['', '', '/network-instance/instances/instance/afs/af/routing/routing-manage/topologys/topology']}, {'/network-instance/instances/instance/afs/af/routing/routing-manage/topologys/topology/name': ['', '', '/network-instance/instances/instance/afs/af/routing/routing-manage/topologys/topology/name']}]

business_tag = ['dhcp', 'network-instance']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4-unicast', 'ipv6-unicast'], 'required': True}), ('route-distinguisher', {'type': 'str', 'required': False}), ('label-mode', {'choices': ['per-instance', 'per-route', 'per-nexthop'], 'default': 'per-instance', 'required': False}), ('vpn-targets', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('vpn-target', {'type': 'dict', 'options': OrderedDict([('value', {'type': 'str', 'required': True}), ('type', {'choices': ['export-extcommunity', 'import-extcommunity'], 'required': True})])})])}), ('routing', {'type': 'dict', 'options': OrderedDict([('routing-manage', {'type': 'dict', 'options': OrderedDict([('option', {'type': 'dict', 'options': OrderedDict([('frr-enable', {'type': 'bool', 'required': False})])}), ('topologys', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('topology', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True})])})])})])})])}), ('vpn-ttlmode', {'type': 'dict', 'options': OrderedDict([('ttlmode', {'choices': ['pipe', 'uniform'], 'default': 'pipe', 'required': False})])})])})])})])})])})])})])

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
            ('route-distinguisher', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(3, 21)]}), 
            ('label-mode', {
                'required': False, 'type': 'enumeration', 'default': 'per-instance', 
                'pattern': [], 
                'key': False, 'choices': ['per-instance', 'per-route', 'per-nexthop']}), 
            ('vpn-targets', OrderedDict([('vpn-target', OrderedDict([('value', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(3, 21)]}), 
            ('type', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': True, 'choices': ['export-extcommunity', 'import-extcommunity']})]))])), 
            ('routing', OrderedDict([('routing-manage', OrderedDict([('option', OrderedDict([('frr-enable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})])), 
            ('topologys', OrderedDict([('topology', OrderedDict([('name', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(1, 31)]})]))]))]))])), 
            ('vpn-ttlmode', OrderedDict([('ttlmode', {
                'required': False, 'type': 'enumeration', 'default': 'pipe', 
                'pattern': [], 
                'key': False, 'choices': ['pipe', 'uniform']})]))]))]))]))]))]))])


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
