# python_controller/net_scanner.py

import json
import os
import socket
from scapy.all import ARP, Ether, srp
import subprocess

def get_real_subnet():
    """Get subnet from actual connected interface (e.g. hotspot, router)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "192.168.1.100"
    finally:
        s.close()
    subnet = '.'.join(local_ip.split('.')[:-1]) + '.0/24'
    return subnet

def scan_arp(subnet):
    print(f"[+] Scanning LAN (ARP) on {subnet} ...")
    packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)
    result = srp(packet, timeout=3, verbose=0)[0]
    
    devices = []
    for _, rcv in result:
        devices.append({"ip": rcv.psrc, "mac": rcv.hwsrc})
    return devices

def fallback_nmap(subnet):
    print(f"[+] Fallback: Using Nmap scan on {subnet} ...")
    try:
        result = subprocess.check_output(["nmap", "-sn", subnet], universal_newlines=True)
        lines = result.split("\n")
        devices = []
        ip, mac = None, None
        for line in lines:
            if "Nmap scan report for" in line:
                ip = line.split("for")[1].strip()
            elif "MAC Address:" in line:
                mac = line.split("MAC Address:")[1].split(" ")[1].strip()
                devices.append({"ip": ip, "mac": mac})
        return devices
    except Exception as e:
        print(f"[!] Nmap scan failed: {e}")
        return []

def save_devices(devices):
    path = os.path.join(os.path.dirname(__file__), "devices.json")
    with open(path, "w") as f:
        json.dump(devices, f, indent=4)
    print(f"[+] Saved {len(devices)} devices to {path}")


def main():
    subnet = get_real_subnet()
    devices = scan_arp(subnet)

    if not devices:
        devices = fallback_nmap(subnet)

    if devices:
        print("[+] Devices found:")
        for idx, d in enumerate(devices, 1):
            print(f"{idx}. IP: {d['ip']}   MAC: {d['mac']}")
        save_devices(devices)
    else:
        print("[!] No devices found or scan failed.")

if __name__ == "__main__":
    main()

