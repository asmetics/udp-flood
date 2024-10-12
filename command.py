import socket
import psutil

hideLocalIP = False ## enable it if you want, incase ur screensharing or something, theres no significant risk to showing a private ip. 

## determining the interface
def get_interface_used_by_socket(remote_host="8.8.8.8", remote_port=80):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect((remote_host, remote_port))
        
        local_ip = sock.getsockname()[0]
        
        interfaces = psutil.net_if_addrs()
        for interface, addrs in interfaces.items():
            for addr in addrs:
                if addr.address == local_ip:
                    return interface, local_ip
    finally:
        sock.close()
        
## using the said interface to see the max size you can send with it


def get_max_packet_size(interface_name):
    net_if_addrs = psutil.net_if_stats()
    
    if interface_name in net_if_addrs:
        mtu = net_if_addrs[interface_name].mtu
        return mtu
    else:
        return None

interface, local_ip = get_interface_used_by_socket()
max_packet_size = get_max_packet_size(interface)

if max_packet_size:
    print(f"Maximum packet size for {interface}: {max_packet_size} bytes")
else:
    print(f"Interface {interface} not found")
    
## finally outputting the command

print(f"Socket is using interface: {interface} with IP: {"HIDDEN" if hideLocalIP else local_ip}")

print("---------------------------")
print("Swap out IP and Port with the desired information if your target.")
print(f"python main.py IP PORT -s {max_packet_size} -r 0")
