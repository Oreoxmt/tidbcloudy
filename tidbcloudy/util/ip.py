import socket

import httpx


def get_current_ip_address() -> str:
    host = "oreo.life"
    # Get the IPv4 address of the host
    addrs = socket.getaddrinfo(host, 80, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
    for addr in addrs:
        ipv4_addr = addr[4][0]
        # Request the IPv4 address of the client from the host
        resp = httpx.get(f"http://{ipv4_addr}/cdn-cgi/trace", headers={"Host": host})
        resp.raise_for_status()
        for line in resp.text.splitlines():
            if line.startswith("ip="):
                # Return the IPv4 address of the client
                return line[3:]
    raise Exception("Failed to get the current IP address")
