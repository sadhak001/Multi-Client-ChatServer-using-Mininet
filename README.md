# Advanced Multi-Client Chat Server (TCP & Mininet)

An enhanced multi-client TCP chat application using Python socket programming and multithreading. Developed and evaluated within a Mininet environment, this project implements advanced client state tracking, private routing, and network performance analysis.

## 🚀 Features
- **Multithreaded Architecture:** Handles concurrent client connections seamlessly over port `5000`.
- **Advanced State Management:** Tracks active usernames, IP addresses, ports, and connection status.
- **Messaging Modes:** Supports global broadcast messaging as well as secure private messaging via `/msg <username> <message>`[cite: 1].
- **Active Directory:** Real-time online user tracking using the `/list` command[cite: 1].
- **Persistent History:** Automatically logs conversations to `chat_history.csv` and restores the last 5 messages upon reconnection[cite: 1].
- **Performance Evaluation:** Tracks message delivery delay and network throughput, logging metrics to `performance_results.csv`[cite: 1].

---

## 🛠️ Network Topology (Mininet)
Simulated using a single switch topology with 5 nodes[cite: 1]:
```bash
sudo mn --topo single,5
h1: Central Chat Server[cite: 1]

h2 to h5: Active Clients (A, B, C, D)[cite: 1]

📁 Repository Structure
Plaintext
Assignment05/
├── server.py               # Multithreaded TCP Server
├── client.py               # Interactive Client Terminal
├── generate_graphs.py      # Automated performance visualization script
├── chat_history.csv        # Persistent chat history database
├── performance_results.csv # Metrics log (Throughput & Delay)
├── Graphs/                 # Automated performance plots
└── Screenshots/            # Wireshark packet capture verifications
💻 How to Run
Start the Mininet Environment:

Bash
sudo mn --topo single,5
Launch the Server (on host h1):

Bash
python3 server.py
Launch Clients (on hosts h2 through h5):

Bash
python3 client.py
🔬 Performance & Verification
Analysis: Experimental evaluation shows that as the client count scales up, concurrent traffic increases overall throughput alongside a gradual increase in average delivery delay[cite: 1].

Wireshark Verification: Network stability and packet routing were verified under the tcp.port == 5000 filter, confirming proper TCP handshakes (SYN/ACK), payload delivery flags (PSH), and clean connection teardowns[cite: 1].
