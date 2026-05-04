import matplotlib.pyplot as plt
import os

os.makedirs("results", exist_ok=True)

# Simulated based on your observations
message_sizes = [10, 50, 100, 200, 500]

udp_latency = [0.001, 0.003, 0.005, 0.010, 0.020]
tcp_latency = [0.0005, 0.001, 0.002, 0.003, 0.005]

plt.figure()
plt.plot(message_sizes, udp_latency, marker='o', label='UDP')
plt.plot(message_sizes, tcp_latency, marker='o', label='TCP')

plt.xlabel("Message Size (characters)")
plt.ylabel("Latency (seconds)")
plt.title("TCP vs UDP Chat Latency")
plt.legend()
plt.grid()

plt.savefig("results/chat_latency.png")
plt.show()