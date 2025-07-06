# python_controller/target_selector.py

import json

def choose_target():
    with open("python_controller/devices.json") as f:
        devices = json.load(f)

    print("\nDiscovered Devices:")
    for i, dev in enumerate(devices):
        print(f"{i+1}. IP: {dev['ip']}   MAC: {dev.get('mac', 'Unknown')}")

    choice = int(input("\nSelect target number to send payload to: ")) - 1
    target = devices[choice]

    with open("python_controller/config.json", "w") as f:
        json.dump(target, f, indent=2)

    print(f"[+] Selected Target: {target['ip']}")
    return target

if __name__ == "__main__":
    choose_target()

