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
- name: config_routing_policy
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
    config_routing_policy:
      operation_type: config
      operation_specs: 
        - path: /relay/global
          operation: merge
        - path: ing-policy/policy-definitions/policy-definition[1]
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[1]/nodes/node
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[1]/nodes/node/next-node-choice
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[2]
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[2]/nodes/node[1]
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[2]/nodes/node[1]/next-node-choice
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[2]/nodes/node[2]
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[2]/nodes/node[2]/next-node-choice
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[3]
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[3]/nodes/node
          operation: create
        - path: ing-policy/policy-definitions/policy-definition[3]/nodes/node/next-node-choice
          operation: create
      dhcp: 
        relay: 
          global: 
            user-detect-interval: 20
            user-autosave-flag: false
            user-store-interval: 300
            distribute-flag: false
            opt82-inner-vlan-insert-flag: false
      routing-policy: 
        policy-definitions: 
          - policy-definition: 
              name: "GEN-POL-OUT-VPN-LOCAL-TO-EBGP"
              nodes: 
                - node: 
                    sequence: 9
                    match-mode: permit
                    next-node-choice: 
                      is-goto-next-node: false
          - policy-definition: 
              name: "VPN-STATIC-TO-MPBGP-TEST"
              nodes: 
                - node: 
                    sequence: 7
                    match-mode: permit
                    next-node-choice: 
                      is-goto-next-node: false
                - node: 
                    sequence: 8
                    match-mode: permit
                    next-node-choice: 
                      is-goto-next-node: false
          - policy-definition: 
              name: "GEN-POL-OUT-VPN-STATIC-TO-MPBGP"
              nodes: 
                - node: 
                    sequence: 6
                    match-mode: permit
                    next-node-choice: 
                      is-goto-next-node: false
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
---
module:config_routing_policy
version_added: "2.6"
short_description: Dynamic Host Configuration Protocol.
                   Routing policies are used to filter routes and control the receiving and advertising of routes. By changing the route attributes, such as 
                   reachability, you can change the path through which the traffic passes.
description:
    - Dynamic Host Configuration Protocol.
      Routing policies are used to filter routes and control the receiving and advertising of routes. By changing the route attributes, such as reachability, 
      you can change the path through which the traffic passes.
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
    routing-policy:
        description:
            - Routing policies are used to filter routes and control the receiving and advertising of routes. By changing the route attributes, such as 
              reachability, you can change the path through which the traffic passes.
        required:False
        policy-definitions:
            description:
                - List of route-policies.
            required:False
            policy-definition:
                description:
                    - Configure a route-policy.
                required:False
                name:
                    description:
                        - Policy name in the format of a string.
                    required:True
                    key:True
                    type:str
                    length:[(1, 200)]
                nodes:
                    description:
                        - List of routing policy nodes.
                    required:False
                    node:
                        description:
                            - Configure a node in a route-policy to filter routes.
                        required:False
                        sequence:
                            description:
                                - Sequence number of a node.
                            required:True
                            key:True
                            type:int
                            range:[(0, 65535)]
                        match-mode:
                            description:
                                - Matching mode of nodes.
                            required:True
                            mandatory:True
                            type:enum
                            choices:['permit', 'deny']
                        next-node-choice:
                            description:
                                - Configure further route matching against a specified node after the routes match the current node. By default, if a route 
                                  matches the current node, it matches the route-policy and is no longer matched against the other nodes.
                            required:False
                            is-goto-next-node:
                                description:
                                    - Enable/disable further route matching against a specified node after the routes match the current node.
                                required:False
                                default:False
                                type:bool
                                choices:['true', 'false']

"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/routing-policy/policy-definitions/policy-definition/name', '/routing-policy/policy-definitions/policy-definition/nodes/node/sequence']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/routing-policy': ['', '@xmlns="urn:huawei:yang:huawei-routing-policy"', '/routing-policy']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/routing-policy/policy-definitions': ['', '', '/routing-policy/policy-definitions']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/routing-policy/policy-definitions/policy-definition': ['', '', '/routing-policy/policy-definitions/policy-definition']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/routing-policy/policy-definitions/policy-definition/name': ['', '', '/routing-policy/policy-definitions/policy-definition/name']}, {'/routing-policy/policy-definitions/policy-definition/nodes': ['', '', '/routing-policy/policy-definitions/policy-definition/nodes']}, {'/routing-policy/policy-definitions/policy-definition/nodes/node': ['', '', '/routing-policy/policy-definitions/policy-definition/nodes/node']}, {'/routing-policy/policy-definitions/policy-definition/nodes/node/sequence': ['', '', '/routing-policy/policy-definitions/policy-definition/nodes/node/sequence']}, {'/routing-policy/policy-definitions/policy-definition/nodes/node/match-mode': ['', '', '/routing-policy/policy-definitions/policy-definition/nodes/node/match-mode']}, {'/routing-policy/policy-definitions/policy-definition/nodes/node/next-node-choice': ['', '', '/routing-policy/policy-definitions/policy-definition/nodes/node/next-node-choice']}, {'/routing-policy/policy-definitions/policy-definition/nodes/node/next-node-choice/is-goto-next-node': ['', '', '/routing-policy/policy-definitions/policy-definition/nodes/node/next-node-choice/is-goto-next-node']}]

business_tag = ['dhcp', 'routing-policy']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('routing-policy', {'type': 'dict', 'options': OrderedDict([('policy-definitions', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('policy-definition', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('nodes', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('node', {'type': 'dict', 'options': OrderedDict([('sequence', {'type': 'int', 'required': True}), ('match-mode', {'choices': ['permit', 'deny'], 'required': True}), ('next-node-choice', {'type': 'dict', 'options': OrderedDict([('is-goto-next-node', {'type': 'bool', 'required': False})])})])})])})])})])})])})])

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
            ('routing-policy', OrderedDict([('policy-definitions', OrderedDict([('policy-definition', OrderedDict([('name', {
                'required': True, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': True, 'length': [(1, 200)]}), 
            ('nodes', OrderedDict([('node', OrderedDict([('sequence', {
                'required': True, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': True, 'range': [(0, 65535)]}), 
            ('match-mode', {
                'required': True, 'type': 'enumeration', 'default': None, 
                'pattern': [], 
                'key': False, 'choices': ['permit', 'deny']}), 
            ('next-node-choice', OrderedDict([('is-goto-next-node', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False})]))]))]))]))]))]))])


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
