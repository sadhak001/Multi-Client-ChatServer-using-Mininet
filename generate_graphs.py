import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("performance_results.csv")

# Clients vs Delay
plt.figure(figsize=(6,4))
plt.plot(df["clients"], df["avg_delay_ms"], marker="o")
plt.title("Clients vs Average Delay")
plt.xlabel("Number of Clients")
plt.ylabel("Average Delay (ms)")
plt.grid(True)
plt.savefig("clients_vs_delay.png")
plt.close()

# Clients vs Throughput
plt.figure(figsize=(6,4))
plt.plot(df["clients"], df["throughput_msgs_per_sec"], marker="o")
plt.title("Clients vs Throughput")
plt.xlabel("Number of Clients")
plt.ylabel("Throughput (msg/sec)")
plt.grid(True)
plt.savefig("clients_vs_throughput.png")
plt.close()

# Broadcast vs Private Messages
plt.figure(figsize=(6,4))
plt.bar(["Broadcast", "Private"], [
    df["broadcast_messages"].sum(),
    df["private_messages"].sum()
])
plt.title("Broadcast vs Private Messages")
plt.savefig("message_type_distribution.png")
plt.close()

print("Graphs generated successfully.")