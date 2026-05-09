import subprocess
import xml.etree.ElementTree as ET
import json
import platform

# --- Configuration ---
# IMPORTANT: Change this to your network's IP range!
NETWORK_TO_SCAN = '10.235.217.0/24' # Use the one you found earlier
NMAP_OUTPUT_FILE = 'scan_results.xml'
JSON_OUTPUT_FILE = 'data.json'

def get_device_type(os_name, open_ports):
    """Guesses the device type based on OS name and open ports."""
    os_name_lower = os_name.lower()
    if "router" in os_name_lower or "gateway" in os_name_lower:
        return "router"
    if "windows" in os_name_lower:
        return "windows"
    if "linux" in os_name_lower:
        return "linux"
    if "mac" in os_name_lower or "apple" in os_name_lower:
        return "mac"
    # Fallback to checking common ports
    for port_info in open_ports:
        if port_info.get("service") in ["http", "https", "http-proxy"]:
            return "web-server"
    return "host" # Default type

def run_nmap_scan():
    """Runs an Nmap scan and saves the output to an XML file."""
    print(f"[*] Starting Nmap scan for {NETWORK_TO_SCAN}...")
    print("[*] This may take several minutes...")

    # Nmap command: -sV (service version), -O (OS detection), -Pn (treat hosts as online), -oX (XML output)
    command = ['nmap', '-sV', '-O', '-Pn', '-oX', NMAP_OUTPUT_FILE, NETWORK_TO_SCAN]
    
    # OS detection often requires elevated privileges
    is_admin = (platform.system() == "Windows" and subprocess.run("net session", capture_output=True).returncode == 0) or \
               (platform.system() != "Windows" and subprocess.run("id -u", capture_output=True, text=True).stdout.strip() == "0")

    if not is_admin:
        print("[!] Warning: Nmap OS detection (-O) works best with root/administrator privileges.")
        print("[!] Running without elevated privileges...")

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"[+] Nmap scan complete. Results saved to {NMAP_OUTPUT_FILE}")
    except FileNotFoundError:
        print("[!] Error: 'nmap' command not found. Is Nmap installed and in your PATH?")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running Nmap. Nmap output:\n{e.stderr}")

def parse_xml_to_json():
    """Parses the Nmap XML output and converts it to a JSON format for Cytoscape."""
    print(f"[*] Parsing {NMAP_OUTPUT_FILE}...")
    nodes = []
    edges = []
    
    try:
        tree = ET.parse(NMAP_OUTPUT_FILE)
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError) as e:
        print(f"[!] Error processing XML file: {e}")
        return

    # Find the gateway (usually the .1 address, but we find it dynamically now)
    gateway_ip = None
    for host in root.findall('host'):
        if host.find("status").get("state") == "up":
            # Heuristic: The device with the lowest IP number is often the gateway
            ip = host.find("address").get("addr")
            if gateway_ip is None or int(ip.split('.')[-1]) < int(gateway_ip.split('.')[-1]):
                gateway_ip = ip

    for host in root.findall('host'):
        if host.find("status").get("state") != "up":
            continue

        ip_address = host.find('address').get('addr')
        
        # Extract OS information
        os_match = host.find(".//osmatch")
        os_name = os_match.get('name') if os_match is not None else "Unknown OS"

        # Extract open ports and services
        open_ports = []
        ports = host.find("ports")
        if ports:
            for port in ports.findall("port"):
                if port.find("state").get("state") == "open":
                    service = port.find("service")
                    port_info = {
                        "portid": port.get("portid"),
                        "protocol": port.get("protocol"),
                        "service": service.get("name") if service is not None else "unknown"
                    }
                    open_ports.append(port_info)
        
        device_type = get_device_type(os_name, open_ports)
        if ip_address == gateway_ip:
            device_type = "router"

        # Create a node for the host with all its data
        nodes.append({
            "data": {
                "id": ip_address,
                "label": f"({device_type.capitalize()})\n{ip_address}",
                "type": device_type,
                "os": os_name,
                "ports": open_ports
            }
        })
        
        # Create an edge connecting the host to the gateway, unless it IS the gateway
        if ip_address != gateway_ip and gateway_ip:
            edges.append({"data": {"source": ip_address, "target": gateway_ip}})

    graph_data = {"nodes": nodes, "edges": edges}

    with open(JSON_OUTPUT_FILE, 'w') as f:
        json.dump(graph_data, f, indent=4)
    
    print(f"[+] Network map data saved to {JSON_OUTPUT_FILE}")

if __name__ == '__main__':
    run_nmap_scan()
    parse_xml_to_json()
