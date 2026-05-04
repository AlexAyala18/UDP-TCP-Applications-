# TCP vs UDP Communication System

Author: Alexander Ayala

## Overview

This project implements and compares TCP and UDP protocols through two applications:
- Chat system
- File transfer system

Both TCP and UDP versions were developed. Since UDP does not provide built-in reliability, a custom reliability layer was implemented to handle packet loss, ordering, and data integrity.

---

## Features

### TCP Chat
- Multi-client communication
- Reliable and ordered message delivery

### UDP Chat
- Sequence numbers for ordering
- Acknowledgment (ACK) handling
- Retransmission using stop-and-wait protocol

### TCP File Transfer
- Reliable file transmission
- Throughput and transfer time measurement

### UDP File Transfer
- Custom reliability layer using:
  - Sequence numbers
  - ACK-based confirmation
  - Retransmission logic
- Packet tracking and ordering
- MD5 checksum verification for data integrity

---

## Key Concepts

- Transport layer protocols (TCP vs UDP)
- Reliable vs unreliable communication
- Stop-and-wait protocol implementation
- Packet loss handling and retransmission
- Data integrity validation

---

## Performance Analysis

Experiments were conducted using files of varying sizes:
- 100 KB
- 1 MB
- 5 MB

Metrics collected:
- Throughput
- Latency
- Transfer time
- Packet loss and retransmissions

Results are stored in:
- results/chat_latency.png
- results/file_throughput.png
- results/file_time.png

---

## How to Run

### TCP Chat
Run server:
python TCP/tcp_chat_server.py

Run client(s):
python TCP/tcp_chat_client.py

---

### UDP Chat
Run server:
python UDP/udp_chat_server.py

Run client(s):
python UDP/udp_chat_client.py

---

### TCP File Transfer
Run server:
python TCP/tcp_file_server.py

Run client:
python TCP/tcp_file_client.py

---

### UDP File Transfer
Run server:
python UDP/udp_file_server.py

Run client:
python UDP/udp_file_client.py

---

## Generating Graphs

Run:
python experiments/make_graphs.py

---

## Screenshots

TCP Chat  
![TCP Chat](screenshots/TCP%20Chat%20System.png)

UDP Chat  
![UDP Chat](screenshots/UDP%20Chat%20System.png)

TCP File Transfer  
![TCP File](screenshots/TCP%20File%20System.png)

UDP File Transfer  
![UDP File](screenshots/UDP%20File%20System.png)

---

## Notes

- UDP reliability was implemented using a stop-and-wait protocol
- Packet loss and retransmissions were explicitly handled
- TCP performed better for large file transfers due to built-in reliability
- UDP required additional logic but demonstrated flexibility

---

## Summary

This project demonstrates the trade-offs between TCP and UDP by implementing both protocols and analyzing their behavior under real-world conditions.
