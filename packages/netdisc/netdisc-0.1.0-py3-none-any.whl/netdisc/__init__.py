import pkg_resources

version = pkg_resources.require("netdisc")[0].version

from .juniper import get_juniper_networks
from .cisco_nxos import get_nxos_networks
from .paloalto_panos import get_panos_networks
from .common import merge_networks
from .network import NetworkSchema