import matplotlib.pyplot as plt

file_sizes = [100000, 1000000, 5000000]

# UDP data
udp_throughput = [3613100.63, 9500918.54, 9098869.38]
udp_time = [0.0277, 0.1053, 0.5495]

# TCP data
tcp_throughput = [3178899.82, 32403961.74, 74227323.73]
tcp_time = [0.0315, 0.0309, 0.0674]

# Throughput graph
plt.figure()
plt.plot(file_sizes, udp_throughput, marker='o', label='UDP')
plt.plot(file_sizes, tcp_throughput, marker='o', label='TCP')
plt.xlabel("File Size (bytes)")
plt.ylabel("Throughput (bytes/sec)")
plt.title("TCP vs UDP Throughput")
plt.legend()
plt.grid()
plt.savefig("results/file_throughput.png")

# Time graph
plt.figure()
plt.plot(file_sizes, udp_time, marker='o', label='UDP')
plt.plot(file_sizes, tcp_time, marker='o', label='TCP')
plt.xlabel("File Size (bytes)")
plt.ylabel("Time (seconds)")
plt.title("TCP vs UDP Transfer Time")
plt.legend()
plt.grid()
plt.savefig("results/file_time.png")

plt.show()