import socket
import threading
import time

SERVER_IP = '127.0.0.1'
PORT = 12347

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(2)

# Register username
username = input("Enter username: ")
client.sendto(f"REGISTER {username}".encode(), (SERVER_IP, PORT))

seq_num = 0
ack_received = True

def receive():
    global ack_received

    while True:
        try:
            data, _ = client.recvfrom(1024)
            message = data.decode()

            # Handle ACK
            if message.startswith("ACK"):
                ack_seq = message.split("|")[1]
                print(f"[ACK RECEIVED for SEQ {ack_seq}]")
                ack_received = True
            else:
                # Handle normal message with latency
                parts = message.split("|", 2)
                if len(parts) == 3:
                    seq, sent_time, msg = parts
                    latency = time.time() - float(sent_time)
                    print(f"{msg} (Latency: {latency:.4f}s)")
                else:
                    print(message)

        except socket.timeout:
            continue
        except:
            print("Disconnected from server")
            break

def send():
    global seq_num, ack_received

    while True:
        message = input()

        if message.strip() == "":
            continue

        seq_num += 1
        timestamp = time.time()

        full_message = f"{seq_num}|{timestamp}|{message}"

        ack_received = False

        # Stop-and-wait retransmission
        while not ack_received:
            print(f"[SENDING SEQ {seq_num}]")
            client.sendto(full_message.encode(), (SERVER_IP, PORT))
            time.sleep(2)

# Start threads
threading.Thread(target=receive, daemon=True).start()
send()