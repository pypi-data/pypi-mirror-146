import re
from ipaddress import IPv4Interface
from loguru import logger

from .network import NetworkSchema
from .common import ipv4_model

def get_nxos_vlans(connection, datacenter) -> list[NetworkSchema]:
    vlan_command = 'show vlan brief'
    logger.trace(f"Running command '{vlan_command}' on {connection.host}")
    vlan_data_raw = connection.send_command(vlan_command)
    vlan_lines = vlan_data_raw.split('\n')
    vlan_data = []

    for line in vlan_lines:
        vlan = re.search("^(\d{1,4})\s+(\S+)", line)
        if not vlan: continue
        vlan_data.append(
            {
                "vlan": int(vlan.group(1)),
                "description": vlan.group(2),
                "datacenter": datacenter,
                "origin_device": connection.host,
                "network": "",
                "gateway": "",
                "network_address": "",
                "broadcast_address": "",
                "netmask": "",
                "bitmask": None,
                "first_usable_ip": "",
                "last_usable_ip": "",
            }
        )
    return vlan_data

def get_nxos_networks(connection, datacenter) -> list[NetworkSchema]:
    vlans = get_nxos_vlans(connection, datacenter)
    logger.trace(f"Collected {len(vlans)} vlans from {connection.host}")
    network_command = 'show ip int vrf all'
    logger.trace(f"Running command '{network_command}' on {connection.host}")
    ip_data_raw = connection.send_command(network_command)
    final_network_data = []
    for vlan in vlans:
        net_match = re.search(rf'^Vlan{vlan["vlan"]},.+\n.+?address: (\S+),.+?subnet: (\S+)', ip_data_raw, re.MULTILINE)
        if not net_match: continue
        ip_interface = IPv4Interface(net_match.group(1))
        ip_network = IPv4Interface(net_match.group(2))
        vlan.update(ipv4_model(ip_network))
        if int(ip_interface) == int(ip_network) + 1:
            vlan['gateway'] = net_match.group(1)
        final_network_data.append(vlan)
    logger.trace(f"Collected {len(final_network_data)} networks from {connection.host}")
    return final_network_data