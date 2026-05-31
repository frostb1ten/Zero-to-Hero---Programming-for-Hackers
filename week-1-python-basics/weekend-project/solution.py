# =============================================================
# SOLUTION — Week 1 Project: Target Info Collector
# =============================================================

def print_banner(title):
    """Print a formatted banner."""
    line = "=" * 42
    print(line)
    print(f"  {title}")
    print(line)


def is_valid_port(port):
    """Check if a port number is valid."""
    return 1 <= port <= 65535


def get_valid_port():
    """Keep asking until we get a valid port."""
    while True:
        raw = input("Enter port: ").strip()
        if not raw.isdigit():
            print("[!] Port must be a number. Try again.")
            continue
        port = int(raw)
        if is_valid_port(port):
            return port
        print("[!] Port must be between 1-65535. Try again.")


def build_url(protocol, ip, port):
    """Build a full URL from components."""
    return f"{protocol.lower()}://{ip}:{port}"


def main():
    print_banner("[*] Target Info Collector")

    # Gather inputs
    target_ip = input("Enter target IP: ").strip()
    port = get_valid_port()
    protocol = input("Enter protocol (http/https): ").strip()
    scan_type = input("Enter scan type (quick/full): ").strip()

    # Build the URL
    full_url = build_url(protocol, target_ip, port)

    # Print summary
    print()
    print_banner("[+] Scan Summary")
    print(f"  Target:    {target_ip}")
    print(f"  Port:      {port}")
    print(f"  Protocol:  {protocol.upper()}")
    print(f"  Scan Type: {scan_type.upper()}")
    print(f"  Full URL:  {full_url}")
    print("=" * 42)


main()
