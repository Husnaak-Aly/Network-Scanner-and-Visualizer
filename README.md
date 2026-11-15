# 🔍 Network Scanner & Visualizer

> A Python tool that discovers live hosts and open ports on a local network and shows the results as an interactive network map.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)


## ⚠️ Disclaimer
This tool is for **educational purposes and authorized networks only**. Scanning networks you do not own or lack permission to test may be illegal.

## ✨ Features
- 🖧 Host discovery using ARP / ICMP ping sweep
- 🔌 Port scanning on common TCP ports
- 🏷️ Service and MAC vendor detection
- 🗺️ Network topology visualization
- 💾 Export results to CSV / JSON

<!-- Edit this list to match what your tool actually does -->

## 🛠️ Tech Stack
- **Python 3**
- `scapy`: packet crafting & ARP scanning
- `socket`: port scanning
- `networkx` + `matplotlib`: visualization

<!-- Replace with the libraries you actually used -->

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Admin/root privileges (needed for raw packets)

### Installation
```bash
git clone https://github.com/Husnaak-Aly/Network-Scanner-and-Visualizer.git
cd Network-Scanner-and-Visualizer
pip install -r requirements.txt
```

### Usage
```bash
# Scan a subnet
sudo python scanner.py --target 192.168.1.0/24

# Scan specific ports and save results
sudo python scanner.py --target 192.168.1.0/24 --ports 22,80,443 --output results.json
```

## 📁 Project Structure
```
Network-Scanner-and-Visualizer/
├── scanner.py          # Entry point
├── modules/
│   ├── discovery.py    # Host discovery
│   ├── ports.py        # Port scanning
│   └── visualize.py    # Graph rendering
├── docs/               # Screenshots & demo GIF
├── requirements.txt
└── README.md
```

## 🧠 What I Learned
- How ARP and ICMP work at the packet level
- TCP handshakes and how port states (open/closed/filtered) are detected
- Handling timeouts and concurrency for faster scans

## 🔮 Future Improvements
- [ ] OS fingerprinting
- [ ] Banner grabbing for service versions
- [ ] Web dashboard for results

## 👤 Author
**Husnaak Mansoor** · [LinkedIn](https://www.linkedin.com/in/husnaak-mansoor-78728b2aa) · [GitHub](https://github.com/Husnaak-Aly)

## 📄 License
MIT
