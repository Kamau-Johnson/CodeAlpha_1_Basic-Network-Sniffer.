import socket
import threading
import time
import tkinter as tk
from tkinter import scrolledtext

# Function to capture packets (Runs in a separate thread)
def capture_packets():
    global running
    running = True  # Flag to stop sniffing

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sniffer.bind(("0.0.0.0", 0))  # Bind to all network interfaces

    print("[+] Sniffing started...")

    while running:
        try:
            raw_packet, addr = sniffer.recvfrom(65535)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            log = f"{timestamp} | Packet from {addr}\n"
            
            # Update GUI (Use .after() to avoid threading issues)
            text_area.after(0, text_area.insert, tk.END, log)
            text_area.after(0, text_area.yview, tk.END)

        except Exception as e:
            print(f"Error: {e}")
            break

    sniffer.close()
    print("[+] Sniffing stopped.")

# Function to start sniffing in a separate thread
def start_sniffer():
    global sniff_thread
    sniff_thread = threading.Thread(target=capture_packets, daemon=True)
    sniff_thread.start()

# Function to stop sniffing
def stop_sniffer():
    global running
    running = False

# GUI Setup
app = tk.Tk()
app.title("Network Sniffer")
app.geometry("600x400")

text_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=20)
text_area.pack(pady=10)

start_button = tk.Button(app, text="Start Sniffing", command=start_sniffer)
start_button.pack()

stop_button = tk.Button(app, text="Stop Sniffing", command=stop_sniffer)
stop_button.pack()

app.mainloop()
