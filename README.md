# Interactive Network Scanner and Visualizer

A powerful **LAN Discovery and Network Visualization Tool** that scans your local network, detects active devices, identifies operating systems and services, and displays everything in an interactive graphical map.


---

## 📋 Project Description

This tool automates network scanning using **Nmap** and transforms the complex scan results into a beautiful, interactive network graph using **Cytoscape.js**. It helps users visually understand their local network topology, device types, and running services.

---

## ✨ Key Features

- **Automated Network Scanning** – Discovers all active hosts in a given IP range
- **Deep Host Enumeration** – Detects OS, open ports, and running services
- **Interactive Graph Visualization** – Physics-based network map with drag & zoom support
- **Device Categorization** – Color-coded nodes (Router, Windows, Linux, etc.)
- **Details on Click** – Click any device to view full information in a sidebar
- **Clean Data Pipeline** – Python backend + JSON + JavaScript frontend

---

## 🛠️ Technologies Used

| Technology          | Purpose                          |
|---------------------|----------------------------------|
| **Nmap**            | Network scanning & OS detection  |
| **Python**          | Backend scripting & data parsing |
| **Cytoscape.js**    | Interactive graph visualization  |
| **HTML + CSS + JS** | Frontend interface               |
| **JSON**            | Data exchange between backend & frontend |

**Libraries:**
- `subprocess`, `xml.etree.ElementTree`, `json` (Python)

---
