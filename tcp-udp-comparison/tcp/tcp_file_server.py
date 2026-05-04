import socket
import os

HOST = '0.0.0.0'
PORT = 12346  # different port from chat

CHUNK_SIZE = 1024

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"File server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Connected with {addr}")

        try:
            # Receive requested filename
            filename = conn.recv(1024).decode()
            print(f"Client requested file: {filename}")

            if not os.path.exists(filename):
                conn.send("ERROR".encode())
                conn.close()
                continue


            # Send file size along with okay signal
            filesize = os.path.getsize(filename)
            conn.sendall(f"OK\n{filesize}\n".encode())

            # Send file in chunks
            with open(filename, "rb") as f:
                while True:
                    data = f.read(CHUNK_SIZE)
                    if not data:
                        break
                    conn.sendall(data)

            print(f"File '{filename}' sent successfully")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            conn.close()

if __name__ == "__main__":
    start_server()