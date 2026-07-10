# Advanced Multi-Client TCP Chat Server

A feature-rich multi-client chat application developed using **Python Socket Programming** and **TCP**. This project extends a basic TCP chat server by adding advanced client management, private messaging, persistent chat history, performance monitoring, graph generation, and packet-level verification using Wireshark.

The application demonstrates concepts of **Computer Networks**, **TCP Socket Programming**, **Multithreading**, and **Client-Server Communication** through a centralized server architecture.

---

## Features

### Multi-Client Support
- Supports multiple clients connecting simultaneously.
- Each client is handled using a separate thread.
- Centralized TCP server manages all active connections.

### User Management
- Username-based login.
- Stores client information including:
  - Username
  - IP Address
  - Port Number
  - Login Time
  - Online/Offline Status

### Broadcast Messaging
- Messages are delivered to all connected clients.
- Sender does not receive their own broadcast.

### Private Messaging
- Send private messages using:

```text
/msg <username> <message>
```

Example:

```text
/msg Aman Hello!
```

Only the intended recipient receives the message.

### Online User List

Display all currently connected users using:

```text
/list
```

### Join & Leave Notifications

The server automatically broadcasts notifications whenever:
- A new user joins
- A user disconnects

### Persistent Chat History

- Chat messages are stored in:

```
chat_history.csv
```

- When a client reconnects, the server displays the previous five messages.

### Performance Monitoring

The server records:

- Average Message Delay
- Throughput
- Broadcast Messages
- Private Messages

Results are saved in:

```
performance_results.csv
```

### Automatic Graph Generation

Performance graphs are generated automatically, including:

- Clients vs Average Delay
- Clients vs Throughput
- Broadcast vs Private Messages

### Wireshark Verification

TCP packets were analyzed using Wireshark to verify:

- TCP Three-Way Handshake
- Broadcast Communication
- Private Messaging
- Client Disconnection
- Four-Way Connection Termination

---

# Project Structure

```
├── server.py
├── client.py
├── chat_history.csv
├── performance_results.csv
├── generate_graphs.py
├── graphs/
├── screenshots/
└── README.md
```

---

# Working

## Step 1

Start the server.

The server listens on TCP Port **5000** and waits for incoming client connections.

---

## Step 2

Clients connect to the server.

Each client provides a username after connecting.

The server stores:

- Username
- IP Address
- Port
- Login Time
- Connection Status

---

## Step 3

Messaging

Users can:

- Send broadcast messages
- Send private messages
- View online users

Every incoming message is classified by the server and routed accordingly.

---

## Step 4

Chat History

Every message is written to:

```
chat_history.csv
```

When users reconnect, the last five chat messages are displayed.

---

## Step 5

Performance Evaluation

During execution, the server records:

- Message Delay
- Throughput
- Number of Broadcast Messages
- Number of Private Messages

These statistics are stored in:

```
performance_results.csv
```

---

## Step 6

Graph Generation

Run:

```bash
python generate_graphs.py
```

The script generates graphs for:

- Average Delay
- Throughput
- Broadcast vs Private Messages

---

# Commands

| Command | Description |
|----------|-------------|
| `/list` | Show online users |
| `/msg <username> <message>` | Send private message |

---

# Technologies Used

- Python 3
- Socket Programming
- TCP Protocol
- Multithreading
- CSV
- Matplotlib
- Mininet
- Wireshark

---

# Experimental Setup

- 1 TCP Server
- 4 Clients
- Mininet Topology

```bash
sudo mn --topo single,5
```

Server Port:

```
5000
```

---

# Performance Analysis

The application evaluates:

- Average Delivery Delay
- Throughput
- Broadcast Messages
- Private Messages

As the number of connected clients increases:

- Average delay increases due to concurrent processing.
- Throughput also increases as more messages are transmitted.

---

# Wireshark Verification

Packet captures verify:

- TCP Three-Way Handshake (SYN, SYN-ACK, ACK)
- Broadcast Messaging
- Private Messaging
- FIN/ACK Connection Termination

Display Filter:

```text
tcp.port == 5000
```

---

# Future Improvements

- TLS Encryption
- User Authentication
- GUI Interface
- Group Chat
- File Sharing
- Emoji Support
- Offline Messaging
- Database Storage
- Improved Scalability using Async I/O

---

# Learning Outcomes

This project provides practical experience in:

- TCP Socket Programming
- Client-Server Architecture
- Concurrent Programming
- Network Communication
- Performance Evaluation
- Wireshark Packet Analysis

---

# Author

**Aman**

Advanced Computer Networks Lab Assignment
