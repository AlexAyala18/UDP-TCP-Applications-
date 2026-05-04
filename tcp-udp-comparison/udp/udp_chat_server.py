import socket

HOST = '0.0.0.0'
PORT = 12347

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"UDP server running on {HOST}:{PORT}")

clients = {}  # addr -> username

while True:
    data, addr = server.recvfrom(1024)
    message = data.decode().strip()

    # REGISTER
    if message.startswith("REGISTER"):
        try:
            username = message.split(" ", 1)[1]
            clients[addr] = username
            print(f"{username} registered from {addr}")
        except:
            print("Invalid REGISTER format")
        continue

    # Ignore unregistered clients
    if addr not in clients:
        continue

    username = clients[addr]

    # Parse message: SEQ|TIMESTAMP|MESSAGE
    try:
        seq, timestamp, msg = message.split("|", 2)
    except:
        print("Invalid message format")
        continue

    print(f"{username} [SEQ {seq}]: {msg}")

    # Send ACK
    server.sendto(f"ACK|{seq}".encode(), addr)

    # Broadcast message WITH timestamp preserved
    for client_addr in clients:
        if client_addr != addr:
            forward_message = f"{seq}|{timestamp}|{msg}"
            server.sendto(forward_message.encode(), client_addr)