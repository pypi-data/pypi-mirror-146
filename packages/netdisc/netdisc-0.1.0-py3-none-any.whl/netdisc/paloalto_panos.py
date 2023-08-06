import re
from ipaddress import IPv4Interface
from loguru import logger

from .network import NetworkSchema
from .common import ipv4_model


def get_panos_networks(connection, datacenter) -> list[NetworkSchema]:
    final_network_data = []
    net_command = "show interface logical"
    logger.trace(f"Running command '{net_command}' on {connection.host}")
    data_raw = connection.send_command(net_command)
    lines = data_raw.split("\n")

    for line in lines:
        filter = re.search(
            "([1-9][0-9]{0,3})\s+([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2})",
            line,
        )
        if not filter:
            continue

        vlan = int(filter[1])
        ip = IPv4Interface(filter[2])

        final_network_data.append(
            {
                "vlan": vlan,
                "description": "",  # todo - get description maybe?
                "datacenter": datacenter,
                "origin_device": connection.host,
                "gateway": filter[2].split("/")[0],
                **ipv4_model(ip),
            },
        )

    logger.trace(f"Collected {len(final_network_data)} networks from {connection.host}")

    return final_network_data
