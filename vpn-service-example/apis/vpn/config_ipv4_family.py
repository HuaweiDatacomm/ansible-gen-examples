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

  - name: 
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
              bgp: 
                base-process: 
                  afs: 
                    af: 
                  peers: 
                    peer: 
                      afs: 
                        af: 
          - instance: 
              afs: 
                af: 
              bgp: 
                base-process: 
                  afs: 
                    af: 
                      ipv4-unicast: 
                        nexthop-recursive-lookup: 
                        import-routes: 
                  peers: 
                    peer: 
                      afs: 
                        af: 
                          ipv4-unicast: 
      provider: "{{ netconf }}"


"""
DOCUMENTATION = """
None
"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = []

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/network-instance/instances/instance': [[OrderedDict([('name', None), ('bgp', OrderedDict([('@xmlns', 'urn:huawei:yang:huawei-bgp'), ('base-process', OrderedDict([('afs', OrderedDict([('af', OrderedDict([('type', None), ('ipv4-vpn', OrderedDict([('policy-vpntarget', None), ('reflect-change-path', None), ('auto-frr', None), ('route-select-delay', None), ('apply-label-mode', None), ('nexthop-select-depend-type', None), ('default-med', None), ('best-external', None), ('label-free-delay', None), ('default-local-preference', None), ('bestroute-med-plus-igp', None), ('bestroute-igp-metric-ignore', None), ('bestroute-router-id-prior-clusterlist', None), ('reflect-between-client', None), ('activate-route-tag', None), ('load-balancing-eibgp-enable', None), ('load-balanc-igp-metric-ignore', None), ('load-balanc-as-path-ignore', None), ('load-balanc-as-path-relax', None), ('reflector-cluster-ipv4', None), ('reflector-cluster-id', None), ('tunnel-selector-name', None), ('add-path-select-num', None), ('route-reflector-ext-community-filter', None), ('nexthop-recursive-lookup', OrderedDict([('common', OrderedDict([('restrain', None), ('default-route', None), ('route-policy', None), ('filter-name', None)])), ('bit-error-detection', OrderedDict([('enable', None), ('route-policy', None), ('filter-name', None), ('filter-parameter', None)]))])), ('slow-peer', OrderedDict([('detection', None), ('detection-threshold', None), ('absolute-detection', None), ('absolute-detection-threshold', None)]))]))]))])), ('peers', OrderedDict([('peer', OrderedDict([('address', None), ('afs', OrderedDict([('af', OrderedDict([('type', None), ('ipv4-vpn', OrderedDict([('route-update-interval', None), ('public-as-only', OrderedDict([('enable', None)])), ('public-as-only-import', OrderedDict([('enable', None)]))]))]))]))]))]))]))]))]), OrderedDict([('name', None), ('afs', OrderedDict([('@xmlns', 'urn:huawei:yang:huawei-l3vpn'), ('af', OrderedDict([('type', None), ('vpn-ttlmode', OrderedDict([('@xmlns', 'urn:huawei:yang:huawei-mpls-forward'), ('ttlmode', None)]))]))])), ('bgp', OrderedDict([('@xmlns', 'urn:huawei:yang:huawei-bgp'), ('base-process', OrderedDict([('afs', OrderedDict([('af', OrderedDict([('type', None), ('ipv4-unicast', OrderedDict([('common', OrderedDict([('auto-frr', None), ('maximum-load-balancing-ibgp', None), ('maximum-load-balancing-ebgp', None), ('nexthop-resolve-aigp', None), ('summary-automatic', None), ('best-route-bit-error-detection', None), ('supernet-unicast-advertise', None), ('supernet-label-advertise', None), ('lsp-mtu', None), ('label-free-delay', None), ('bestroute-as-path-ignore', None), ('determin-med', None), ('attribute-set-enable', None), ('load-balanc-igp-metric-ignore', None), ('load-balanc-as-path-ignore', None), ('load-balanc-as-path-relax', None), ('maximum-load-balancing', None), ('import-rib-nexthop-invariable', None), ('route-relay-tunnel', None), ('bestroute-med-plus-igp', None), ('bestroute-igp-metric-ignore', None), ('bestroute-router-id-prior-clusterlist', None), ('bestroute-med-none-as-maximum', None), ('load-balancing-eibgp-enable', None), ('prefix-origin-as-validation', None), ('advertise-route-mode', None), ('reoriginate-route', None), ('route-select-delay', None), ('reflect-change-path', None), ('always-compare-med', None), ('default-med', None), ('nexthop-third-party', None), ('default-local-preference', None), ('default-route-import', None), ('routerid-neglect', None), ('reflect-between-client', None), ('ext-community-change', None), ('active-route-advertise', None), ('ebgp-interface-sensitive', None)])), ('preference', OrderedDict([('external', None), ('internal', None), ('local', None)])), ('nexthop-recursive-lookup', OrderedDict([('common', OrderedDict([('restrain', None), ('default-route', None)]))])), ('import-routes', OrderedDict([('import-route', [OrderedDict([('protocol', None), ('process-id', None)]), OrderedDict([('protocol', None), ('process-id', None), ('policy-name', None)])])])), ('lsp-options', OrderedDict([('ingress-protect-mode-bgp-frr', None), ('maximum-load-balancing-ingress', None), ('maximum-load-balancing-transit', None)])), ('slow-peer', OrderedDict([('detection', None), ('detection-threshold', None), ('absolute-detection', None), ('absolute-detection-threshold', None)])), ('routing-table-rib-only', OrderedDict([('enable', None)]))]))]))])), ('peers', OrderedDict([('peer', OrderedDict([('address', None), ('remote-as', None), ('ebgp-max-hop', None), ('local-ifnet-disable', None), ('timer', OrderedDict([('keep-alive-time', None), ('hold-time', None), ('min-hold-time', None), ('connect-retry-time', None)])), ('graceful-restart', OrderedDict([('enable', None), ('peer-reset', None)])), ('local-graceful-restart', OrderedDict([('enable', None)])), ('afs', OrderedDict([('af', OrderedDict([('type', None), ('ipv4-unicast', OrderedDict([('import-policy', None), ('export-policy', None), ('route-update-interval', None), ('public-as-only', OrderedDict([('enable', None)])), ('public-as-only-import', OrderedDict([('enable', None)]))]))]))]))]))]))]))]))])], '', '/network-instance/instances/instance']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}]

business_tag = ['dhcp', 'network-instance']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('bgp', {'type': 'dict', 'options': OrderedDict([('base-process', {'type': 'dict', 'options': OrderedDict([('afs', {'type': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('ipv4-unicast', {'type': 'dict', 'options': OrderedDict([('nexthop-recursive-lookup', {'type': 'dict', 'options': OrderedDict()}), ('import-routes', {'type': 'dict', 'options': OrderedDict()})])})])})])}), ('peers', {'type': 'dict', 'options': OrderedDict([('peer', {'type': 'dict', 'options': OrderedDict([('afs', {'type': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('ipv4-unicast', {'type': 'dict', 'options': OrderedDict()})])})])})])})])})])})])}), ('afs', {'type': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict()})])})])})])})])})])

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
            ('network-instance', OrderedDict([('instances', OrderedDict([('instance', OrderedDict([('bgp', OrderedDict([('base-process', OrderedDict([('afs', OrderedDict([('af', OrderedDict([('ipv4-unicast', OrderedDict([('common', OrderedDict()), 
            ('preference', OrderedDict()), 
            ('nexthop-recursive-lookup', OrderedDict([('common', OrderedDict())])), 
            ('import-routes', OrderedDict([('import-route', OrderedDict())])), 
            ('lsp-options', OrderedDict()), 
            ('slow-peer', OrderedDict()), 
            ('routing-table-rib-only', OrderedDict())]))]))])), 
            ('peers', OrderedDict([('peer', OrderedDict([('timer', OrderedDict()), 
            ('graceful-restart', OrderedDict()), 
            ('local-graceful-restart', OrderedDict()), 
            ('afs', OrderedDict([('af', OrderedDict([('ipv4-unicast', OrderedDict([('public-as-only', OrderedDict()), 
            ('public-as-only-import', OrderedDict())]))]))]))]))]))]))])), 
            ('afs', OrderedDict([('af', OrderedDict([('vpn-ttlmode', OrderedDict())]))]))]))]))]))])


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
