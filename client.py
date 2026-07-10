import socket
import threading
import time

PORT = 5000

# -----------------------------
# Connect to Server
# -----------------------------
server_ip = input("Enter Server IP: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, PORT))

username = input("Enter Username: ")
client.send(username.encode())


# -----------------------------
# Receive Messages
# -----------------------------
def receive():

    while True:

        try:

            message = client.recv(1024).decode()

            if not message:
                break

            if message == "START":
                print("\n*** Chat Started ***")
                continue

            print(message)

        except:

            print("\nDisconnected from server.")
            break


threading.Thread(
    target=receive,
    daemon=True
).start()

print("\n====================================")
print("Commands:")
print("/list")
print("/msg <username> <message>")
print("exit")
print("====================================\n")


# -----------------------------
# Send Messages
# -----------------------------

while True:

    try:

        message = input()

        if message.lower() == "exit":
            break

        elif message.lower() == "/auto":

            print("\nSending 50 messages...\n")

            for i in range(1, 51):

                text = f"Message {i} from {username}"

                client.send(text.encode())

                print("Sent ->", text)

                time.sleep(0.1)

            print("\nFinished sending 50 messages.\n")

        else:

            client.send(message.encode())

    except:

        break

client.close()