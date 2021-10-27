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
- name: config_ipv6_family
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

  - name: config_ipv6_family_example
    config_ipv6_family:
      operation_type: config
      operation_specs: 
        - path: /config/dhcp/relay/global
          operation: merge
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af
          operation: create
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af/ipv6-vpn
          operation: create
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af/ipv6-vpn/public-as-only
          operation: create
        - path: /config/network-instance/instances/instance[1]/bgp/base-process/peers/peer/afs/af/ipv6-vpn/public-as-only-import
          operation: create
        - path: /config/network-instance/instances/instance[2]/afs/af/vpn-ttlmode
          operation: merge
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/common
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/preference
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route[1]
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route[2]
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/slow-peer
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/routing-table-rib-only
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/afs/af/ipv6-unicast/qos
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
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af/ipv6-unicast
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only
          operation: create
        - path: /config/network-instance/instances/instance[2]/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only-import
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
                  peers: 
                    - peer: 
                        address: "5.5.5.5"
                        afs: 
                          - af: 
                              type: ipv6vpn
          - instance: 
              name: "vrf_ncc_oc_nat"
              afs: 
                - af: 
                    type: ipv6-unicast
                    vpn-ttlmode: 
                      ttlmode: pipe
              bgp: 
                base-process: 
                  afs: 
                    - af: 
                        type: ipv6uni
                        ipv6-unicast: 
                          common: 
                            auto-frr: false
                            maximum-load-balancing-ibgp: 1
                            maximum-load-balancing-ebgp: 1
                            nexthop-resolve-aigp: false
                            supernet-unicast-advertise: false
                            bestroute-as-path-ignore: false
                            determin-med: false
                            attribute-set-enable: false
                            load-balanc-igp-metric-ignore: false
                            load-balanc-as-path-ignore: false
                            load-balanc-as-path-relax: false
                            maximum-load-balancing: 1
                            best-route-bit-error-detection: false
                            import-rib-nexthop-invariable: false
                            route-relay-tunnel-v4: false
                            bestroute-med-plus-igp: false
                            bestroute-igp-metric-ignore: false
                            bestroute-router-id-prior-clusterlist: false
                            bestroute-med-none-as-maximum: false
                            load-balancing-eibgp-enable: false
                            prefix-origin-as-validation: false
                            advertise-route-mode: all
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
                          slow-peer: 
                            detection: true
                            detection-threshold: 300
                            absolute-detection: true
                            absolute-detection-threshold: 9
                          routing-table-rib-only: 
                            enable: false
                          qos: 
                            ipv6-qppb: false
                  peers: 
                    - peer: 
                        address: "30::1"
                        remote-as: "65001"
                        ebgp-max-hop: 1
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
                              type: ipv6uni
                              ipv6-unicast: 
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
None
"""



xml_head = """<config>"""

xml_tail = """</config>"""

# Keyword list
key_list = ['/network-instance/instances/instance/name', '/network-instance/instances/instance/afs/af/type', '/network-instance/instances/instance/bgp/base-process/afs/af/type', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/protocol', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/process-id', '/network-instance/instances/instance/bgp/base-process/peers/peer/address', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/type']

namespaces = [{'/dhcp': ['', '@xmlns="urn:huawei:yang:huawei-dhcp"', '/dhcp']}, {'/network-instance': ['', '@xmlns="urn:huawei:yang:huawei-network-instance"', '/network-instance']}, {'/dhcp/relay': ['', '', '/dhcp/relay']}, {'/network-instance/instances': ['', '', '/network-instance/instances']}, {'/dhcp/relay/global': ['', '', '/dhcp/relay/global']}, {'/network-instance/instances/instance': ['', '', '/network-instance/instances/instance']}, {'/dhcp/relay/global/user-detect-interval': ['', '', '/dhcp/relay/global/user-detect-interval']}, {'/dhcp/relay/global/user-autosave-flag': ['', '', '/dhcp/relay/global/user-autosave-flag']}, {'/dhcp/relay/global/user-store-interval': ['', '', '/dhcp/relay/global/user-store-interval']}, {'/dhcp/relay/global/distribute-flag': ['', '', '/dhcp/relay/global/distribute-flag']}, {'/dhcp/relay/global/opt82-inner-vlan-insert-flag': ['', '', '/dhcp/relay/global/opt82-inner-vlan-insert-flag']}, {'/network-instance/instances/instance/name': ['', '', '/network-instance/instances/instance/name']}, {'/network-instance/instances/instance/afs': ['', '@xmlns="urn:huawei:yang:huawei-l3vpn"', '/network-instance/instances/instance/afs']}, {'/network-instance/instances/instance/bgp': ['', '@xmlns="urn:huawei:yang:huawei-bgp"', '/network-instance/instances/instance/bgp']}, {'/network-instance/instances/instance/afs/af': ['', '', '/network-instance/instances/instance/afs/af']}, {'/network-instance/instances/instance/bgp/base-process': ['', '', '/network-instance/instances/instance/bgp/base-process']}, {'/network-instance/instances/instance/afs/af/type': ['', '', '/network-instance/instances/instance/afs/af/type']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode': ['', '@xmlns="urn:huawei:yang:huawei-mpls-forward"', '/network-instance/instances/instance/afs/af/vpn-ttlmode']}, {'/network-instance/instances/instance/bgp/base-process/afs': ['', '', '/network-instance/instances/instance/bgp/base-process/afs']}, {'/network-instance/instances/instance/bgp/base-process/peers': ['', '', '/network-instance/instances/instance/bgp/base-process/peers']}, {'/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode': ['', '', '/network-instance/instances/instance/afs/af/vpn-ttlmode/ttlmode']}, {'/network-instance/instances/instance/bgp/base-process/afs/af': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/type': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/type']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/address': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/address']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/remote-as': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/remote-as']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/ebgp-max-hop': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/ebgp-max-hop']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/routing-table-rib-only': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/routing-table-rib-only']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/qos': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/qos']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/keep-alive-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/keep-alive-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/hold-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/hold-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/min-hold-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/min-hold-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/timer/connect-retry-time': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/timer/connect-retry-time']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/peer-reset': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/graceful-restart/peer-reset']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/local-graceful-restart/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/router-id-auto-select': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/router-id-auto-select']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/auto-frr': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/auto-frr']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/maximum-load-balancing-ibgp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/maximum-load-balancing-ibgp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/maximum-load-balancing-ebgp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/maximum-load-balancing-ebgp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/nexthop-resolve-aigp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/nexthop-resolve-aigp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/supernet-unicast-advertise': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/supernet-unicast-advertise']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-as-path-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-as-path-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/determin-med': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/determin-med']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/attribute-set-enable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/attribute-set-enable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balanc-igp-metric-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balanc-igp-metric-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balanc-as-path-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balanc-as-path-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balanc-as-path-relax': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balanc-as-path-relax']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/maximum-load-balancing': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/maximum-load-balancing']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/best-route-bit-error-detection': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/best-route-bit-error-detection']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/import-rib-nexthop-invariable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/import-rib-nexthop-invariable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/route-relay-tunnel-v4': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/route-relay-tunnel-v4']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-med-plus-igp': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-med-plus-igp']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-igp-metric-ignore': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-igp-metric-ignore']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-router-id-prior-clusterlist': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-router-id-prior-clusterlist']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-med-none-as-maximum': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/bestroute-med-none-as-maximum']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balancing-eibgp-enable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/load-balancing-eibgp-enable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/prefix-origin-as-validation': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/prefix-origin-as-validation']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/advertise-route-mode': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/advertise-route-mode']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/route-select-delay': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/route-select-delay']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/reflect-change-path': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/reflect-change-path']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/always-compare-med': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/always-compare-med']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/default-med': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/default-med']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/nexthop-third-party': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/nexthop-third-party']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/default-local-preference': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/default-local-preference']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/default-route-import': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/default-route-import']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/routerid-neglect': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/routerid-neglect']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/reflect-between-client': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/reflect-between-client']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/ext-community-change': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/ext-community-change']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/active-route-advertise': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/active-route-advertise']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/ebgp-interface-sensitive': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/common/ebgp-interface-sensitive']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference/external': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference/external']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference/internal': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference/internal']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference/local': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/preference/local']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/detection': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/detection']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/detection-threshold': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/detection-threshold']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/absolute-detection': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/absolute-detection']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/absolute-detection-threshold': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/slow-peer/absolute-detection-threshold']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/routing-table-rib-only/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/routing-table-rib-only/enable']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/qos/ipv6-qppb': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/qos/ipv6-qppb']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/type': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/type']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common/restrain': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common/restrain']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common/default-route': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/nexthop-recursive-lookup/common/default-route']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/protocol': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/protocol']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/process-id': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/process-id']}, {'/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/policy-name': ['', '', '/network-instance/instances/instance/bgp/base-process/afs/af/ipv6-unicast/import-routes/import-route/policy-name']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/import-policy': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/import-policy']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/export-policy': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/export-policy']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/route-update-interval': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/route-update-interval']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only-import': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only-import']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only/enable']}, {'/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only-import/enable': ['', '', '/network-instance/instances/instance/bgp/base-process/peers/peer/afs/af/ipv6-unicast/public-as-only-import/enable']}]

business_tag = ['dhcp', 'network-instance']

# Passed to the ansible parameter
argument_spec = OrderedDict([('dhcp', {'type': 'dict', 'options': OrderedDict([('relay', {'type': 'dict', 'options': OrderedDict([('global', {'type': 'dict', 'options': OrderedDict([('user-detect-interval', {'type': 'int', 'default': 20, 'required': False}), ('user-autosave-flag', {'type': 'bool', 'required': False}), ('user-store-interval', {'type': 'int', 'default': 300, 'required': False}), ('distribute-flag', {'type': 'bool', 'required': False}), ('opt82-inner-vlan-insert-flag', {'type': 'bool', 'required': False})])})])})])}), ('network-instance', {'type': 'dict', 'options': OrderedDict([('instances', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('instance', {'type': 'dict', 'options': OrderedDict([('name', {'type': 'str', 'required': True}), ('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4-unicast', 'ipv6-unicast'], 'required': True}), ('vpn-ttlmode', {'type': 'dict', 'options': OrderedDict([('ttlmode', {'choices': ['pipe', 'uniform'], 'default': 'pipe', 'required': False})])})])})])}), ('bgp', {'type': 'dict', 'options': OrderedDict([('base-process', {'type': 'dict', 'options': OrderedDict([('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan'], 'required': True}), ('ipv6-unicast', {'type': 'dict', 'options': OrderedDict([('common', {'type': 'dict', 'options': OrderedDict([('auto-frr', {'type': 'bool', 'required': False}), ('maximum-load-balancing-ibgp', {'type': 'int', 'default': 1, 'required': False}), ('maximum-load-balancing-ebgp', {'type': 'int', 'default': 1, 'required': False}), ('nexthop-resolve-aigp', {'type': 'bool', 'required': False}), ('supernet-unicast-advertise', {'type': 'bool', 'required': False}), ('bestroute-as-path-ignore', {'type': 'bool', 'required': False}), ('determin-med', {'type': 'bool', 'required': False}), ('attribute-set-enable', {'type': 'bool', 'required': False}), ('load-balanc-igp-metric-ignore', {'type': 'bool', 'required': False}), ('load-balanc-as-path-ignore', {'type': 'bool', 'required': False}), ('load-balanc-as-path-relax', {'type': 'bool', 'required': False}), ('maximum-load-balancing', {'type': 'int', 'default': 1, 'required': False}), ('best-route-bit-error-detection', {'type': 'bool', 'required': False}), ('import-rib-nexthop-invariable', {'type': 'bool', 'required': False}), ('route-relay-tunnel-v4', {'type': 'bool', 'required': False}), ('bestroute-med-plus-igp', {'type': 'bool', 'required': False}), ('bestroute-igp-metric-ignore', {'type': 'bool', 'required': False}), ('bestroute-router-id-prior-clusterlist', {'type': 'bool', 'required': False}), ('bestroute-med-none-as-maximum', {'type': 'bool', 'required': False}), ('load-balancing-eibgp-enable', {'type': 'bool', 'required': False}), ('prefix-origin-as-validation', {'type': 'bool', 'required': False}), ('advertise-route-mode', {'choices': ['all', 'best', 'valid'], 'default': 'all', 'required': False}), ('route-select-delay', {'type': 'int', 'required': False}), ('reflect-change-path', {'type': 'bool', 'required': False}), ('always-compare-med', {'type': 'bool', 'required': False}), ('default-med', {'type': 'int', 'required': False}), ('nexthop-third-party', {'type': 'bool', 'required': False}), ('default-local-preference', {'type': 'int', 'default': 100, 'required': False}), ('default-route-import', {'type': 'bool', 'required': False}), ('routerid-neglect', {'type': 'bool', 'required': False}), ('reflect-between-client', {'type': 'bool', 'default': True, 'required': False}), ('ext-community-change', {'type': 'bool', 'required': False}), ('active-route-advertise', {'type': 'bool', 'required': False}), ('ebgp-interface-sensitive', {'type': 'bool', 'default': True, 'required': False})])}), ('preference', {'type': 'dict', 'options': OrderedDict([('external', {'type': 'int', 'default': 255, 'required': False}), ('internal', {'type': 'int', 'default': 255, 'required': False}), ('local', {'type': 'int', 'default': 255, 'required': False})])}), ('nexthop-recursive-lookup', {'type': 'dict', 'options': OrderedDict([('common', {'type': 'dict', 'options': OrderedDict([('restrain', {'type': 'bool', 'default': True, 'required': False}), ('default-route', {'type': 'bool', 'required': False})])})])}), ('import-routes', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('import-route', {'type': 'dict', 'options': OrderedDict([('protocol', {'choices': ['direct', 'isis', 'static', 'ospfv3', 'ripng', 'unr'], 'required': True}), ('process-id', {'type': 'int', 'required': True}), ('policy-name', {'type': 'str', 'required': False})])})])}), ('slow-peer', {'type': 'dict', 'options': OrderedDict([('detection', {'type': 'bool', 'default': True, 'required': False}), ('detection-threshold', {'type': 'int', 'default': 300, 'required': False}), ('absolute-detection', {'type': 'bool', 'default': True, 'required': False}), ('absolute-detection-threshold', {'type': 'int', 'default': 9, 'required': False})])}), ('routing-table-rib-only', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False})])}), ('qos', {'type': 'dict', 'options': OrderedDict([('ipv6-qppb', {'type': 'bool', 'required': False})])})])})])})])}), ('peers', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('peer', {'type': 'dict', 'options': OrderedDict([('address', {'type': 'str', 'required': True}), ('remote-as', {'type': 'str', 'required': True}), ('ebgp-max-hop', {'type': 'int', 'required': False}), ('timer', {'type': 'dict', 'options': OrderedDict([('keep-alive-time', {'type': 'int', 'default': 60, 'required': False}), ('hold-time', {'type': 'int', 'default': 180, 'required': False}), ('min-hold-time', {'type': 'int', 'required': False}), ('connect-retry-time', {'type': 'int', 'default': 32, 'required': False})])}), ('graceful-restart', {'type': 'dict', 'options': OrderedDict([('enable', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False}), ('peer-reset', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False})])}), ('local-graceful-restart', {'type': 'dict', 'options': OrderedDict([('enable', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False})])}), ('afs', {'type': 'list', 'elements': 'dict', 'options': OrderedDict([('af', {'type': 'dict', 'options': OrderedDict([('type', {'choices': ['ipv4uni', 'ipv4multi', 'ipv4vpn', 'ipv4labeluni', 'ipv6uni', 'ipv6vpn', 'ipv4flow', 'l2vpnad', 'evpn', 'mvpn', 'vpntarget', 'ipv4vpnmcast', 'ls', 'mdt', 'ipv6flow', 'mvpnv6', 'vpnv4flow', 'vpnv6flow', 'rpd', 'ipv4srpolicy', 'ipv6srpolicy', 'ipv4sdwan'], 'required': True}), ('ipv6-unicast', {'type': 'dict', 'options': OrderedDict([('import-policy', {'type': 'str', 'required': False}), ('export-policy', {'type': 'str', 'required': False}), ('route-update-interval', {'type': 'int', 'required': False}), ('public-as-only', {'type': 'dict', 'options': OrderedDict([('enable', {'type': 'bool', 'required': False})])}), ('public-as-only-import', {'type': 'dict', 'options': OrderedDict([('enable', {'choices': ['default', 'enable', 'disable'], 'default': 'default', 'required': False})])})])})])})])})])})])})])})])})])})])})])})])

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
            ('ipv6-unicast', OrderedDict([('common', OrderedDict([('auto-frr', {
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
            ('supernet-unicast-advertise', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
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
            ('best-route-bit-error-detection', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('import-rib-nexthop-invariable', {
                'required': False, 'type': 'boolean', 'default': False, 
                'pattern': [], 
                'key': False}), 
            ('route-relay-tunnel-v4', {
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
                'key': True, 'choices': ['direct', 'isis', 'static', 'ospfv3', 'ripng', 'unr']}), 
            ('process-id', {
                'required': True, 'type': 'int', 'default': None, 
                'pattern': [], 
                'key': True, 'range': [(0, 4294967295)]}), 
            ('policy-name', {
                'required': False, 'type': 'string', 'default': None, 
                'pattern': [], 
                'key': False, 'length': [(1, 200)]})]))])), 
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
                'key': False})])), 
            ('qos', OrderedDict([('ipv6-qppb', {
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
            ('ipv6-unicast', OrderedDict([('import-policy', {
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
