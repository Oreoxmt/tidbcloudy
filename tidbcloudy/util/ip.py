import requests
import socket


def get_current_ip_address() -> str:
    host = "ifconfig.co"
    addrs = socket.getaddrinfo(host, 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    for addr in addrs:
        ipv4_addr = addr[4][0]
        resp = requests.get("http://" + ipv4_addr + "/ip", headers={"Host": host})
        if resp.ok:
            return resp.text.strip()
    raise Exception("Failed to get current ip address")
