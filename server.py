import socket
import threading
import time
import csv
import os
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000
MESSAGES_PER_CLIENT = 50
RECV_BUFFER = 1024

CHAT_LOG = "chat_log.csv"
CONNECTION_LOG = "connection_log.csv"
RESULTS_FILE = "performance_results.csv"


class ChatServer:
    def __init__(self, host, port, expected_clients):
        self.expected_clients = expected_clients
        self.expected_messages = expected_clients * MESSAGES_PER_CLIENT

        self.clients = {}          # socket -> {username, ip, port, login_time, status}
        self.lock = threading.Lock()
        self.chat_history = []     # recent messages, shown to newly joined clients

        self.message_count = 0
        self.broadcast_count = 0
        self.private_count = 0
        self.delivery_times = []

        self.experiment_started = False
        self.experiment_completed = False
        self.start_time = 0

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))
        self.socket.listen()

    # ---------------------------------------------------------- utilities

    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _append_csv(path, header, row):
        file_exists = os.path.exists(path)
        with open(path, "a", newline="") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(row)

    def log_connection(self, event, username, ip):
        self._append_csv(CONNECTION_LOG, ["timestamp", "event", "username", "ip"],
                          [self.timestamp(), event, username, ip])

    def save_chat(self, sender, receiver, msg_type, message):
        row = [self.timestamp(), sender, receiver, msg_type, message]
        self.chat_history.append(row)
        self._append_csv(CHAT_LOG, ["timestamp", "sender", "receiver", "type", "message"], row)

    def show_statistics(self):
        with self.lock:
            online = sum(1 for c in self.clients.values() if c["status"] == "Online")
        print(f"[stats] messages={self.message_count} broadcast={self.broadcast_count} "
              f"private={self.private_count} online={online}")

    # ---------------------------------------------------------- messaging

    def broadcast_system(self, text):
        with self.lock:
            for client in self.clients:
                try:
                    client.send(text.encode())
                except OSError:
                    pass

    def broadcast_message(self, sender_socket, sender_name, message):
        start = time.perf_counter()
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(f"[{sender_name}] {message}".encode())
                    except OSError:
                        pass
        self.delivery_times.append((time.perf_counter() - start) * 1000)
        self.broadcast_count += 1
        self.save_chat(sender_name, "ALL", "Broadcast", message)

    def private_message(self, sender_socket, sender_name, receiver_name, message):
        with self.lock:
            target = next(
                (c for c, info in self.clients.items() if info["username"] == receiver_name),
                None,
            )

        if target is None:
            sender_socket.send(f"User '{receiver_name}' not found.".encode())
            return

        try:
            target.send(f"[Private from {sender_name}] {message}".encode())
            sender_socket.send(f"[Private to {receiver_name}] {message}".encode())
            self.private_count += 1
            self.save_chat(sender_name, receiver_name, "Private", message)
        except OSError:
            pass

    def send_online_users(self, client):
        with self.lock:
            names = [info["username"] for info in self.clients.values() if info["status"] == "Online"]
        body = "\n===== ONLINE USERS =====\n" + "\n".join(names) + "\n========================\n"
        client.send(body.encode())

    def send_last_messages(self, client, limit=10):
        if not self.chat_history:
            return
        lines = ["\n===== RECENT CHAT HISTORY =====\n"]
        lines += [f"[{t}] {s} -> {r}: {m}\n" for t, s, r, _, m in self.chat_history[-limit:]]
        lines.append("================================\n")
        try:
            client.send("".join(lines).encode())
        except OSError:
            pass

    # ------------------------------------------------------- performance

    def save_results(self):
        elapsed = time.time() - self.start_time
        avg_delay = sum(self.delivery_times) / len(self.delivery_times) if self.delivery_times else 0
        throughput = self.message_count / elapsed if elapsed > 0 else 0

        self._append_csv(
            RESULTS_FILE,
            ["clients", "broadcast_messages", "private_messages", "avg_delay_ms", "throughput_msgs_per_sec"],
            [self.expected_clients, self.broadcast_count, self.private_count,
             round(avg_delay, 3), round(throughput, 3)],
        )

        print("\n========== PERFORMANCE ==========")
        print("Clients            :", self.expected_clients)
        print("Broadcast Messages :", self.broadcast_count)
        print("Private Messages   :", self.private_count)
        print("Average Delay(ms)  :", round(avg_delay, 3))
        print("Throughput(msg/s)  :", round(throughput, 3))
        print("=================================\n")

    # ------------------------------------------------------ client loop

    def handle_client(self, client):
        username = self.clients[client]["username"]

        while True:
            try:
                data = client.recv(RECV_BUFFER)
                if not data:
                    break

                message = data.decode().strip()

                if not self.experiment_started:
                    self.experiment_started = True
                    self.start_time = time.time()

                print(f"[{username}] {message}")

                if message == "/list":
                    self.send_online_users(client)
                    continue

                if message.startswith("/msg "):
                    parts = message.split(" ", 2)
                    if len(parts) < 3:
                        client.send("Usage: /msg <username> <message>".encode())
                        continue
                    self.private_message(client, username, parts[1], parts[2])
                    self.message_count += 1
                    self.show_statistics()
                    continue

                self.broadcast_message(client, username, message)
                self.message_count += 1
                self.show_statistics()

                if self.message_count >= self.expected_messages and not self.experiment_completed:
                    self.experiment_completed = True
                    self.save_results()

            except Exception:
                break

        self._disconnect(client, username)

    def _disconnect(self, client, username):
        print(f"{username} disconnected")

        with self.lock:
            info = self.clients.get(client)
            if info:
                info["status"] = "Offline"
            ip = info["ip"] if info else "unknown"

        self.broadcast_system(f"\n*** {username} left the chat ***\n")
        self.show_statistics()
        self.log_connection("DISCONNECTED", username, ip)

        with self.lock:
            self.clients.pop(client, None)

        client.close()

    # ------------------------------------------------------------ setup

    def accept_clients(self):
        print(f"\nWaiting for {self.expected_clients} clients...\n")

        while len(self.clients) < self.expected_clients:
            client, address = self.socket.accept()
            username = client.recv(RECV_BUFFER).decode().strip()

            with self.lock:
                self.clients[client] = {
                    "username": username,
                    "ip": address[0],
                    "port": address[1],
                    "login_time": self.timestamp(),
                    "status": "Online",
                }

            print(f"{username} connected ({len(self.clients)}/{self.expected_clients})")
            self.log_connection("CONNECTED", username, address[0])
            self.send_last_messages(client)
            self.broadcast_system(f"\n*** {username} joined the chat ***\n")
            self.show_statistics()

            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def start_experiment(self):
        print("\n===================================")
        print("All Clients Connected")
        print("Experiment starts in 3 seconds...")
        print("===================================")
        time.sleep(3)

        for client in list(self.clients.keys()):
            try:
                client.send("START".encode())
            except OSError:
                pass

        print("\nChat Server Running...\n")

    def run(self):
        self.accept_clients()
        self.start_experiment()

        while not self.experiment_completed:
            time.sleep(1)

        print("\nExperiment Completed")
        print("performance_results.csv saved.")
        print("\nServer Closed.")
        self.socket.close()


if __name__ == "__main__":
    print("=" * 50)
    print(" Advanced Multi-Client Chat Server ")
    print("=" * 50)

    num_clients = int(input("\nEnter number of clients (2/3/4): "))

    server = ChatServer(HOST, PORT, num_clients)
    print("Listening on Port", PORT)
    server.run()
    
    