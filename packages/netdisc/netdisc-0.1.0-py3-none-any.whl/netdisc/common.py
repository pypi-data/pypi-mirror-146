from ipaddress import IPv4Address, IPv4Interface
from copy import deepcopy


def merge_networks(current_networks, new_networks):
    merged_networks = deepcopy(current_networks)
    for device_network in new_networks:
        existing = [x for x in merged_networks if x["vlan"] == device_network["vlan"]]
        if existing:
            existing = existing[0]
            if not existing["network"]:
                existing["network"] = device_network["network"]
                existing["gateway"] = device_network["gateway"]
                existing["network_address"] = device_network["network_address"]
                existing["broadcast_address"] = device_network["broadcast_address"]
                existing["netmask"] = device_network["netmask"]
                existing["bitmask"] = device_network["bitmask"]
                existing["first_usable_ip"] = device_network["first_usable_ip"]
                existing["last_usable_ip"] = device_network["last_usable_ip"]
                existing["origin_device"] = device_network["origin_device"]
        else:
            merged_networks.append(device_network)

    for network in merged_networks:
        network["id"] = f"{network['datacenter']}:{network['vlan']}"
    return merged_networks


def ipv4_model(ipv4_interface: IPv4Interface):
    return {
        "network": str(ipv4_interface.network),
        "network_address": str(ipv4_interface.network).split("/")[0],
        "broadcast_address": str(ipv4_interface.network.broadcast_address),
        "netmask": str(ipv4_interface.network.netmask),
        "bitmask": int(ipv4_interface.network._prefixlen),
        "first_usable_ip": str(
            IPv4Address(int(ipv4_interface.network.network_address) + 1)
        ),
        "last_usable_ip": str(
            IPv4Address(int(ipv4_interface.network.broadcast_address) - 1)
        ),
    }
