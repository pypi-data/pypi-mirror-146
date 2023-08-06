from pydantic import BaseModel

class NetworkSchema(BaseModel):
    id: str = None
    datacenter: str = ""
    network: str = ""
    vlan: int = None
    description: str = ""
    netmask: str = ""
    bitmask: int = None
    gateway: str = ""
    network_address: str = ""
    broadcast_address: str = ""
    first_usable_ip: str = ""
    last_usable_ip: str = ""
    origin_device: str = ""

    class Config:
        orm_mode = True
