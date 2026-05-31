# =============================================================
# SOLUTION — Week 2 Project: Network Inventory Manager
# =============================================================
import os

inventory = []


def print_banner():
    print("=" * 42)
    print("  Network Inventory Manager")
    print("=" * 42)


def add_host():
    ip = input("IP: ").strip()
    hostname = input("Hostname: ").strip()
    os_name = input("OS: ").strip()
    ports = input("Open ports (comma-separated): ").strip()

    host = {
        "ip": ip,
        "hostname": hostname,
        "os": os_name,
        "ports": ports
    }
    inventory.append(host)
    print("[+] Host added!")


def list_hosts():
    if not inventory:
        print("[!] Inventory is empty.")
        return

    print(f"\n{'IP':<16} {'Hostname':<15} {'OS':<12} {'Ports'}")
    print("-" * 55)
    for host in inventory:
        print(f"{host['ip']:<16} {host['hostname']:<15} {host['os']:<12} {host['ports']}")


def search_host():
    target = input("Search IP: ").strip()
    found = [h for h in inventory if h["ip"] == target]

    if found:
        for h in found:
            print(f"\n  IP:       {h['ip']}")
            print(f"  Hostname: {h['hostname']}")
            print(f"  OS:       {h['os']}")
            print(f"  Ports:    {h['ports']}")
    else:
        print(f"[!] No host found with IP {target}")


def save_to_file():
    filename = input("Filename (default: inventory.csv): ").strip()
    if not filename:
        filename = "inventory.csv"

    with open(filename, "w") as f:
        f.write("ip,hostname,os,ports\n")
        for host in inventory:
            f.write(f"{host['ip']},{host['hostname']},{host['os']},{host['ports']}\n")

    print(f"[+] Saved {len(inventory)} hosts to {filename}")


def load_from_file():
    filename = input("Filename (default: inventory.csv): ").strip()
    if not filename:
        filename = "inventory.csv"

    if not os.path.exists(filename):
        print(f"[!] File {filename} not found")
        return

    inventory.clear()
    with open(filename, "r") as f:
        header = f.readline()  # skip header
        for line in f:
            parts = line.strip().split(",", 3)
            if len(parts) == 4:
                inventory.append({
                    "ip": parts[0],
                    "hostname": parts[1],
                    "os": parts[2],
                    "ports": parts[3]
                })

    print(f"[+] Loaded {len(inventory)} hosts from {filename}")


def main():
    print_banner()

    while True:
        print("\n[1] Add host")
        print("[2] List hosts")
        print("[3] Search by IP")
        print("[4] Save to file")
        print("[5] Load from file")
        print("[6] Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            add_host()
        elif choice == "2":
            list_hosts()
        elif choice == "3":
            search_host()
        elif choice == "4":
            save_to_file()
        elif choice == "5":
            load_from_file()
        elif choice == "6":
            print("[*] Goodbye!")
            break
        else:
            print("[!] Invalid choice")


main()
