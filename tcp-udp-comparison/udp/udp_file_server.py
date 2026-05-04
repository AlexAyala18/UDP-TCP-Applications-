import socket
import os
import hashlib

HOST = '0.0.0.0'
PORT = 12348
CHUNK_SIZE = 1024
retransmissions = 0

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"UDP File Server running on {HOST}:{PORT}")

while True:
    data, addr = server.recvfrom(1024)
    print(f"Received request from {addr}")

    message = data.decode()

    if message.startswith("REQUEST"):
        filename = message.split(" ", 1)[1]
        print(f"Client requested: {filename}")

        if not os.path.exists(filename):
            server.sendto("ERROR".encode(), addr)
            continue

        filesize = os.path.getsize(filename)

        # 🔥 Compute checksum (MD5)
        with open(filename, "rb") as f:
            file_data = f.read()
            checksum = hashlib.md5(file_data).hexdigest()

        # Send START message with size + checksum
        server.sendto(f"START|{filesize}|{checksum}".encode(), addr)

        seq = 0

        with open(filename, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break

                seq += 1
                packet = f"{seq}|".encode() + chunk

                #Stop-and-wait retransmission
                while True:
                    server.sendto(packet, addr)

                    try:
                        server.settimeout(2)
                        ack_data, _ = server.recvfrom(1024)
                        ack_msg = ack_data.decode()

                        if ack_msg == f"ACK|{seq}":
                            break
                    except socket.timeout:
                        retransmissions += 1
                        print(f"Resending packet {seq}")
                #server.sendto(packet, addr) #ONLY USED FOR NON ACK TESTING

        server.sendto("END".encode(), addr)
        print("File transfer complete")
        print(f"Total retransmissions: {retransmissions}")

        # ✅ Reset timeout so server doesn’t crash
        server.settimeout(None)