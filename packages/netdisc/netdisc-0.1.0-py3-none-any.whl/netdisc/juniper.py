import re
from ipaddress import IPv4Interface
from loguru import logger

from .network import NetworkSchema
from .common import ipv4_model


def get_juniper_vlans(connection, datacenter) -> list[NetworkSchema]:
    vlan_command = "show configuration vlans | display set | match description"
    logger.trace(f"Running command '{vlan_command}' on {connection.host}")
    vlan_data_raw = connection.send_command(vlan_command)
    vlan_lines = vlan_data_raw.split("\n")
    vlan_data = []

    for line in vlan_lines:
        vlan = re.search("vlans v([0-9]+)\s", line)
        if not vlan:
            continue
        vlan = int(vlan[1])
        description = re.search("description\s(.*)$", line)[1]
        vlan_data.append(
            {
                "vlan": vlan,
                "description": description,
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


def get_juniper_networks(connection, datacenter) -> list[NetworkSchema]:
    vlans = get_juniper_vlans(connection, datacenter)
    logger.trace(f"Collected {len(vlans)} vlans from {connection.host}")
    network_command = "show interfaces terse"
    logger.trace(f"Running command '{network_command}' on {connection.host}")
    ip_data_raw = connection.send_command(network_command)
    ip_lines = ip_data_raw.split("\n")
    final_network_data = []
    re_search = "(?:vlan|irb)\.([0-9]{1,4})\s"
    filtered_ip_lines = [x for x in ip_lines if re.search(re_search, x)]

    ip_data = []
    for line in filtered_ip_lines:
        ip_vlan = int(re.search(re_search, line)[1])
        ip_address = re.search(
            "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}", line
        )
        if not ip_address:
            continue
        ip_data.append({"vlan": ip_vlan, "obj": IPv4Interface(ip_address[0])})

    for vlan in vlans:
        network_match = [x for x in ip_data if x["vlan"] == vlan["vlan"]]
        if network_match:
            network_match = network_match[0]
            vlan.update(ipv4_model(network_match["obj"]))
        final_network_data.append(vlan)
    logger.trace(f"Collected {len(final_network_data)} networks from {connection.host}")
    return final_network_data
