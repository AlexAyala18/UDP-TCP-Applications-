import socket
import time
import hashlib

SERVER_IP = '127.0.0.1'
PORT = 12348
CHUNK_SIZE = 1024
received_packets = 0

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(5)

print("Client started")

filename = input("Enter filename to request: ")
client.sendto(f"REQUEST {filename}".encode(), (SERVER_IP, PORT))

try:
    data, _ = client.recvfrom(1024)
    message = data.decode()

    if message == "ERROR":
        print("File not found on server")
        client.close()
        exit()

    if message.startswith("START"):
        parts = message.split("|")
        filesize = int(parts[1])
        expected_checksum = parts[2]

        print(f"Receiving file of size {filesize} bytes")

    received_data = {}
    total_received = 0

    start_time = time.time()

    while True:
        try:
            packet, _ = client.recvfrom(CHUNK_SIZE + 50)

            if packet == b"END":
                break

            seq_part, file_data = packet.split(b"|", 1)
            seq = int(seq_part.decode())

            if seq not in received_data:
                received_data[seq] = file_data
                total_received += len(file_data)
                received_packets += 1
            # Send ACK
            client.sendto(f"ACK|{seq}".encode(), (SERVER_IP, PORT))

        except socket.timeout:
            print("Timeout waiting for data...")
            break

    end_time = time.time()

    # Reassemble file
    output_filename = "received_" + filename
    with open(output_filename, "wb") as f:
        for i in sorted(received_data):
            f.write(received_data[i])

    total_time = end_time - start_time
    throughput = total_received / total_time if total_time > 0 else 0

    expected_packets = max(received_data.keys())
    loss = expected_packets - received_packets
    loss_percent = (loss / expected_packets) * 100 if expected_packets > 0 else 0

    print("\n--- Transfer Complete ---")
    print(f"Bytes received: {total_received}")
    print(f"Time taken: {total_time:.4f} sec")
    print(f"Throughput: {throughput:.2f} bytes/sec")
    print(f"Packets received: {received_packets}")
    print(f"Estimated packet loss: {loss_percent:.2f}%")

    # 🔥 Compute checksum of received file
    with open(output_filename, "rb") as f:
        received_file_data = f.read()
        received_checksum = hashlib.md5(received_file_data).hexdigest()

    print(f"\nExpected checksum: {expected_checksum}")
    print(f"Received checksum: {received_checksum}")

    if received_checksum == expected_checksum:
        print("✅ File integrity verified (MATCH)")
    else:
        print("❌ File corrupted (MISMATCH)")

except Exception as e:
    print(f"Error: {e}")

client.close()